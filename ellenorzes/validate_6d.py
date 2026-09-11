# 6D bibliografiai validacio + cit-ref kereszt-ellenorzes
# 6 dimenzio: DOI, elso szerzo, szerzolista (szam), folyoirat, kotet, oldal/cikkszam (+ ev)
# Forrasok: Crossref REST API es NCBI eutils (PubMed esummary)
import json, re, time, urllib.parse, urllib.request, pathlib, sys

HERE = pathlib.Path(__file__).parent
SRC  = HERE.parent / "kezirat_szoveg.md"
UA   = "MNL-refcheck/1.0 (mailto:szilikaroly@gmail.com)"

# ref-szam -> (DOI vagy None, PMID); az osszefuz_es_szamoz.py altal generalt terkepbol
IDS = {int(k): tuple(v) for k, v in
       json.loads((HERE / "ids_szam.json").read_text(encoding="utf-8")).items()}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def crossref(doi):
    return get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))["message"]

def pubmed(pmid):
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
         "?db=pubmed&retmode=json&id=" + pmid)
    return get(u)["result"][pmid]

# ------------------------------------------------- a kezirat hivatkozasjegyzeke
txt = SRC.read_text(encoding="utf-8")
blokk = txt[txt.index("## IRODALOMJEGYZÉK"):txt.index("## ENGLISH TITLE")]
printed = {}
for m in re.finditer(r"^\[(\d+)\]\s+(.+?)$", blokk, re.M):
    printed[int(m.group(1))] = m.group(2).strip()

# ------------------------------------------------- osszehasonlito segedek
def norm(s):
    s = (s or "").lower()
    s = s.replace("–", "-").replace("—", "-").replace("’", "'")
    return re.sub(r"[^a-z0-9]+", "", s)

def pages_match(printed_ref, cr_page, pm_pages, article_no):
    """Elfogad oldalszam-tartomanyt es cikkszamot is (MDPI/BMC/Frontiers stilus)."""
    cand = [cr_page, pm_pages, article_no]
    pref = norm(printed_ref)
    for c in cand:
        if not c:
            continue
        c = str(c).replace("--", "-")
        if norm(c) and norm(c) in pref:
            return True, c
        # roviditett veg: 4226-37 vs 4226-4237
        m = re.match(r"^(\d+)-(\d+)$", c)
        if m:
            a, b = m.groups()
            if len(b) < len(a):
                b = a[: len(a) - len(b)] + b
            if norm(f"{a}-{b}") in pref or norm(f"{a}-{b[len(a)-len(str(int(b)))]:}") in pref:
                return True, c
            short = b[len(a) - 2:] if len(b) == len(a) else b
            if norm(f"{a}-{short}") in pref:
                return True, c
    return False, cand

