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
THEME_ASSETS=["/assets/halloween/night-pattern.svg","/assets/halloween/pumpkin.svg","/assets/halloween/bat.svg","/assets/halloween/moon.svg"]

def fetch(path,expected):
    url=urljoin(BASE,path)
    with urlopen(Request(url,headers={"User-Agent":"BMI-Newsletter-Production-QA/1.0"}),timeout=12) as response:
        if response.status!=200:raise ValueError(f"{url}: HTTP {response.status}")
        mime=response.headers.get("Content-Type","").lower()
        raw=response.read()
        if expected not in mime:raise ValueError(f"{url}: expected {expected}, got {mime}")
        if len(raw)<100:raise ValueError(f"{url}: response too small")
        return raw

def class_count(html,name):
    return sum(name in value.split() for value in re.findall(r'class="([^"]*)"',html))

def audit():
    pages=[]
    for route in ROUTES:
        html=fetch(route,"text/html").decode("utf-8")
        if "/assets/bmi-logo-272.webp" not in html:raise ValueError(route+": BMI logo not local")
        for id in IDS:
            if id != "u4" and f"/assets/events/{id}-640.webp" not in html:raise ValueError(route+": missing "+id)
        if "night-pattern.svg" not in html:raise ValueError(route+": Halloween night wallpaper not deployed")
        if 'data-unsubscribe-request="email"' not in html:raise ValueError(route+": unsubscribe control missing")
        if "halloween-pumpkin" not in html:raise ValueError(route+": seasonal card icons missing")
        # Ensure the deployed site contains the actual requested editorial design.
        if class_count(html,"category-buttons")<1:raise ValueError(route+": compact category buttons not deployed")
        expected_features=3
        expected_events=18
        if class_count(html,"feature-cell")!=expected_features:raise ValueError(route+": category cards missing")
        if class_count(html,"editorial-event")!=expected_events:raise ValueError(route+": editorial event cards missing")
        if html.count('data-event-thumb="traume"')!=1:raise ValueError(route+": TRÄUME repeated")
        if 'id="bmi-sticky-categories"' not in html:raise ValueError(route+": sticky category navigation missing")
        if 'id="ceridwen-invite"' not in html or 'class="cer-trigger cer-figure"' not in html:raise ValueError(route+": Jósda figure is not live")
        if '<span class="cer-name">Jósda</span>' not in html or 'https://www.helloits.me/' not in html:raise ValueError(route+": Jósda label or app link missing")
        if "BlinkMacSystemFont" not in html or "font-family:Georgia" not in html:raise ValueError(route+": premium typography not deployed")
        if "border:1px solid #C8A76D" not in html:raise ValueError(route+": gold 1px button border missing")
        expected_school=2 if route=="/" else 0
        if class_count(html,"school-event-image")!=expected_school:raise ValueError(route+": unified school cards missing")
        if html.count("aspect-ratio:1/1")<expected_school:raise ValueError(route+": square school images missing")
        expected_telapo=1
        if html.count('data-event="bmi-telapo"')!=expected_telapo:raise ValueError(route+": St Nicholas event not moved to children section")
        titles={"/":"Bécsi Programajánló","/de/":"Wiener Programmtipps","/en/":"Vienna Event Guide"}
        if titles[route] not in html:raise ValueError(route+": Vienna guide title not deployed")
        child_counts={"/":"01 · 9 program","/de/":"01 · 9 Veranstaltungen","/en/":"01 · 9 events"}
        if child_counts[route] not in html:raise ValueError(route+": children event count not updated")
        if "#C82932" in html or "#B82029" in html:raise ValueError(route+": old burgundy accent remains")
        if re.search(r'<img\b[^>]*src="https://static\.wixstatic\.com/',html):raise ValueError(route+": unresolved Wix source")
        pages.append({"route":route,"htmlBytes":len(html)})
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(fetch,path,"image/"):path for path in FILES}
        for future in as_completed(futures):
            payload=future.result()
            if len(payload)<1000:raise ValueError(futures[future]+": broken image")
    for path in THEME_ASSETS:
        fetch(path,"image/svg+xml")
    print(json.dumps({"status":"PRODUCTION-VERIFIED","site":BASE,"pages":pages,"imageUrlsChecked":len(FILES)}),flush=True)

for attempt in range(12):
    try:
        audit()
        break
    except Exception as error:
        print(f"Attempt {attempt+1}/12: {error}",flush=True)
        if attempt==11:raise
        time.sleep(5)
