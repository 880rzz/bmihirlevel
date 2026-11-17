#!/usr/bin/env python3
"""Check the newsletter HU/EN/DE schema without changing the editorial payload."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
bmi = "https://www.magyariskola.at/#organization"
fed = "https://www.kozpontiszovetseg.at/#organization"
person = "https://www.wikidata.org/wiki/Q56391118"
magazine = "https://www.becsiszelet.at/#periodical"
for path, lang in (("index.html", "hu"), ("en/index.html", "en"), ("de/index.html", "de")):
    data = (root / path).read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', data)
    assert len(blocks) == 1, f"{path}: expected one structured-data script"
    obj = json.loads(blocks[0])
    assert obj["@type"] == "WebPage" and obj["inLanguage"] == lang
    assert obj["publisher"]["@id"] == bmi
    assert obj["publisher"]["parentOrganization"]["@id"] == fed
    assert obj["isPartOf"]["publisher"]["@id"] == bmi
    assert obj["mentions"]["@id"] == magazine
    assert obj["mentions"]["publisher"]["@id"] == fed
    founders = obj["mentions"]["founder"]
    assert len(founders) == 2
    assert any(x.get("@id") == person for x in founders)
    assert any(x.get("name") == "Kovács Attila" for x in founders)
    assert obj["mentions"]["subjectOf"]["@id"] == "https://okoszisztema.kozpontiszovetseg.at/forrasok/#catalog"
print("PASS: HU/EN/DE newsletter entity IDs, publisher, project and magazine founders.")
