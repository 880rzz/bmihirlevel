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

## BMI embléma a hírlevél elején

- A feltöltött `bmi_blue_round_rgb_logo.svg` alapján email-kompatibilis, 420×426 px, átlátszó PNG készült. Az eredeti SVG nagy (8,4 MB), mert beágyazott rasterképet tartalmaz; ezért nem azt töltjük be a hírlevélből.
- Hivatalos BMI Wix média URL: `https://static.wixstatic.com/media/b0aee1_944db6e866844c83b2e5d8b7bdf7ecb6~mv2.png` (kép feltöltve 2026-10-18, a Wix visszajelzése: PENDING).
- A logo közvetlenül a fejléc előtt, fehér háttérrel és 136 px látható szélességgel jelenik meg; a képre kattintva a hivatalos iskolai honlapra jut az olvasó.
- A fejléc, kategóriák és a három eredeti iskolai program vizuális része nem változott. Éles CDN és GitHub Pages ellenőrzés szükséges a végleges production lezáráshoz.

## Háromnyelvű hírlevél és nyelvválasztó (2026-10-18)

- **Magyar:** https://hirlevel.magyariskola.at/ – `index.html`
- **Német:** https://hirlevel.magyariskola.at/de/ – `de/index.html`
- **Angol:** https://hirlevel.magyariskola.at/en/ – `en/index.html`
- A kódoldali hírlevél nyelvválasztó három normál HTTPS linkkel működik; e-mailben nem függ JavaScripttől és mindig a teljes adott nyelvű online oldalra mutat.
- Az egyes nyelvek külön canonical és hreflang kapcsolatokkal rendelkeznek. Az online EN/DE változat az analitikát a webhely gyökeréről tölti.
- Wix Email Marketing import: `exports/bmi-hirlevel-wix-2026-10-18.html` (HU), `exports/bmi-hirlevel-wix-de-2026-10-18.html` (DE), `exports/bmi-hirlevel-wix-en-2026-10-18.html` (EN).
- Az e-mail HTML fájlokból hiányzik a JavaScript és a saját leiratkozási felszólítás; Wix biztosítja a natív leiratkozást. Mindhárom változat azonos 19 programot, BMI-képeket, külső linkeket és a 3 célcsoportot használja.
- Egy magyar vonatkozású program nem feltétlenül magyar nyelvű. Fordításkor eseménycímek (különösen saját márkanevek) és forráslinkek megmaradnak, a kísérőszöveg DE/EN nyelvű. A dátumok a 2026-10-18-i hírlevél pillanatképét jelentik.

## Egylapos háromnyelvű nyelvválasztó (2026-10-18)

- A webes gyökéroldal (`index.html`) alapnyelve magyar, és tartalmazza a teljes DE/EN verziót két inaktív HTML `template` blokkban. A nyelvváltás kattintásra ugyanazon az oldalon, újratöltés nélkül történik, és `?lang=de` / `?lang=en` megosztható URL-re frissíti a címsort.
- A három nyelvikon: 🇭🇺 Magyar · 🇦🇹 Deutsch · 🇬🇧 English. Az aktív nyelv vizuálisan jelölt. A választás az oldalcímet és a nyelvi metaadatokat is frissíti, a magyar alapértelmezés mellett.
- A `de/index.html` és `en/index.html` külön nyelvű kanonikus oldalak továbbra is rendelkezésre állnak SEO/hreflang és JavaScript nélküli eszközök számára.
- A Wix e-mail HTML-ekbe **nem** kerül interaktív JavaScript; az ikonok a nyelvnek megfelelő teljes online hírlevélre linkelnek. A forrás tartalma és képei mindhárom kiadásban változatlanok.
- A levelezőkliensek JS-tiltása miatt kizárólag a webes online verzió kapcsol át a három nyelv között helyben. A Wix-export HTML-változatok külön is megtarthatók.

## Optimalizált eseményképek és 5 px sarokkerekítés (2026-10-18)

- A 16 külső eseményből **14** kapott a szervezői oldalhoz vagy témához köthető fotót; **2** programnál nincs hitelesen társítható közvetlen médiaforrás (1956-os bécsi közös megemlékezés és U4 Halloween). Az eredeti **3 BMI-eseménykép maradt**, és sarokkerekítésük 10 → **5 px**.
- Az új képek eredetije és dátuma a `data/programajanlo-2026-10-18.json` `image` mezőjében van nyilvántartva. Az archív/témakép szerkesztőségi képaláírást kap, ezért nem látszik 2026-os eseményen készült felvételnek.
- Képek: Wix Media CDN, 480 × 270 px JPEG transzformáció, `q_65`, max. 300 px vizuális szélesség, 5 px radius, deklarált 300 × 169 megjelenítési méret. Az online verzió lusta képletöltést és aszinkron dekódolást használ; a három Wix e-mail export JS-mentes és a képeket e-mailbarát `img` elemekkel jeleníti meg.
- A három nyelv azonos 14 külső képhez csatlakozik; böngésző gyorsítótára megosztja a képek letöltését. A két kép nélküli programnál nem került be hamis vagy félrevezető kép.
- **Release-korlát:** a Wix médiaszolgáltatás feltöltéskor `PENDING` státuszt jelentett. A végleges CDN-válasz és a tényleges teljesítmény/fájlméret külső eszközzel nem ellenőrzött. **A szerzői jogi / felhasználási engedély nem igazolt**, különösen a harmadik fél által publikált sajtó-/archív fotóknál. A képek nyilvános közzététele és a Wix-kiküldés előtt jogosultsági ellenőrzés szükséges.

