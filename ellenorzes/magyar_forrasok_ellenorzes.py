# A magyar forrasjeloltek 6D ellenorzese Crossref + PubMed ellen,
# ugyanazzal a logikaval, mint a kezirat hivatkozasai.
import json, re, time, urllib.parse, urllib.request, pathlib

UA = "MNL-refcheck/1.0 (mailto:szilikaroly@gmail.com)"
HERE = pathlib.Path(__file__).parent

# kulcs -> (varhato hivatkozas szovege, DOI, PMID)
JELOLTEK = {
 "erdei":      ("Erdei G, Bakacs M, Illés É, et al. Substantial variation across geographic regions in the obesity prevalence among 6-8 years old Hungarian children (COSI Hungary 2016). BMC Public Health 2018;18(1):611.",
                "10.1186/s12889-018-5530-6", "29743055"),
 "kovacsva":   ("Kovacs VA, Bakacs M, Kaposvari C, et al. Weight Status of 7-Year-Old Hungarian Children between 2010 and 2016 Using Different Classifications (COSI Hungary). Obes Facts 2018;11(3):195–205.",
                "10.1159/000487327", "29788023"),
 "spinelli":   ("Spinelli A, Buoncristiano M, Kovacs VA, et al. Prevalence of Severe Obesity among Primary School Children in 21 European Countries. Obes Facts 2019;12(2):244–258.",
                "10.1159/000500436", "31030201"),
 "jakab":      ("Jakab AE, Hidvégi EV, Illyés M, et al. [Prevalence of hypertension in overweight and obese Hungarian children and adolescents]. Orv Hetil 2020;161(4):151–160.",
                "10.1556/650.2020.31543", "31955583"),
 "sagodi":     ("Ságodi L, Fehér V, Kiss-Tóth E, et al. [Metabolic complications of obesity during adolescence, particularly regarding elevated uric acid levels]. Orv Hetil 2015;156(22):888–95.",
                "10.1556/650.2015.30140", "26004548"),
 "tobisch":    ("Tobisch B, Blatniczky L, Schusterova I, et al. [Insulin resistance and its effects in children and adolescents]. Orv Hetil 2021;162(11):403–412.",
                "10.1556/650.2021.32048", "33714938"),
 "hidvegi":    ("Hidvégi EV, Jakab A, Cziráki A, et al. [Normal values of peripheral (brachial) blood pressure measured in 14 062 Hungarian healthy children and adolescents with normal body mass index]. Orv Hetil 2024;165(28):1086–1100.",
                "10.1556/650.2024.33069", "39008368"),
 "matkovics":  ("Matkovics L, Czeglédi E. [The role of the school health care system in the prevention of childhood obesity - lessons of a pilot study]. Orv Hetil 2022;163(38):1499–1505.",
                "10.1556/650.2022.32569", "36121722"),
 "sarga":      ("Sárga D, Biró L, Kiss-Tóth B, et al. [Nutrient intake and nutritional status of 4-10-year-old Hungarian children]. Orv Hetil 2023;164(14):533–540.",
                "10.1556/650.2023.32713", "37031445"),
 "piko":       ("Pikó B, Kiss H, Gráczer A. [Relationship of young women's body appreciation with eating disorders and psychological variables]. Orv Hetil 2022;163(27):1082–1088.",
                "10.1556/650.2022.32518", "35895466"),
 "winklergip": ("Winkler G, Kis JT, Schandl L. [The \"other\" incretin - the therapeutic rediscovery of the glucose-dependent insulinotropic polypeptide]. Orv Hetil 2023;164(6):210–218.",
                "10.1556/650.2023.32710", "36774634"),
 "winklertri": ("Winkler G, Kis JT, Arapovicsné Kiss K, et al. [From GLP1 receptor agonists to triple hormone receptor activation supplemented with glucagon receptor agonism]. Orv Hetil 2023;164(42):1656–1664.",
                "10.1556/650.2023.32894", "37865924"),
 "horvathosa": ("Horváth G, Berner SC, Bardóczi AB, et al. [The role of obesity and weight reduction in obstructive sleep apnea]. Orv Hetil 2026;167(26):1011–1017.",
                "10.1556/650.2026.33589", "42365594"),
 "katona":     ("Katona ZB, Takács J, Gyömörei T, et al. [Assessing physical activity and subjective health status among Hungarian secondary school students during the distance learning period]. Orv Hetil 2022;163(17):655–662.",
                "10.1556/650.2022.32481", "35462350"),
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(s):
    s = (s or "").lower().replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-z0-9]+", "", s)


