# Az OH-valtozat osszeallitasa es hivatkozas-sorszamozasa.
# A refs.json / ids.json a szulomappaban van: EGYETLEN kozos forras a ket kezirathoz.
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
SZULO = HERE.parent

refs = json.loads((SZULO / "refs.json").read_text(encoding="utf-8"))
torzs = (HERE / "kezirat_torzs.md").read_text(encoding="utf-8")
tabl = (HERE / "kezirat_vege_tablazatok.md").read_text(encoding="utf-8")

angol = tabl[:tabl.index("## TÁBLÁZATOK")]
tablazatok = tabl[tabl.index("## TÁBLÁZATOK"):]

# --- sorrend: az elso elofordulas a torzsben, majd a tablazatokban ---
idezo = torzs + "\n" + tablazatok
sorrend, latott = [], set()
for m in re.finditer(r"\[\[([a-z0-9]+)\]\]", idezo):
    k = m.group(1)
    if k not in latott:
        latott.add(k)
        sorrend.append(k)

hianyzo = [k for k in sorrend if k not in refs]
if hianyzo:
    raise SystemExit("Hivatkozott, de a jegyzekben nem szereplo kulcs: " + ", ".join(hianyzo))
nem_idezett = [k for k in refs if k not in latott]

szam = {k: i + 1 for i, k in enumerate(sorrend)}


def cserel(szoveg):
    def egy(m):
        kulcsok = re.findall(r"\[\[([a-z0-9]+)\]\]", m.group(0))
        return "[" + ", ".join(str(szam[k]) for k in kulcsok) + "]"
    return re.sub(r"\[\[[a-z0-9]+\]\](?:\s*\[\[[a-z0-9]+\]\])*", egy, szoveg)


jegyzek = ["## IRODALOM", ""]
for k in sorrend:
    jegyzek.append(f"[{szam[k]}] {refs[k]}")
    jegyzek.append("")

vegleges = "\n".join([
    cserel(torzs).rstrip(), "",
    "---", "",
    angol.strip(), "",
    "---", "",
    "## ANYAGI TÁMOGATÁS ÉS ÉRDEKELTSÉGEK", "",
    "A közlemény megírása anyagi támogatásban nem részesült. A szerzőknek nincsenek "
    "érdekeltségeik.", "",
    "## SZERZŐI MUNKAMEGOSZTÁS", "",
    "*(a szerzők töltik ki)*", "",
    "---", "",
    "\n".join(jegyzek).rstrip(), "",
    "---", "",
    cserel(tablazatok).rstrip(), "",
])
(HERE / "kezirat_szoveg.md").write_text(vegleges, encoding="utf-8")

# az ellenorzo azonosito-terkepe: SZARMAZTATOTT a kozos ids.json-bol
ids = {k: v for k, v in json.loads((SZULO / "ids.json").read_text(encoding="utf-8")).items()
       if not k.startswith("_")}
hianyzo_id = [k for k in sorrend if k not in ids]
if hianyzo_id:
    raise SystemExit("Hianyzo DOI/PMID: " + ", ".join(hianyzo_id))
(HERE / "ids_szam.json").write_text(
    json.dumps({str(szam[k]): ids[k] for k in sorrend}, ensure_ascii=False, indent=1),
    encoding="utf-8")

print("hivatkozasok:", len(sorrend))
print("nem idezett jegyzektetel:", ", ".join(nem_idezett) if nem_idezett else "nincs")
body = vegleges[vegleges.index("## BEVEZETÉS"):vegleges.index("---\n\n## SUMMARY")]
sorok = [s for s in body.split("\n") if not s.startswith("#")]
sz = re.sub(r"\[[\d,\s]+\]", "", "\n".join(sorok))
print("torzsszoveg:", len(re.sub(r"[*_]", " ", sz).split()), "szo")
elso = [int(x) for x in re.findall(r"\[(\d+)", body)]
seq, latott2 = [], set()
for v in elso:
    if v not in latott2:
        latott2.add(v); seq.append(v)
print("sorrendhelyes szamozas:", seq == sorted(seq))