- **Adatjavítás:** a három eredeti BMI-programképet a képadatbázis `EXISTING_OWN_EVENT_ARTWORK` státusszal kezeli. A kizárólag két kép nélküli külső esemény: 1956-os megemlékezés és U4 Halloween.

## Teljes vizuális lefedettség: 19/19 (2026-10-18, kiegészítés)

- A két utolsó külső eseményhez külön **szimbólumot** illesztettünk a már meglevő 14 fotó mellé. Az 1956-os közös megemlékezés jelölője Thommy9 1956-os lyukas zászlója (**CC0**, nem rendezvényfotó); az U4 Halloween jelölője az U4 helyszín logója (**nem a 2026-os esemény plakátja**). A forrás és státusz a JSON-ben szerepel.
- Most minden eseménynek van vizuális eleme: **16 külső ajánló (14 archív/illusztratív/aktuális fotó + 2 jelképes), 3 BMI eredeti eseménykép**. A korábbi 14/16 és két kép nélküli sor a korábbi végrehajtási szakasz állapotát jelölte.
- Mind a 19 eseményképnél 5 px sarokkerekítés érvényes; a kör alakú BMI-fejléclogót nem téglalaposítottuk.
- A sajtóképek és U4 márkajel szerzői jogi/használati státuszának ellenőrzése továbbra is kötelező. A Wix CDN-válaszok és az éles oldal teljesítménye az ellenőrző eszközből nem volt igazolható.

## GitHub-képtárolás: gyökérok és helyreállítás (2026-10-18)

**Azonosított hiba:** a 16 külső eseménykép URL-je Wix-médiatranszformációra mutatott, miközben a médiabetöltések korábban `PENDING` állapotúak voltak, és a produkciós képfájlok létezése nem volt igazolva. A CSS minden képet 300 px szélességre korlátozott, ezért a programkártya szabad terét sem töltötték ki.

**Azonnali elrendezési javítás:** a 6 HTML-kiadásban az összes eseménykép `width:100%;max-width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:5px` beállítást kapott. Az eredeti 3 BMI eseményképet nem vágjuk meg.

**Helyben tárolás átállása – két fázisban, hogy ne szülessenek 404-es linkek:**
1. `scripts/cache_newsletter_images.py` és `.github/workflows/cache-newsletter-images.yml` a GitHub Actions gépén letölti a 19 eredetit (elsőként a felhasználó BMI Wix médiatárából, másodsorban a dokumentált külső forrásokból), validálja és generálja a `640 px` széles, `JPEG` (Wix e-mailhez) és `WebP` (webre) változatokat.
2. A megbízhatatlan letöltés helyére nem egy hibás kép kerül, hanem feliratozott, helyben generált eseménykártya. Az eredmény `data/event-image-assets.json` fájlban ellenőrizhető: `photo` vagy `labelled_fallback`, bájtméret és SHA-256.
3. `scripts/use_local_newsletter_images.py` csak a képfájlok sikeres létrejötte után állítja a 6 HTML-t és a központi nyilvántartást a `/assets/events/` GitHub-fájlokra.
4. A workflow **külön `generated/newsletter-image-assets-...` review branchre** ment. Ezt ellenőrizni és PR-ként egyesíteni kell a `main` ágba. A mostani PR kizárólag a megjelenítést javítja és bevezeti a migrációs eszközt; **a GitHub-képtárolás nem tekinthető késznek, amíg a generált fájlokat nem látjuk a main ágon.**

A képek harmadik féltől származó újraközlési jogai továbbra is külön szerkesztői ellenőrzést igényelnek; a saját Wix médiatárba másolás nem jelent automatikus felhasználási engedélyt.

## GitHub-képek: kész elsődleges forrás (2026-10-18)

- **Az összes hírlevél-kép a repository saját `assets/` mappájában van**: 19 programhoz JPEG + WebP (38 fájl) és a hivatalos BMI körlogóhoz PNG + WebP (2 fájl).
- A 3 webes nyelv és az egylapos nyelvi sablonok `/assets/events/<id>-640.webp` és `/assets/bmi-logo-272.webp` URL-eket használnak; a 3 Wix e-mail export teljes HTTPS JPEG/PNG URL-eket.
- Az adott 19 képből **17 valódi fénykép vagy eredeti BMI-grafika**, **2 jelölt helyettesítő** (`prater` és `u4`), mert a megadott harmadik fél képfájlját nem lehetett érvényes képformátumban letölteni.
- Az eredeti BMI-programképek képaránya megmaradt; a külső ajánlóképek 640×360 pixelesek, szülőelemet kitöltő megjelenítéssel és 5 px lekerekítéssel.
- A `data/event-image-assets.json` tartalmazza a generált fájlok méretét, SHA-256 értékét és fotó/helyettesítő státuszát. A hírlevél HTML-kódja közvetlenül nem használ többé Wix médiaszolgáltatást. A főoldal elsődleges nyelve magyar maradt.
- **Korlátok:** az éles GitHub Pages URL vizuális ellenőrzése és a harmadik féltől származó fotók újraközlési engedélye külön feladat. A későbbi képcseréket ugyanaz az automatizmus generálhatja új PR-ben.
