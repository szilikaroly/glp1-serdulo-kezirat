# Orvosi Hetilap változat

**Fiatalkori elhízás és kezelése: hazai helyzetkép és a GLP-1-receptor-agonisták helye a terápiás lépcsőben**

A gyermeknőgyógyászati (MNL) kézirat anyagára épülő, más célközönségnek szánt változat. A két kézirat **közös hivatkozáspoolt** használ: a `../refs.json` és a `../ids.json` az egyetlen forrás mindkettőhöz, a sorszámozás pedig kéziratonként külön, az első előfordulás sorrendjében készül.

## Miben tér el az MNL-változattól

| | MNL-változat | OH-változat |
|---|---|---|
| Fókusz | reproduktív axis, gyermeknőgyógyász olvasónak | a teljes terápiás lépcső, általános orvosi olvasónak |
| Hazai réteg | nincs | **14 magyar hivatkozás**, önálló „Hazai helyzetkép” fejezettel |
| Összefoglaló | magyar + külön angol blokk | **kétnyelvű** (Összefoglaló + Summary), OH-stílusú zárósorral |
| Hivatkozás | 40 | **54** |
| Szerkezet | öt hatásdomén | terápiás lépcső (életmód → metformin → GLP-1RA → kettős/hármas agonizmus → sebészet) |

## Újrafuttatás

```bash
python osszefuz_es_szamoz.py   # összeillesztés + sorszámozás + azonosító-térkép
python build_docx.py           # kezirat_OrvHetil.docx
python validate_6d.py          # 6D validáció (hálózat kell)
```

Az ábrák közösek a szülőmappa `abrak/` könyvtárával.

## Állapot

- Törzsszöveg **2859 szó**, magyar összefoglaló 246 szó, angol summary 305 szó
- **54 hivatkozás**, 6D validáció **54/54**, cit-ref tiszta, sorrendhelyes számozás
- 4 ábra, 5 táblázat (közös az MNL-változattal)
- Beküldés előtt ellenőrizendő: az Orvosi Hetilap érvényes szerzői útmutatójának terjedelmi és formai előírásai, valamint a 2. affiliáció doktori iskolájának hivatalos megnevezése
