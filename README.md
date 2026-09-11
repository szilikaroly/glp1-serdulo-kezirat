# Inkretin-alapú terápiák a gyermeknőgyógyászati praxisban

**A GLP-1 receptor agonisták hatása a serdülőkori reproduktív axisra** — összefoglaló közlemény a *Magyar Nőorvosok Lapja* számára.

Ez a repó nem csak a kéziratot tartalmazza, hanem az előállításának teljes, újrafuttatható láncát: az ábrákat generáló kódot, a gazdasági modellt, a hivatkozás-ellenőrzőt és a bírálatokat.

---

## Mi van a repóban

| Útvonal | Mi ez |
|---|---|
| `kezirat_MNL.docx` | **A beküldésre szánt kézirat**, a szerzői útmutató szerint formázva |
| `kezirat_szoveg.md` | A generált, végleges markdown-változat (számozott hivatkozásokkal) |
| `kezirat_torzs.md` | A törzsszöveg forrása — **szimbolikus hivatkozáskulcsokkal** (`[[weghuber]]`) |
| `kezirat_vege_tablazatok.md` | A táblázatok és ábraaláírások forrása |
| `kezirat_promptok.md` | Képpromptok: a négy ábra részletes leírása + illusztratív képek |
| `refs.json` | Kulcs → hivatkozás szövege |
| `ids.json` | Kulcs → DOI/PMID (**egyetlen forrás**, ebből származik minden azonosító-térkép) |
| `abrak/` | Az ábrákat generáló scriptek + a kimenetek (600 dpi PNG, 300 dpi TIFF, színes és szürkeárnyalatos) |
| `ellenorzes/` | 6D bibliográfiai validátor és a jelentései |
| `biralatok/` | Rigorózus bírálat, metodikai–élettani–biokémiai bírálat, javítási napló |

---

## A hivatkozáskezelés logikája

A törzsszöveg **nem** tartalmaz sorszámokat, csak szimbolikus kulcsokat:

```
... 68 hét alatt 16,1%-os BMI-csökkenést eredményezett [[weghuber]].
```

A sorszámozás **származtatott**: az `osszefuz_es_szamoz.py` végigolvassa a törzsszöveget és a táblázatokat, az **első előfordulás sorrendjében** számoz, majd ebből építi a jegyzéket *és* az ellenőrző azonosító-térképét is.

Ennek az a haszna, hogy egy hivatkozás beszúrása vagy törlése soha nem csúsztathatja el a számozást, és az ellenőrző sem hasonlíthat rossz tételhez. Egy új forrás felvétele három lépés:

1. `refs.json` — a hivatkozás szövege
2. `ids.json` — a DOI és a PMID
3. `[[kulcs]]` beírása a szövegbe

Ezután `python osszefuz_es_szamoz.py` mindent újraszámoz.

---

## Újrafuttatás

```bash
python osszefuz_es_szamoz.py        # összeillesztés + sorszámozás + azonosító-térkép
python build_docx.py                # a .docx előállítása a markdownból
python ellenorzes/validate_6d.py    # 6D validáció + cit-ref kereszt-ellenőrzés (hálózat kell)
cd abrak && python abra1_mechanizmus.py && python abra2_eletut_flowchart.py \
          && python abra3_megelozes_koltseg.py && python abra4_biokemiai_kaszkad.py \
          && python mono_build.py   # szürkeárnyalatos változatok
```

Függőségek: `python-docx`, `matplotlib`, `numpy`. Hálózat csak a validátorhoz kell (Crossref + NCBI E-utilities).

---

## A 6D bibliográfiai validáció

Minden hivatkozást hat dimenzióban vet össze a Crossref és a PubMed rekordjával — DOI feloldhatósága, első szerző, szerzőlista (*et al.* szabály), folyóirat, kötet, oldalszám vagy cikkszám —, plusz az évszámot. Kezeli a szokásos buktatókat:

- **cikkszámos folyóiratok** (füzetszám nélküli kötet: `13:897776`)
- **testületi szerzők** (nincs *et al.*)
- **online vs. nyomtatott évszám** (a Crossref `issued` mezője gyakran az online dátum)
- kiadói kötetformátum-furcsaságok (`"Volume 19"`)

**Jelenlegi állapot: 45/45 tétel megfelelt, cit-ref kereszt-ellenőrzés tiszta.**

---

## A gazdasági modell

Az `abrak/abra3_megelozes_koltseg.py` egy szemléltető életút-modell 1000 obes leányra, 14-től 65 éves korig, **társadalmi perspektívában**, 3%/év diszkontálással, forintban:

- közvetlen ellátási költség
- munkahelyi távollétek (absenteizmus)
- reprodukciós veszteség (ART-ciklusok, GDM-mel szövődött terhesség)
- a kezelés kettős hatása: testsúlymediált + fogyástól független
- egyirányú **és** valószínűségi (4000 futtatásos Monte Carlo) érzékenységi elemzés

> **Figyelem:** a modell minden paramétere irodalmi nagyságrendekre támaszkodó *feltételezés*, nem mért incidencia- és nem mért költségadat. Szemléltetésre készült; finanszírozási döntés megalapozására önmagában nem alkalmas.

---

## Állapot

- Törzsszöveg **3489 szó** (határ: 3500) · összefoglalás 328 szó (határ: 350) · **45 hivatkozás** (határ: 80)
- 4 ábra, 5 táblázat, mind színes és szürkeárnyalatos változatban
- Nyitott teendő: a címoldalon a munkahely és a levelezési cím kitöltése

A bírálati pontok állapotát a `biralatok/3_javitasi_naplo.md` tartja nyilván.