eredmeny = []
for kulcs, (ref, doi, pmid) in JELOLTEK.items():
    cr = pm = None
    try:
        cr = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))["message"]
    except Exception as e:
        cr = None
    try:
        pm = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                 "?db=pubmed&retmode=json&id=" + pmid)["result"][pmid]
    except Exception:
        pm = None
    time.sleep(0.35)

    d = {"kulcs": kulcs, "doi": doi, "pmid": pmid}
    d["D1_doi"] = "OK" if cr else "HIBA"
    # a magyar folyoiratok Crossref-rekordjai gyakran hianyosak -> PubMed az elsodleges
    first = pm["authors"][0]["name"].split()[0] if (pm and pm.get("authors")) else None
    if not first and cr:
        first = (cr.get("author") or [{}])[0].get("family")
    d["D2_first"] = "OK" if (first and norm(first) in norm(ref)) else "ELTER"
    n_auth = len(pm.get("authors", [])) if pm else (len(cr.get("author", [])) if cr else 0)
    etal = "et al" in ref.lower()
    d["D3_authors"] = "OK" if ((n_auth > 3) == etal) else ("HIANYZO et al." if n_auth > 3 else "FELESLEGES et al.")
    jpm = pm.get("source") if pm else None
    jr = (cr.get("short-container-title") or cr.get("container-title") or [None])[0] if cr else None
    d["D4_journal"] = "OK" if any(j and norm(j) in norm(ref) for j in (jpm, jr)) else "ELTER"
    vol = (pm.get("volume") if pm else None) or (cr.get("volume") if cr else None)
    m = re.search(r"\d+", str(vol or ""))
    vol = m.group(0) if m else None
    d["D5_volume"] = "OK" if (vol and re.search(r"\b" + re.escape(vol) + r"\s*[(:]", ref)) else "ELTER"
    lapok = (pm.get("pages") if pm else None) or (cr.get("page") if cr else None)
    art = re.split(r"[./-]", doi)[-1]
    ok = False
    for c in (lapok, art):
        if c and norm(str(c).replace("--", "-")) in norm(ref):
            ok = True
    d["D6_pages"] = "OK" if ok else f"ELLENORIZNI (PubMed: {lapok})"
    evek = []
    if pm:
        mm = re.match(r"(\d{4})", pm.get("pubdate", ""))
        if mm: evek.append(int(mm.group(1)))
    if cr:
        for k in ("published-print", "issued"):
            dp = cr.get(k, {}).get("date-parts") or []
            if dp and dp[0] and dp[0][0]:
                evek.append(dp[0][0])
    d["D7_year"] = "OK" if any(str(y) in ref for y in evek) else f"ELTER (PubMed: {evek})"
    d["nyelv"] = (pm or {}).get("lang", [None])[0] if pm else None
    eredmeny.append(d)

(HERE / "magyar_forrasok_6d.json").write_text(
    json.dumps({"jeloltek": JELOLTEK, "eredmeny": eredmeny}, ensure_ascii=False, indent=1),
    encoding="utf-8")

fej = f"{'kulcs':<13}{'D1':<7}{'D2':<8}{'D3':<17}{'D4':<8}{'D5':<8}{'D6':<26}{'D7':<10}"
print(fej); print("-" * len(fej))
for d in eredmeny:
    print(f"{d['kulcs']:<13}{d['D1_doi']:<7}{d['D2_first']:<8}{d['D3_authors']:<17}"
          f"{d['D4_journal']:<8}{d['D5_volume']:<8}{d['D6_pages']:<26}{d['D7_year']:<10}")
jo = [d for d in eredmeny if all(str(v).startswith("OK") for k, v in d.items() if k.startswith("D"))]
print(f"\nkifogastalan: {len(jo)} / {len(eredmeny)}")