rows, issues = [], []
for n in sorted(IDS):
    doi, pmid = IDS[n]
    ref = printed.get(n, "")
    cr = pm = None
    try:
        if doi:
            cr = crossref(doi)
    except Exception as e:
        issues.append(f"[{n}] DOI nem oldhato fel Crossrefben: {doi} ({type(e).__name__})")
    try:
        pm = pubmed(pmid)
    except Exception as e:
        issues.append(f"[{n}] PMID nem elerheto: {pmid} ({type(e).__name__})")
    time.sleep(0.35)

    d = {"n": n, "doi": doi, "pmid": pmid}

    # D1 - DOI letezik es feloldhato
    d["D1_doi"] = "OK" if (doi and cr) else ("NINCS DOI" if not doi else "HIBA")

    # D2 - elso szerzo vezetekneve
    first = None
    if cr and cr.get("author"):
        first = cr["author"][0].get("family")
    pm_first_raw = pm["authors"][0]["name"] if (pm and pm.get("authors")) else None
    collective = bool(pm_first_raw and re.search(r"collaborators|group|committee|consortium",
                                                 pm_first_raw, re.I))
    if collective:
        first = pm_first_raw            # testuleti szerzo: a teljes nev a hivatkozas eleje
    elif not first and pm_first_raw:
        first = pm_first_raw.split()[0]
    d["first_author"] = first
    d["D2_first"] = "OK" if (first and norm(first) in norm(ref)) else "ELTER"

    # D3 - szerzolista: >3 szerzo eseten 'et al.', pontosan <=3 eseten mind
    n_auth = len(cr.get("author", [])) if cr else (len(pm.get("authors", [])) if pm else 0)
    d["n_authors"] = n_auth
    has_etal = "et al" in ref.lower()
    if collective:
        n_auth = 1
        d["n_authors"] = 1
        d["D3_authors"] = "OK (testuleti szerzo)" if not has_etal else "FELESLEGES et al."
    elif n_auth == 0:
        d["D3_authors"] = "n. a. (testulet)"
    elif n_auth > 3:
        d["D3_authors"] = "OK" if has_etal else "HIANYZO et al."
    else:
        d["D3_authors"] = "OK" if not has_etal else "FELESLEGES et al."

    # D4 - folyoirat
    jr = None
    if cr:
        jr = (cr.get("short-container-title") or cr.get("container-title") or [None])[0]
    jpm = pm.get("source") if pm else None
    d["journal"] = jpm or jr
    d["D4_journal"] = "OK" if any(j and norm(j) in norm(ref) for j in (jpm, jr)) else "ELTER"

    # D5 - kotet
    # nehany kiado 'Volume 19' formaban adja meg a kotetet -> a szamot vesszuk,
    # es a PubMed ertekere tamaszkodunk elsokent
    vol = (pm.get("volume") if pm else None) or (cr.get("volume") if cr else None)
    m_vol = re.search(r"\d+", str(vol or ""))
    vol = m_vol.group(0) if m_vol else None
    d["volume"] = vol
    # kotet: 'kotet(fuzet)' vagy cikkszamos, fuzet nelkuli folyoiratnal 'kotet:cikkszam'
    d["D5_volume"] = "OK" if (vol and re.search(
        r"\b" + re.escape(str(vol)) + r"\s*[(:]", ref)) else "ELTER"

    # D6 - oldalszam vagy cikkszam
    art = None
    if doi:
        art = re.split(r"[./-]", doi)[-1]
    ok, cand = pages_match(ref, cr.get("page") if cr else None,
                           pm.get("pages") if pm else None, art)
    d["pages_src"] = cand
    d["D6_pages"] = "OK" if ok else "ELLENORIZNI"

    # +ev
    # ev: a nyomtatott megjelenes az iranyado (a Crossref 'issued' gyakran az online datum)
    years = []
    if pm:
        m = re.match(r"(\d{4})", pm.get("pubdate", ""))
        if m: years.append(int(m.group(1)))
    if cr:
        for k in ("published-print", "issued"):
            dp = cr.get(k, {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                years.append(dp[0][0])
    d["year"] = years[0] if years else None
    d["year_kandidatusok"] = sorted(set(years))
    d["D7_year"] = "OK" if any(str(y) in ref for y in years) else "ELTER"
    rows.append(d)

# ------------------------------------------------- cit-ref kereszt-ellenorzes
body = txt[txt.index("## ÖSSZEFOGLALÁS"):txt.index("## IRODALOMJEGYZÉK")]
cited = set()
for m in re.finditer(r"\[(\d+(?:\s*,\s*\d+)*)\]", body):
    for x in m.group(1).split(","):
        cited.add(int(x.strip()))
listed = set(printed)
seq = []
for m in re.finditer(r"\[(\d+(?:\s*,\s*\d+)*)\]", body):
    for x in m.group(1).split(","):
        v = int(x.strip())
        if v not in seq:
            seq.append(v)

report = {
 "hivatkozasok_szama": len(listed),
 "szovegben_idezett": sorted(cited),
 "jegyzekben_szereplo": sorted(listed),
 "idezett_de_nincs_jegyzekben": sorted(cited - listed),
 "jegyzekben_van_de_nincs_idezve": sorted(listed - cited),
 "elso_elofordulas_sorrendje": seq,
 "sorrend_helyes": seq == sorted(seq),
 "tetelek": rows,
 "technikai_hibak": issues,
}
(HERE / "6d_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

# ------------------------------------------------- konzol-osszegzes
print(f"{'#':>3} {'D1 DOI':<10}{'D2 szerzo':<11}{'D3 lista':<17}{'D4 lap':<9}"
      f"{'D5 kotet':<10}{'D6 oldal':<14}{'D7 ev':<7}")
for d in rows:
    print(f"{d['n']:>3} {d['D1_doi']:<10}{d['D2_first']:<11}{d['D3_authors']:<17}"
          f"{d['D4_journal']:<9}{d['D5_volume']:<10}{d['D6_pages']:<14}{d['D7_year']:<7}")
bad = [d for d in rows if any(not str(v).startswith("OK") and v not in ("NINCS DOI",)
                              for k, v in d.items() if k.startswith("D"))]
print(f"\nTetelek osszesen: {len(rows)}  | kifogastalan: {len(rows)-len(bad)}  | ellenorzendo: {len(bad)}")
print("Idezett de nincs jegyzekben:", report["idezett_de_nincs_jegyzekben"] or "nincs")
print("Jegyzekben van de nincs idezve:", report["jegyzekben_van_de_nincs_idezve"] or "nincs")
print("Szamozas az elso elofordulas sorrendjeben:", report["sorrend_helyes"])
if issues:
    print("Technikai hibak:", *issues, sep="\n  ")
