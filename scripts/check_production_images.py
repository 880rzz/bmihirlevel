#!/usr/bin/env python3
"""Smoke-test live newsletter routes and their structured identity."""
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://hirlevel.magyariskola.at"
PAGES = {
    "/": ("hu", "https://hirlevel.magyariskola.at/"),
    "/de/": ("de", "https://hirlevel.magyariskola.at/de/"),
    "/en/": ("en", "https://hirlevel.magyariskola.at/en/"),
}
ALTERNATES = {
    "hu": "https://hirlevel.magyariskola.at/",
    "de": "https://hirlevel.magyariskola.at/de/",
    "en": "https://hirlevel.magyariskola.at/en/",
    "x-default": "https://hirlevel.magyariskola.at/",
}
SCHOOL = "https://www.wikidata.org/wiki/Q141274560"
MAGAZINE = "https://www.wikidata.org/wiki/Q142154314"
FOUNDER = "https://www.wikidata.org/wiki/Q56391118"


def request_page(route):
    request = Request(BASE + route, headers={"User-Agent": "BMI-Newsletter-Production-QA/1.0"})
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise ValueError(f"{route}: expected HTTP 200, got {response.status}")
        if "text/html" not in response.headers.get("Content-Type", "").lower():
            raise ValueError(f"{route}: response is not HTML")
        return response.geturl(), response.read().decode("utf-8")


def audit():
    results = []
    for route, (language, canonical) in PAGES.items():
        final_url, html = request_page(route)
        if final_url != canonical:
            raise ValueError(f"{route}: resolved to unexpected URL {final_url}")
        if f'<link rel="canonical" href="{canonical}">' not in html:
            raise ValueError(f"{route}: canonical link missing or incorrect")
        for locale, url in ALTERNATES.items():
            tag = f'<link rel="alternate" hreflang="{locale}" href="{url}">'
            if tag not in html:
                raise ValueError(f"{route}: hreflang {locale} missing or incorrect")
        scripts = re.findall(r'<script type="application/ld\\+json">(.*?)</script>', html, re.S)
        if len(scripts) != 1:
            raise ValueError(f"{route}: expected one JSON-LD block, found {len(scripts)}")
        schema = json.loads(scripts[0])
        if schema.get("@type") != "WebPage" or schema.get("inLanguage") != language:
            raise ValueError(f"{route}: WebPage type or language mismatch")
        if schema.get("publisher", {}).get("sameAs") != SCHOOL:
            raise ValueError(f"{route}: WebPage publisher must remain the Bécsi Magyar Iskola")
        periodical = schema.get("mentions", {})
        if periodical.get("@type") != "Periodical" or periodical.get("sameAs") != MAGAZINE:
            raise ValueError(f"{route}: Bécsi Szelet Periodical identity missing")
        founder = periodical.get("founder", {})
        if founder.get("@type") != "Person" or founder.get("sameAs") != FOUNDER:
            raise ValueError(f"{route}: Norbert Bánhalmi founder identity missing")
        results.append({"route": route, "resolvedUrl": final_url, "htmlBytes": len(html.encode("utf-8"))})
    print(json.dumps({"status": "PRODUCTION-VERIFIED", "site": BASE, "pages": results}), flush=True)


for attempt in range(3):
    try:
        audit()
        break
    except HTTPError as error:
        raise SystemExit(f"Definitive HTTP failure: {error}") from error
    except (URLError, TimeoutError, ConnectionError, ValueError, json.JSONDecodeError) as error:
        print(f"Attempt {attempt + 1}/3: {error}", flush=True)
        if attempt == 2:
            raise
        time.sleep(5)
