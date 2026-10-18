# BMI hírlevél — 2026/27 · 7. hét · 7. kiadás

A Wix-hírlevélben használható reszponzív HTML-forrás: `index.html`.

## Tartalom
- Iskolai események: Csináljuk a forradalmat!, Ruhacsere Party, Bécsi Magyar Télapó.
- Télapó: az első héten a rendelkezésre álló jegyek közel fele elkelt (szerkesztőségi adat).
- **Három fő belépési pont a kezdőlapon:** Bécsi gyerekprogramok (8), Felnőtt programok (8), Bécsi Magyar Iskolai programok (3). A Halloween és a magyar kulturális események az adott közönség kategóriáján belül szerepelnek.
- Két elérhető önálló BMI-felület: https://programvalaszto.magyariskola.at/ és https://tanarok.magyariskola.at/.
- Megmaradt: Szülői Közösség, Kisbarát kereső, leiratkozás: marketing@kozpontiszovetseg.at; explicit beleegyezéshez kötött GA4 script.

## Esemény- és forrásnapló
- `data/programajanlo-2026-10-18.json` a három fő kategória és a 19 esemény központi nyilvántartása, DORAPP-rekordazonosítókkal és forráslinkekkel.
- Az ausztriai magyar események forrása a [DORAPP](https://github.com/880rzz/DORAPP) `data/events.json` fájl.
- A Halloween, bécsi családi és nemzetközi kulturális programok forrása a város vagy az esemény szervezője.
- A magyar vonatkozás nem igazolja automatikusan a program magyar nyelvét; a belépő, a korhatár és a szabad férőhely kiküldés előtt újból ellenőrizendő.

## Archívumok — ne módosítsd
- **`archive/2026-10-18-pre-week07.html`**: a 7. hírlevél előtti régi kezdőfájl, a Táltos dob videójával. A novemberi Táltos dob hírlevélhez őrizendő.
- `archive/2026-10-18-week07-before-categories.html`: a 7. hét első, bécsi programajánlóval bővített kiadása.
- `archive/2026-10-18-week07-before-three-entry-structure.html`: a korábbi négy kategóriás elrendezés teljes másolata.
- `archive/2026-10-01.html`: korábbi kiadás.
- `assets/og/2026-10-01.jpg`: korábbi kiadás OG-képe.

## Reszponzivitás és ellenőrzés
- Maximális levélszélesség 620 px, mobil CSS és inline levélstílusok.
- Mindhárom fő kategória az első tartalmi képernyőn, rövid leírással és közvetlen HTML-horgonyos navigációval. Levelezőkliens-függő horgonytámogatás; a tartalom mindig közvetlenül olvasható.
- Az Ősztündér és a Táltos dob nem szerepel az aktuális kezdőlapon.
- Dátum, részvételi feltétel, regisztráció és elérhetőség ellenőrzendő kiküldés előtt.

## First-principles információarchitektúra

- Kérdés: Kinek keresek programot? Válasz: **gyerekek / felnőttek / az iskola programjai**.
- Nincs külön magyar és Halloween főmenü, mert a célcsoport szerinti döntést zavarták.
- 3 fő csoport → közvetlen részletek → a szervező hivatalos oldala. Az új részletes eseménylista egyszer szerepelteti az egyes eseményeket.
- Hírréteg: Mikulás-jegyértékesítés röviden a 3 belépési pont alatt. Teljes részletek az iskolai kategóriában.
- A korábbi nagy iskolai képgalériát egyetlen, kisebb Télapó-képre redukáltuk; a többi esemény linkje és tartalma megmaradt.

## BMI iskolai programegység megőrzött stílusa (2026-10-18)

A háromkategóriás kezdőlap változatlan. A `#program-iskola` blokk az archivált `archive/2026-10-18-week07-before-three-entry-structure.html` kiadás eredeti iskolai megjelenéséből lett visszaállítva: nagyméretű programképek, hosszabb leírások, az eredeti jelentkezési gombok és a Télapó Pingvintánc-linkje. Mobilon a táblázatcellák oldalsó paddingje a meglévő közös szabályt követi. A többi programkategória nem változott.
