# A szimbolikus kulcsu reszekbol osszeallitja a vegleges kesziratot,
# es a hivatkozasokat az ELSO ELOFORDULAS sorrendjeben szamozza.
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
refs = json.loads((HERE / "refs.json").read_text(encoding="utf-8"))

torzs = (HERE / "kezirat_torzs.md").read_text(encoding="utf-8")
tabl  = (HERE / "kezirat_vege_tablazatok.md").read_text(encoding="utf-8")
vege  = (HERE / "kezirat_vege.md").read_text(encoding="utf-8")
angol = vege[:vege.index("## TÁBLÁZATOK")]
promptok = (HERE / "kezirat_promptok.md").read_text(encoding="utf-8")

# a hivatkozott reszek, amelyekben a sorszamozas szamit (torzs + tablazatok)
idezo = torzs + "\n" + tabl

# --- sorrend meghatarozasa ---
sorrend, latott = [], set()
for m in re.finditer(r"\[\[([a-z0-9]+)\]\]", idezo):
    k = m.group(1)
    if k not in latott:
        latott.add(k); sorrend.append(k)

hianyzo = [k for k in sorrend if k not in refs]
if hianyzo:
    raise SystemExit("Hivatkozott, de a jegyzekben nem szereplo kulcs: " + ", ".join(hianyzo))
nem_idezett = [k for k in refs if k not in latott]

szam = {k: i + 1 for i, k in enumerate(sorrend)}

def cserel(szoveg):
    # egymas melletti hivatkozasok osszevonasa: [[a]] [[b]] -> [3, 7]
    def egy(m):
        kulcsok = re.findall(r"\[\[([a-z0-9]+)\]\]", m.group(0))
        return "[" + ", ".join(str(szam[k]) for k in kulcsok) + "]"
    return re.sub(r"\[\[[a-z0-9]+\]\](?:\s*\[\[[a-z0-9]+\]\])*", egy, szoveg)

jegyzek = ["## IRODALOMJEGYZÉK", ""]
for k in sorrend:
    jegyzek.append(f"[{szam[k]}] {refs[k]}")
    jegyzek.append("")

vegleges = "\n".join([
    cserel(torzs).rstrip(), "",
    "---", "",
    "## KÖSZÖNETNYILVÁNÍTÁS", "",
    "*(a szerző tölti ki)*", "",
    "## ÉRDEKELTSÉGEK, TÁMOGATÁSOK", "",
    "A szerző(k)nek nincsenek érdekeltségei. A közlemény elkészítése külső támogatásban nem részesült.", "",
    "---", "",
    "\n".join(jegyzek).rstrip(), "",
    "---", "",
    angol.strip(), "",
    "---", "",
    cserel(tabl).rstrip(), "",
    "---", "",
    promptok.strip(), "",
])

(HERE / "kezirat_szoveg.md").write_text(vegleges, encoding="utf-8")

print(f"hivatkozasok szama: {len(sorrend)}")
if nem_idezett:
    print("FIGYELEM - a jegyzekben van, de nincs idezve:", ", ".join(nem_idezett))
else:
    print("minden jegyzekbeli tetel idezve van")
body = vegleges[vegleges.index("## BEVEZETÉS"):vegleges.index("## KÖSZÖNETNYILVÁNÍTÁS")]
print("torzsszoveg szavak:", len(re.sub(r"[#*_\[\]]", " ", body).split()))
# a szamozas sorrendjenek ellenorzese
elso = [int(x) for x in re.findall(r"\[(\d+)", body)]
latott2, seq = set(), []
for v in elso:
    if v not in latott2: latott2.add(v); seq.append(v)
print("szamozas sorrendhelyes:", seq == sorted(seq))
# a kulcs -> szam terkep mentese az ellenorzohoz
(HERE / "ellenorzes" / "kulcs_szam.json").write_text(
    json.dumps(szam, ensure_ascii=False, indent=1), encoding="utf-8")

# az ellenorzo azonosito-terkepe is SZARMAZTATOTT, hogy ne tudjon elavulni
ids = {k: v for k, v in json.loads((HERE / "ids.json").read_text(encoding="utf-8")).items()
       if not k.startswith("_")}
hianyzo_id = [k for k in sorrend if k not in ids]
if hianyzo_id:
    raise SystemExit("Hianyzo DOI/PMID azonosito: " + ", ".join(hianyzo_id))
(HERE / "ellenorzes" / "ids_szam.json").write_text(
    json.dumps({str(szam[k]): ids[k] for k in sorrend}, ensure_ascii=False, indent=1),
    encoding="utf-8")
print("azonosito-terkep ujragenerálva:", len(sorrend), "tetel")
