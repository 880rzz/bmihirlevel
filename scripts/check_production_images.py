#!/usr/bin/env python3
"""Smoke-test published newsletter routes, crawl files, and entity schema."""
import json
import re
import time
import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class DeploymentPending(Exception):
    """Pages content has not reached the public edge yet."""


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
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def request_resource(route):
    request = Request(BASE + route, headers={"User-Agent": "BMI-Newsletter-Production-QA/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise ValueError(f"{route}: expected HTTP 200, got {response.status}")
            return response.geturl(), response.headers.get("Content-Type", "").lower(), response.read()
    except HTTPError as error:
        if error.code == 404 and route in {"/robots.txt", "/sitemap.xml"}:
            raise DeploymentPending(f"{route}: new crawl file is not deployed yet") from error
        raise


def audit():
    results = []
    for route, (language, canonical) in PAGES.items():
        final_url, content_type, raw = request_resource(route)
        html = raw.decode("utf-8")
        if final_url != canonical:
            raise ValueError(f"{route}: resolved to unexpected URL {final_url}")
        if "text/html" not in content_type:
            raise ValueError(f"{route}: response is not HTML")
        if f'<link rel="canonical" href="{canonical}">' not in html:
            raise DeploymentPending(f"{route}: canonical link is not at the public edge yet")
        for locale, url in ALTERNATES.items():
            if f'<link rel="alternate" hreflang="{locale}" href="{url}">' not in html:
                raise DeploymentPending(f"{route}: hreflang {locale} is not at the public edge yet")
        scripts = re.findall(r'<script type="application/ld[+]json">(.*?)</script>', html, re.S)
        if len(scripts) != 1:
            raise DeploymentPending(f"{route}: expected one JSON-LD block, found {len(scripts)}")
        schema = json.loads(scripts[0])
        if schema.get("@type") != "WebPage" or schema.get("inLanguage") != language:
            raise DeploymentPending(f"{route}: WebPage type or language is not current")
        if schema.get("publisher", {}).get("sameAs") != SCHOOL:
            raise DeploymentPending(f"{route}: Bécsi Magyar Iskola publisher identity is missing")
        periodical = schema.get("mentions", {})
        if periodical.get("@type") != "Periodical" or periodical.get("sameAs") != MAGAZINE:
            raise DeploymentPending(f"{route}: Bécsi Szelet Periodical identity is missing")
        founder = periodical.get("founder", {})
        if founder.get("@type") != "Person" or founder.get("sameAs") != FOUNDER:
            raise DeploymentPending(f"{route}: founder Wikidata identity is missing")
        results.append({"route": route, "resolvedUrl": final_url, "htmlBytes": len(raw)})

    robots_url, robots_type, robots_raw = request_resource("/robots.txt")
    robots = robots_raw.decode("utf-8")
    if robots_url != BASE + "/robots.txt" or "text/plain" not in robots_type:
        raise ValueError("robots.txt did not resolve as the expected text file")
    if "User-agent: *" not in robots or "Allow: /" not in robots:
        raise DeploymentPending("robots.txt crawl directives are not current")
    if f"Sitemap: {BASE}/sitemap.xml" not in robots.splitlines():
        raise DeploymentPending("robots.txt sitemap declaration is not current")

    sitemap_url, sitemap_type, sitemap_raw = request_resource("/sitemap.xml")
    if sitemap_url != BASE + "/sitemap.xml" or "xml" not in sitemap_type:
        raise ValueError("sitemap.xml did not resolve as XML")
    sitemap = ET.fromstring(sitemap_raw)
    listed_urls = {node.text for node in sitemap.findall(f".//{SITEMAP_NS}loc") if node.text}
    expected_urls = {canonical for _, canonical in PAGES.values()}
    if listed_urls != expected_urls:
        raise DeploymentPending("sitemap.xml does not yet list all three canonical newsletter URLs")

    print(json.dumps({
        "status": "PRODUCTION-VERIFIED",
        "site": BASE,
        "pages": results,
        "robots": robots_url,
        "sitemap": sitemap_url,
    }), flush=True)


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
