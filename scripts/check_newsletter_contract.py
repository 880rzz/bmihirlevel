#!/usr/bin/env python3
"""Regression contract for the Advent 2026 BMI newsletter and Wix exports."""
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
    "https://www.magyariskola.at/event-details/taltos-dob-es-oromzene-schwedenplatz",
    "https://www.magyariskola.at/event-details/becsi-magyar-mikulas",
    "https://lilarum.at/veranstaltungsreihe/a-legcsinosabb-orias/",
    "https://www.becsiszelet.at/post/gospel-christmas-becs-stadthalle-2026",
]
EVENT_TITLES = ("SPONT", "Jazz", "Ruhacsere", "Koncz", "Táltos", "Mikul", "Advent", "óriás", "Gospel")
for path, lang in PAGES.items():
    html = (ROOT / path).read_text(encoding="utf-8")
    prefix = f"{path}: "
    assert len(html.encode("utf-8")) < 150000, prefix + "HTML exceeds 150 KB"
    assert f'<html lang="{lang}">' in html, prefix + "incorrect locale"
    assert len(re.findall(r"<h1\\b", html)) == 1, prefix + "expected one H1"
    start = html.find("<!-- Only requested Advent 2026 events -->")
    end = html.find("<!-- /Only requested Advent 2026 events -->")
    assert 0 <= start < end, prefix + "missing event section boundaries"
    section = html[start:end]
    assert len(re.findall(r"<h3\\b", section)) == 9, prefix + "expected nine event cards"
    for name in EVENT_TITLES:
        assert name.lower() in section.lower(), prefix + "missing event " + name
    for url in EVENT_LINKS:
        assert url in section, prefix + "missing event URL " + url
    assert "2026" in section and "december 9" in section.lower() or (
        "2026" in section and ("9. Dezember" in section or "9 December" in section)
    ), prefix + "missing Gospel date"
    assert 'id="kozosseg"' in html, prefix + "BMI community section missing"
    assert 'data-unsubscribe-request="email"' in html, prefix + "unsubscribe missing"
    assert "halloween" not in html.lower(), prefix + "obsolete Halloween references"
    if path.startswith("exports/"):
        assert "<script" not in html.lower(), prefix + "email export contains JS"
    else:
        assert 'rel="canonical"' in html, prefix + "canonical missing"
        assert 'hreflang="x-default"' in html, prefix + "hreflang missing"
print("Advent newsletter contract: 6/6 pages passed.")
