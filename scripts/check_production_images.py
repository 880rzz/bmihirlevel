#!/usr/bin/env python3
"""Smoke-test live newsletter routes and their structured identity."""
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

class DeploymentPending(Exception):
    """Pages build is complete but its current HTML has not reached the public edge yet."""


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
            raise DeploymentPending(f"{route}: canonical link missing or incorrect")
        for locale, url in ALTERNATES.items():
            tag = f'<link rel="alternate" hreflang="{locale}" href="{url}">'
            if tag not in html:
                raise DeploymentPending(f"{route}: hreflang {locale} missing or incorrect")
        scripts = re.findall(r'<script type="application/ld[+]json">(.*?)</script>', html, re.S)
        if len(scripts) != 1:
            raise DeploymentPending(f"{route}: expected one JSON-LD block, found {len(scripts)}")
        schema = json.loads(scripts[0])
        if schema.get("@type") != "WebPage" or schema.get("inLanguage") != language:
            raise DeploymentPending(f"{route}: WebPage type or language mismatch")
        if schema.get("publisher", {}).get("sameAs") != SCHOOL:
            raise DeploymentPending(f"{route}: WebPage publisher must remain the Bécsi Magyar Iskola")
        periodical = schema.get("mentions", {})
        if periodical.get("@type") != "Periodical" or periodical.get("sameAs") != MAGAZINE:
            raise DeploymentPending(f"{route}: Bécsi Szelet Periodical identity missing")
        founder = periodical.get("founder", {})
        if founder.get("@type") != "Person" or founder.get("sameAs") != FOUNDER:
            raise DeploymentPending(f"{route}: Norbert Bánhalmi founder identity missing")
        results.append({"route": route, "resolvedUrl": final_url, "htmlBytes": len(html.encode("utf-8"))})
    print(json.dumps({"status": "PRODUCTION-VERIFIED", "site": BASE, "pages": results}), flush=True)


last_error = None
for attempt in range(12):
    try:
        audit()
        break
    except DeploymentPending as error:
        last_error = error
        print(f"Attempt {attempt + 1}/12: Pages content is still propagating: {error}", flush=True)
    except HTTPError as error:
        if error.code not in {500, 502, 503, 504}:
            raise SystemExit(f"Definitive HTTP failure: {error}") from error
        last_error = error
        print(f"Attempt {attempt + 1}/12: transient HTTP {error.code}", flush=True)
    except (URLError, TimeoutError, ConnectionError) as error:
        last_error = error
        print(f"Attempt {attempt + 1}/12: transient network error: {error}", flush=True)
    if attempt == 11:
        raise SystemExit(f"Production verification did not converge after Pages deployment: {last_error}")
    time.sleep(5)
