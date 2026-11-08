#!/usr/bin/env python3
"""Regression contract for the Autumn-Winter 2026 BMI newsletter and Wix exports."""
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
for path, lang in PAGES.items():
    html = (ROOT / path).read_text(encoding="utf-8")
    prefix = f"{path}: "
    assert len(html.encode("utf-8")) < 150000, prefix + "HTML exceeds 150 KB"
    assert f'<html lang="{lang}">' in html, prefix + "incorrect locale"
    assert len(re.findall(r"<h1\b", html)) == 1, prefix + "expected one H1"
    start = html.find("<!-- Only requested Advent 2026 events -->")
    end = html.find("<!-- /Only requested Advent 2026 events -->")
    assert 0 <= start < end, prefix + "missing event section boundaries"
    section = html[start:end]
    assert len(re.findall(r"<h3\b", section)) == 10, prefix + "expected ten event cards"
    assert 'data-event="svung-8894"' in section, prefix + "SVUNG event missing"
    assert "https://shop.svung.at/show/8894" in section, prefix + "SVUNG ticket link missing"
    assert ("UTOLSÓ 50 JEGY" in section or "LETZTEN 50 TICKETS" in section or "FINAL 50 TICKETS" in section), prefix + "Santa ticket notice missing"
    for url in EVENT_LINKS:
        assert url in section, prefix + "missing event URL " + url
    assert "2026" in section and "december 9" in section.lower() or (
        "2026" in section and ("9. Dezember" in section or "9 December" in section)
    ), prefix + "missing Gospel date"
    assert 'id="kozosseg"' in html, prefix + "BMI community section missing"
    assert 'data-unsubscribe-request="email"' in html, prefix + "unsubscribe missing"
    assert "halloween" not in html.lower(), prefix + "obsolete Halloween references"
    assert "ceridwen-invite" in html.lower() and "helloits.me" in html.lower(), prefix + "Jósda/Ceridwen integration missing"
    assert ("Őszi és téli programok" in html or "Herbst- und Winterprogramme" in html or "Autumn and winter programmes" in html), prefix + "autumn-winter heading missing"
    assert 'data-event-recap="telapo-backstage-2025"' in html, prefix + "Santa backstage recap missing"
    assert 'data-event-recap-image="telapo-backstage-2025"' in html, prefix + "square backstage image missing"
    assert "IMG_6998.jpeg" in html, prefix + "uploaded image reference missing"
    assert 'data-event-recap="osztunder-2026"' not in html, prefix + "obsolete autumn recap remains"
    assert "#A61920" in html and "#FBF6F0" in html, prefix + "new palette missing"
    for obsolete_color in ("#101F33", "#17283D", "#F5F3EE"):
        assert obsolete_color.upper() not in html.upper(), prefix + "obsolete dark color remains: " + obsolete_color
    if path.startswith("exports/"):
        assert "<script" not in html.lower(), prefix + "email export contains JS"
    else:
        assert 'rel="canonical"' in html, prefix + "canonical missing"
        assert 'hreflang="x-default"' in html, prefix + "hreflang missing"
print("Autumn-Winter newsletter contract: 6/6 pages passed.")
