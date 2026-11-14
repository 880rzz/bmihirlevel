#!/usr/bin/env python3
"""Regression contract for the current 2026 BMI newsletter web pages and Wix email exports."""
from pathlib import Path
import re

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
    "https://exhibition.vipach.at",
    "https://kultpult.eu/jazzjatszoter-becsben-des-andrassal-es-zenesztarsaival/",
    "https://www.magyariskola.at/event-details/ruhacsere-party-2026-osz",
    "https://www.kozpontiszovetseg.at/event-details/koncz-zsuzsa-becs",
    "https://www.magyariskola.at/event-details/taltos-dob-es-oromzene-schwedenplatz",
    "https://www.magyariskola.at/event-details/becsi-magyar-mikulas",
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
    assert len(re.findall(r"<h1\\b", html)) == 1, prefix + "expected one H1"
    assert ("programajánló" in html.lower()
            or "programmempfehlungen" in html.lower()
            or "events guide" in html.lower()), prefix + "program guide identity missing"
    assert "halloween" not in html.lower(), prefix + "obsolete Halloween references"
    start, end = html.find(SECTION_OPEN), html.find(SECTION_CLOSE)
    assert 0 <= start < end, prefix + "missing event section boundaries"
    section = html[start:end]
    titles = re.findall(r"<h3[^>]*>(.*?)</h3>", section, re.S)
    assert len(titles) == 13, prefix + "expected thirteen current event cards"
    assert "Jazz" in titles[-2] and "Gospel Christmas" in titles[-1], prefix + "Jazz/Gospel ordering"
    assert "https://www.kozpontiszovetseg.at/event-details/darvasi-laszlo" in section, prefix + "Darvasi event missing"
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
        assert "<script" not in html.lower(), prefix + "email export contains script"
        assert 'data-unsubscribe-request="email"' in html, prefix + "email unsubscribe mechanism missing"
        assert 'data-event="darvasi-laszlo-2026"' in section, prefix + "Darvasi export marker missing"
        assert 'data-event="svung-8894"' in section, prefix + "SVUNG export marker missing"
        assert ('UTOLSÓ 50 JEGY' in section or 'LETZTEN 50 TICKETS' in section
                or 'FINAL 50 TICKETS' in section), prefix + "Santa tickets notice missing"
        assert 'data-event-recap="telapo-backstage-2025"' in html, prefix + "Santa recap missing"
        assert 'data-event-recap-image="telapo-backstage-2025"' in html, prefix + "recap image missing"
        assert "IMG_6998.jpeg" in html and "IMG_7001.webp" in section, prefix + "export images missing"
        assert 'rel="canonical"' in html, prefix + "canonical missing"
        assert 'hreflang="x-default"' in html, prefix + "hreflang missing"
    else:
        assert "https://www.becsiszelet.at/" in html, prefix + "permanent magazine recommendation missing"
        assert "https://www.wikidata.org/wiki/Q142154314" in html, prefix + "magazine entity JSON-LD missing"
        assert "https://www.wikidata.org/wiki/Q141274560" in html, prefix + "school entity JSON-LD missing"
        assert "<script" in html.lower(), prefix + "web page scripts missing"
        assert 'href="mailto:' in html, prefix + "unsubscription contact missing"
        assert "csizmas-kandur.webp" in section, prefix + "current Puss in Boots poster missing"
        assert 'class="josda"' in html, prefix + "web Ceridwen experience missing"
print("BMI newsletter identity and current web/export contracts: 6/6 passed.")
