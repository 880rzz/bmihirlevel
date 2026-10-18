#!/usr/bin/env python3
"""Switch six BMI newsletter HTML files to the verified, local GitHub image files."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVENTS=json.loads((ROOT/"data"/"programajanlo-2026-10-18.json").read_text(encoding="utf-8"))["groups"]
PROGRAMS=[event for group in EVENTS for event in group["events"]]
if len(PROGRAMS)!=19: raise ValueError("Expected 19 source events")
WEB_FILES=("index.html","de/index.html","en/index.html")
EMAIL_FILES=(
    "exports/bmi-hirlevel-wix-2026-10-18.html",
    "exports/bmi-hirlevel-wix-de-2026-10-18.html",
    "exports/bmi-hirlevel-wix-en-2026-10-18.html",
)
SITE="https://hirlevel.magyariskola.at"
REGISTRY=ROOT/"data"/"event-image-assets.json"
assets=json.loads(REGISTRY.read_text(encoding="utf-8"))["images"]

for rel in (*WEB_FILES,*EMAIL_FILES):
    p=ROOT/rel
    text=p.read_text(encoding="utf-8")
    email=rel in EMAIL_FILES
    replacements={}
    for ev in PROGRAMS:
        eid=ev["id"]
        ext="jpg" if email else "webp"
        path=f"/assets/events/{eid}-640.{ext}"
        target=(SITE+path) if email else path
        if not (ROOT/path.lstrip("/")).exists():
            raise FileNotFoundError(path)
        if eid.startswith("bmi-"):
            old=ev.get("image",{}).get("url")
            if not old: raise ValueError("Missing first-party source for "+eid)
            expected=3 if rel=="index.html" else 1
            present=text.count('src="'+old+'"')
            if present!=expected: raise ValueError(f"Missing BMI image {eid} in {rel}: {present}/{expected}")
            text=text.replace('src="'+old+'"','src="'+target+'"')
        else:
            pattern=r'(<div data-event-thumb="'+re.escape(eid)+r'"[^>]*>\s*<img\s+src=")([^"]+)(")'
            text,count=re.subn(pattern,lambda m:m.group(1)+target+m.group(3),text)
            expected=3 if rel=="index.html" else 1
            if count!=expected: raise ValueError(f"Event photo missing {eid} in {rel}: {count}/{expected}")
        replacements[eid]=target
    if len(replacements)!=19: raise ValueError("Incomplete imagery")
    # The independent BMI masthead logo remains in its previously working Wix URL.
    # All 19 programme visuals must already have GitHub assets before migration.
    remaining=re.findall(r'<img\b[^>]*src="https://static\.wixstatic\.com/media/[^"]+"[^>]*>',text)
    if any("Wiener Ungarische Schule" not in image for image in remaining):
        raise ValueError("Unmigrated programme image remains in "+rel)
    if email and '<script' in text:
        raise ValueError("JavaScript leaked into "+rel)
    p.write_text(text,encoding="utf-8")
    print(rel,len(replacements),"complete, local image URLs",flush=True)

manifest=ROOT/"data"/"programajanlo-2026-10-18.json"
source=json.loads(manifest.read_text(encoding="utf-8"))
for group in source["groups"]:
    for ev in group["events"]:
        data=ev.setdefault("image",{})
        eid=ev["id"]
        data["githubAsset"]="/assets/events/"+eid+"-640.webp"
        data["githubEmailAsset"]=SITE+"/assets/events/"+eid+"-640.jpg"
        data["assetGenerationStatus"]=assets[eid]["status"]
        data["wixExternalDependencyRemoved"]=True
manifest.write_text(json.dumps(source,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
