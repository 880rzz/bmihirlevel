#!/usr/bin/env python3
"""Validate exact-live newsletter pages and every GitHub-hosted image response."""
import json,re,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urljoin
from urllib.request import Request,urlopen
BASE="https://hirlevel.magyariskola.at"
ROUTES=["/","/de/","/en/"]
IDS=["pumpkin","kkunst","sicher","prater","run","friedhof","schoen","buch","traume","h1956","viennale","hsecession","u4","hdarvasi","comic","hkoncz","bmi-forradalom","bmi-ruhacsere","bmi-telapo"]
FILES=[f"/assets/events/{name}-640.{ext}" for name in IDS for ext in ("jpg","webp")]+["/assets/bmi-logo-272.png","/assets/bmi-logo-272.webp"]

def fetch(path,expected):
    url=urljoin(BASE,path)
    with urlopen(Request(url,headers={"User-Agent":"BMI-Newsletter-Production-QA/1.0"}),timeout=12) as response:
        if response.status!=200:raise ValueError(f"{url}: HTTP {response.status}")
        mime=response.headers.get("Content-Type","").lower()
        raw=response.read()
        if expected not in mime:raise ValueError(f"{url}: expected {expected}, got {mime}")
        if len(raw)<100:raise ValueError(f"{url}: response too small")
        return raw

def audit():
    pages=[]
    for route in ROUTES:
        html=fetch(route,"text/html").decode("utf-8")
        if "/assets/bmi-logo-272.webp" not in html:raise ValueError(route+": BMI logo not local")
        for id in IDS:
            if f"/assets/events/{id}-640.webp" not in html:raise ValueError(route+": missing "+id)
        if "border-radius:5px" not in html:raise ValueError(route+": missing 5px design")
        if re.search(r'<img\b[^>]*src="https://static\.wixstatic\.com/',html):raise ValueError(route+": unresolved Wix source")
        pages.append({"route":route,"htmlBytes":len(html)})
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(fetch,path,"image/"):path for path in FILES}
        for future in as_completed(futures):
            payload=future.result()
            if len(payload)<1000:raise ValueError(futures[future]+": broken image")
    print(json.dumps({"status":"PRODUCTION-VERIFIED","site":BASE,"pages":pages,"imageUrlsChecked":len(FILES)}),flush=True)

for attempt in range(12):
    try:
        audit()
        break
    except Exception as error:
        print(f"Attempt {attempt+1}/12: {error}",flush=True)
        if attempt==11:raise
        time.sleep(5)
