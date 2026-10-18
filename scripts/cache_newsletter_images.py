#!/usr/bin/env python3
"""Prepare independently stored, optimized newsletter images on a GitHub runner."""
import hashlib
import io
import json
import textwrap
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"assets"/"events"
HEADERS={"User-Agent":"BMI-Newsletter/1.0 (+https://www.magyariskola.at/)"}
SIZE=(640,360)

def sources(event):
    data=event.get("image",{})
    if data.get("mediaId"):
        yield "https://static.wixstatic.com/media/"+data["mediaId"]
    for key in ("url","original"):
        u=data.get(key)
        if u and u.startswith("https://") and "/v1/fill/" not in u:
            yield u

def download(session, event):
    failures=[]
    for u in dict.fromkeys(sources(event)):
        try:
            with session.get(u,stream=True,timeout=(8,22),headers=HEADERS,allow_redirects=True) as r:
                r.raise_for_status()
                chunks=[]; length=0
                for c in r.iter_content(65536):
                    length+=len(c)
                    if length>12*1024*1024: raise ValueError("Source exceeds 12MiB")
                    chunks.append(c)
            im=Image.open(io.BytesIO(b"".join(chunks)))
            im.load()
            if min(im.size)<64 or im.width*im.height>50_000_000:
                raise ValueError("Source image geometry invalid")
            return im,u,failures
        except (requests.RequestException,UnidentifiedImageError,OSError,ValueError) as error:
            failures.append(f"{urlparse(u).hostname}: {type(error).__name__}")
    return None,None,failures

def fallback(event):
    """An honest, locally hosted placeholder if sources fail; not a fake event photograph."""
    im=Image.new("RGB",SIZE,"#e8eef3")
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,640,11),fill="#173d5b")
    try:
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",27)
        small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",14)
    except OSError:
        font=small=ImageFont.load_default()
    for n,line in enumerate(textwrap.wrap(event["title"],width=28)[:3]):
        d.text((38,112+42*n),line,font=font,fill="#173d5b")
    d.text((38,316),"EVENT INFO  ·  PHOTO NOT AVAILABLE",font=small,fill="#526878")
    return im

def main():
    groups=json.loads((ROOT/"data"/"programajanlo-2026-10-18.json").read_text(encoding="utf-8"))["groups"]
    events=[ev for group in groups for ev in group["events"]]
    if len(events)!=19: raise ValueError(f"Expected 19 events, got {len(events)}")
    session=requests.Session()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    records={}
    for event in events:
        im,url,errors=download(session,event)
        status="photo" if im is not None else "labelled_fallback"
        if im is None: im=fallback(event)
        im=(ImageOps.contain(im.convert("RGB"),(1104,1400),method=Image.Resampling.LANCZOS) if event.get("image",{}).get("kind")=="first_party" else ImageOps.fit(im.convert("RGB"),SIZE,method=Image.Resampling.LANCZOS))
        kind=event.get("image",{}).get("kind")
        if kind=="first_party": rights="first-party"
        elif kind=="official_event_artwork": rights="official event artwork supplied by user"
        elif kind=="generated_poster": rights="generated for BMI newsletter; not official organiser artwork"
        else: rights="third-party rights review"
        records[event["id"]]={"status":status,"sourceUrl":url,"errors":errors,"files":{},"photoRights":rights,"sourceKind":kind}
        for ext,options in [("jpg",dict(format="JPEG",quality=72,optimize=True,progressive=True)),("webp",dict(format="WEBP",quality=70,method=5))]:
            p=OUTPUT/(event["id"]+"-640."+ext)
            im.save(p,**options)
            raw=p.read_bytes()
            records[event["id"]]["files"][ext]={"path":p.relative_to(ROOT).as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
        print(event["id"],status,records[event["id"]]["files"]["jpg"]["bytes"],flush=True)
    # The BMI crest is a first-party logo, separate from event artwork.
    logo_url="https://static.wixstatic.com/media/b0aee1_944db6e866844c83b2e5d8b7bdf7ecb6~mv2.png"
    crest,url,issues=download(session,{"title":"Bécsi Magyar Iskola","image":{"original":logo_url}})
    if crest is None:
        raise RuntimeError("Unable to validate the official masthead logo source: "+str(issues))
    crest=ImageOps.contain(crest.convert("RGBA"),(272,276),method=Image.Resampling.LANCZOS)
    logoFiles={}
    for ext,options in [("png",dict(format="PNG",optimize=True)),("webp",dict(format="WEBP",lossless=True,method=5))]:
        path=ROOT/"assets"/("bmi-logo-272."+ext)
        path.parent.mkdir(parents=True,exist_ok=True)
        crest.save(path,**options)
        b=path.read_bytes()
        logoFiles[ext]={"path":path.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
    out={"edition":"2026-27-W07","generatedAt":datetime.now(timezone.utc).isoformat(),"images":records,"logo":{"status":"first_party","sourceUrl":logo_url,"files":logoFiles}}
    (ROOT/"data"/"event-image-assets.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
