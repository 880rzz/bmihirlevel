#!/usr/bin/env python3
"""Offline regression contract for the static BMI newsletter and its Wix exports."""
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
POSTERS = ("h1956", "hdarvasi", "hkoncz")
for path, lang in PAGES.items():
    html = (ROOT / path).read_text(encoding="utf-8")
    assert len(html.encode("utf-8")) < 150000, f"{path}: editorial HTML exceeds 150 KB"
    assert html.count("<h1 ") == 1, f"{path}: expected exactly one H1"
    assert html.count('data-event-thumb="traume"') == 1, f"{path}: duplicate TRÄUME event"
    assert 'data-newsletter-subscription="top"' not in html, f"{path}: unwanted top subscription CTA"
    assert html.count('data-newsletter-subscription="bottom"') == 1, f"{path}: bottom subscription CTA missing"
    assert html.count("https://magyariskola.at/#feliratkozas") == 1, f"{path}: incorrect subscription target"
    assert html.count('class="event-editorial-details"') == 18, f"{path}: editorial event parity broken"
    assert html.count('class="event-school-details"') == 2, f"{path}: school event panels missing"
    assert 'data-event="napraforgok-2026"' in html, f"{path}: missing 20th event"
    assert 'data-unsubscribe-request="email"' in html, f"{path}: unsubscribe missing"
    assert "mailto:marketing@kozpontiszovetseg.at?" in html
    assert f'<html lang="{lang}">' in html
    assert "newsletter-content-de" not in html and "newsletter-content-en" not in html
    for poster in POSTERS:
        images = re.findall(r'<img\b[^>]*src="[^"]*/' + poster + r'-640\.(?:jpg|webp)"[^>]*>', html)
        assert len(images) == 1, f"{path}: {poster} missing or duplicated"
        assert "aspect-ratio:1/1" in images[0], f"{path}: {poster} not square"
    assert html.count('data-newsletter-locale=') == 2, f"{path}: language navigation"
    if not path.startswith("exports/"):
        assert html.count('id="ceridwen-invite"') == 1, f"{path}: Ceridwen launcher missing"
        assert 'href="https://www.helloits.me/"' in html, f"{path}: app link missing"
        assert 'aria-expanded="false"' in html, f"{path}: trigger state missing"
        assert 'min-height:44px' in html, f"{path}: mobile touch target missing"
    if path.startswith("exports/"):
        assert "<script" not in html, f"{path}: email must not contain JS"
    else:
        assert html.count('loading="lazy"') >= 16, f"{path}: below-fold images should be lazy"
print("Newsletter regression: 6/6 pages passed.")
