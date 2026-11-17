#!/usr/bin/env python3
"""Regression contract for the current 2026 BMI newsletter web pages and Wix email exports."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "index.html": "hu",
    "de/index.html": "de",
    "en/index.html": "en",
    "exports/bmi-hirlevel-wix-2026-10-18.html": "hu",
    "exports/bmi-hirlevel-wix-de-2026-10-18.html": "de",
    "exports/bmi-hirlevel-wix-en-2026-10-18.html": "en",
}
EVENT_LINKS = [
    "https://kultpult.eu/jazzjatszoter-becsben-des-andrassal-es-zenesztarsaival/",
    "https://www.magyariskola.at/event-details/ruhacsere-party-2026-osz",
    "https://www.kozpontiszovetseg.at/event-details/koncz-zsuzsa-becs",
    "https://www.magyariskola.at/event-details/taltos-dob-es-oromzene-schwedenplatz",
    "https://www.magyariskola.at/event-details/becsi-magyar-mikulas",
    "https://www.magyariskola.at/event-details/hangolodj-onmagadra",
    "https://www.magyariskola.at/event-details/kicsi-svung-bemutatja-narnia-nyomaban",
    "https://lilarum.at/veranstaltungsreihe/a-legcsinosabb-orias/",
    "https://www.stadthalle.com/de/events/alle-events/51539/Gospel-Christmas",
    "https://www.magyariskola.at/event-details/adventi-bazar-2026",
]
SECTION_OPEN = "<!-- Only requested Advent 2026 events -->"
SECTION_CLOSE = "<!-- /Only requested Advent 2026 events -->"

for path, lang in PAGES.items():
    html = (ROOT / path).read_text(encoding="utf-8")
    prefix = f"{path}: "
    is_export = path.startswith("exports/")
    assert len(html.encode("utf-8")) < 150000, prefix + "HTML exceeds 150 KB"
    assert f'<html lang="{lang}">' in html, prefix + "incorrect locale"
    assert len(re.findall(r"<h1\b", html)) == 1, prefix + "expected one H1"
    assert ("programajánló" in html.lower()
            or "programmempfehlungen" in html.lower()
            or "events guide" in html.lower()), prefix + "program guide identity missing"
    assert "halloween" not in html.lower(), prefix + "obsolete Halloween references"
    start, end = html.find(SECTION_OPEN), html.find(SECTION_CLOSE)
    assert 0 <= start < end, prefix + "missing event section boundaries"
    section = html[start:end]
    titles = re.findall(r"<h3[^>]*>(.*?)</h3>", section, re.S)
    assert len(titles) == 11, prefix + "expected eleven current event cards"
    expected_title_patterns = [
        r"(?i)(kandúr|gestiefelte|puss in boots)",
        r"(?i)jazz",
        r"(?i)(ruhacsere|kleidertausch|clothes swap)",
        r"(?i)(koncz|world turns|welt dreht)",
        r"(?i)(táltos|taltos)",
        r"(?i)hangolódj",
        r"(?i)(mikulás|nikolaus|hungarian santa)",
        r"(?i)narnia",
        r"(?i)(óriás|riese|giant)",
        r"(?i)gospel",
        r"(?i)(bazár|basar|bazaar)",
    ]
    for position, (title, pattern) in enumerate(zip(titles, expected_title_patterns), start=1):
        assert re.search(pattern, title), prefix + f"chronological event order incorrect at card {position}: {title}"
    if is_export:
        assert "margin:12px 28px" not in section, prefix + "music therapy/Narnia card outside Wix table row"
    assert "SPONTÁN" not in html and "darvasi" not in html.lower(), prefix + "removed events still present"
    assert "telapo-backstage-2025" not in html, prefix + "removed Santa recap still present"
    assert "https://shop.svung.at/show/8894" in section, prefix + "SVUNG tickets missing"
    for url in EVENT_LINKS:
        assert url in section, prefix + "missing event URL " + url
    assert ("december 9" in section.lower()
            or "9. Dezember" in section
            or "9 December" in section
            or "december 9." in section.lower()), prefix + "Gospel date missing"
    assert 'id="kozosseg"' in html, prefix + "community section missing"
    assert '#101F33' not in html.upper(), prefix + "obsolete palette"
    if is_export:
        browser_urls = {
            "hu": "https://hirlevel.magyariskola.at/",
            "de": "https://hirlevel.magyariskola.at/de/",
            "en": "https://hirlevel.magyariskola.at/en/",
        }
        localized_browser_labels = {"hu": "Megnyitás böngészőben",
                                    "de": "Im Browser öffnen",
                                    "en": "View in browser"}
        assert html.count('data-newsletter-utility="top"') == 1, prefix + "missing or duplicate top utility bar"
        assert html.count('<div data-newsletter-langs') == 1, prefix + "missing or duplicate language selector"
        assert html.count('data-newsletter-browser="true"') == 1, prefix + "browser link must appear exactly once"
        assert f'data-newsletter-browser="true" href="{browser_urls[lang]}"' in html, prefix + "incorrect browser URL"
        assert localized_browser_labels[lang] in html, prefix + "localized browser label missing"
        for locale, url in browser_urls.items():
            assert f'data-newsletter-locale="{locale}"' in html, prefix + f"missing {locale} switch"
            assert f'href="{url}"' in html, prefix + f"missing {locale} destination"
        assert len(re.findall(r'<a[^>]+aria-current="page"', html)) == 1, prefix + "expected one selected language link"
        assert (html.index('data-newsletter-utility="top"') <
                html.index('data-unsubscribe-request="email"')), prefix + "utility bar is not first"
        assert "<script" not in html.lower(), prefix + "email export contains script"
        assert 'data-unsubscribe-request="email"' in html, prefix + "email unsubscribe mechanism missing"
        assert 'data-event="svung-8894"' in section, prefix + "SVUNG export marker missing"
        assert ('UTOLSÓ 50 JEGY' in section or 'LETZTEN 50 TICKETS' in section
                or 'FINAL 50 TICKETS' in section), prefix + "Santa tickets notice missing"
        assert "IMG_7001.webp" in section, prefix + "current Santa event image missing"
        assert 'rel="canonical"' in html, prefix + "canonical missing"
        assert 'hreflang="x-default"' in html, prefix + "hreflang missing"
    else:
        canonical = {
            "index.html": "https://hirlevel.magyariskola.at/",
            "de/index.html": "https://hirlevel.magyariskola.at/de/",
            "en/index.html": "https://hirlevel.magyariskola.at/en/",
        }[path]
        assert f'<link rel="canonical" href="{canonical}">' in html, prefix + "canonical URL missing"
        alternates = {
            "hu": "https://hirlevel.magyariskola.at/",
            "de": "https://hirlevel.magyariskola.at/de/",
            "en": "https://hirlevel.magyariskola.at/en/",
            "x-default": "https://hirlevel.magyariskola.at/",
        }
        for locale, url in alternates.items():
            assert f'<link rel="alternate" hreflang="{locale}" href="{url}">' in html, prefix + f"hreflang {locale} missing"
        schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        assert schema_match, prefix + "JSON-LD script missing"
        schema = json.loads(schema_match.group(1))
        assert schema.get("@type") == "WebPage", prefix + "expected WebPage schema"
        assert schema.get("inLanguage") == lang, prefix + "JSON-LD locale mismatch"
        assert schema.get("publisher", {}).get("sameAs") == "https://www.wikidata.org/wiki/Q141274560", prefix + "school publisher identity mismatch"
        periodical = schema.get("mentions", {})
        assert periodical.get("@type") == "Periodical", prefix + "magazine must remain a Periodical mention"
        assert periodical.get("sameAs") == "https://www.wikidata.org/wiki/Q142154314", prefix + "magazine Wikidata identity mismatch"
        founders = periodical.get("founder", [])
        assert isinstance(founders, list) and len(founders) == 2, prefix + "both documented founders required"
        assert any(p.get("@type") == "Person" and p.get("@id") == "https://www.wikidata.org/wiki/Q56391118"
                   and p.get("name") == "Bánhalmi Norbert" for p in founders), prefix + "Norbert founder identity mismatch"
        assert any(p.get("@type") == "Person" and p.get("name") == "Kovács Attila"
                   for p in founders), prefix + "Kovács founder identity mismatch"
        assert periodical.get("publisher", {}).get("@id") == "https://www.kozpontiszovetseg.at/#organization", prefix + "magazine publisher mismatch"
        assert all(re.sub(r"[^a-z]", "", value.lower()) in html.lower() for value in (lang,)), prefix + "language marker missing"
        assert "https://www.becsiszelet.at/" in html, prefix + "permanent magazine recommendation missing"
        assert "https://www.wikidata.org/wiki/Q142154314" in html, prefix + "magazine entity JSON-LD missing"
        assert "https://www.wikidata.org/wiki/Q141274560" in html, prefix + "school entity JSON-LD missing"
        assert "<script" in html.lower(), prefix + "web page scripts missing"
        assert 'href="mailto:' in html, prefix + "unsubscription contact missing"
        assert "csizmas-kandur.webp" in section, prefix + "current Puss in Boots poster missing"
        assert 'class="josda"' in html, prefix + "web Ceridwen experience missing"
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert "User-agent: *" in robots and "Allow: /" in robots, "robots.txt must allow public crawling"
assert "Sitemap: https://hirlevel.magyariskola.at/sitemap.xml" in robots, "robots.txt sitemap declaration missing"
sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
sitemap_urls = {node.text for node in sitemap.findall(f".//{namespace}loc") if node.text}
expected_sitemap_urls = {
    "https://hirlevel.magyariskola.at/",
    "https://hirlevel.magyariskola.at/de/",
    "https://hirlevel.magyariskola.at/en/",
}
assert sitemap_urls == expected_sitemap_urls, "sitemap.xml must list each canonical newsletter URL exactly once"
print("BMI newsletter identity and current web/export contracts: 6/6 passed.")
