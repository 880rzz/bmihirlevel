# BMI hírlevél — 2026/27 · 7. hét · 7. kiadás

A Wix-hírlevélben használható reszponzív HTML-forrás: `index.html`.

## Tartalom
- Iskolai események: Csináljuk a forradalmat!, Ruhacsere Party, Bécsi Magyar Télapó.
- Télapó: az első héten a rendelkezésre álló jegyek közel fele elkelt (szerkesztőségi adat).
- Bécsi programajánló **16 eseménnyel, négy kategóriában**: magyar programok, gyerekek és családok, Halloween, felnőttek és nagyobb fiatalok.
- Két elérhető önálló BMI-felület: https://programvalaszto.magyariskola.at/ és https://tanarok.magyariskola.at/.
- Megmaradt: Szülői Közösség, Kisbarát kereső, leiratkozás: marketing@kozpontiszovetseg.at; explicit beleegyezéshez kötött GA4 script.

## Esemény- és forrásnapló
- `data/programajanlo-2026-10-18.json` tartalmazza a kategóriákat, az események szervezői URL-jeit, az ellenőrzési dátumot és a DORAPP rekordazonosítóit.
- Az ausztriai magyar események forrása a [DORAPP](https://github.com/880rzz/DORAPP) `data/events.json` fájl.
- A Halloween, bécsi családi és nemzetközi kulturális programok forrása a város vagy az esemény szervezője.
- A magyar vonatkozás nem igazolja automatikusan a program magyar nyelvét; a belépő, a korhatár és a szabad férőhely kiküldés előtt újból ellenőrizendő.

## Archívumok — ne módosítsd
- **`archive/2026-10-18-pre-week07.html`**: a 7. hírlevél előtti régi kezdőfájl, a Táltos dob videójával. A novemberi Táltos dob hírlevélhez őrizendő.
- `archive/2026-10-18-week07-before-categories.html`: a 7. hét első kiadásának változatlan másolata a kategóriás bővítés előtt.
- `archive/2026-10-01.html`: korábbi kiadás.
- `assets/og/2026-10-01.jpg`: korábbi kiadás OG-képe.

## Reszponzivitás és ellenőrzés
- Maximális levélszélesség 620 px, mobil CSS és inline levélstílusok.
- Kategóriaugrások hagyományos HTML-horgonyokkal; a külső oldalak abszolút URL-ek. A támogatás levelezőkliens-függő.
- Az Ősztündér és a Táltos dob nem szerepel az aktuális kezdőlapon.
- Dátum, részvételi feltétel, regisztráció és elérhetőség ellenőrzendő kiküldés előtt.
