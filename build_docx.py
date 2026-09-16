# A kezirat .docx-e a Magyar Noorvosok Lapja szerzoi utmutatoja szerint:
# Times New Roman 12 pt, dupla sorkoz, 3 cm margo, kozepen felul oldalszam,
# tablazatok kulon oldalakon, abrak kulon fajlban.
import re, pathlib
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = pathlib.Path(__file__).parent
SRC = HERE / "kezirat_szoveg.md"
OUT = HERE / "kezirat_MNL.docx"

# ---------------------------------------------------------------- segedek
def alap_dokumentum():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    pf = st.paragraph_format
    pf.line_spacing = 2.0
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(3)
        s.left_margin = s.right_margin = Cm(3)
    return doc

def oldalszam_fejlecbe(doc):
    """Folyamatos, kozepre zart, arab oldalszam a lap tetejen."""
    for s in doc.sections:
        p = s.header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run()
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        for instr in ("begin", "PAGE", "end"):
            e = OxmlElement("w:fldChar") if instr != "PAGE" else OxmlElement("w:instrText")
            if instr == "PAGE":
                e.set(qn("xml:space"), "preserve")
                e.text = " PAGE "
            else:
                e.set(qn("w:fldCharType"), instr)
            r._r.append(e)

def cim(doc, szoveg, meret=12, felkover=True, kozep=False, elotte=0, utana=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(elotte)
    p.paragraph_format.space_after = Pt(utana)
    if kozep:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(szoveg)
    r.bold = felkover
    r.font.size = Pt(meret)
    return p

def bekezdes(doc, szoveg, dolt=False, meret=12, sorkoz=2.0, igazit=None):
    """A **felkover** jeloleseket valodi felkover futamokra bontja."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = sorkoz
    if igazit is not None:
        p.alignment = igazit
    for i, darab in enumerate(re.split(r"\*\*(.+?)\*\*", szoveg)):
        if not darab:
            continue
        r = p.add_run(darab)
        r.bold = (i % 2 == 1)
        r.italic = dolt
        r.font.size = Pt(meret)
    return p

def uj_oldal(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def tablazat(doc, fejlec, sorok, szeles=None):
    t = doc.add_table(rows=1, cols=len(fejlec))
    t.style = "Table Grid"
    for i, c in enumerate(fejlec):
        cella = t.rows[0].cells[i]
        cella.text = ""
        p = cella.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(c)
        r.bold = True
        r.font.size = Pt(9)
        r.font.name = "Times New Roman"
    for sor in sorok:
        cellak = t.add_row().cells
        for i, c in enumerate(sor):
            cellak[i].text = ""
            p = cellak[i].paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            felkover = c.startswith("**") and c.endswith("**")
            r = p.add_run(c.strip("*"))
            r.bold = felkover
            r.font.size = Pt(9)
            r.font.name = "Times New Roman"
    return t

# ---------------------------------------------------------------- forras
szoveg = SRC.read_text(encoding="utf-8")

def szakasz(kezdet, veg=None):
    i = szoveg.index(kezdet)
    j = szoveg.index(veg) if veg else len(szoveg)
    return szoveg[i:j]

def bekezdesek(blokk):
    """Cimsorok nelkuli bekezdesek listaja, a markdown jelolok eltavolitasaval."""
    ki = []
    for sor in blokk.split("\n"):
        s = sor.strip()
        if not s or s.startswith("#") or s.startswith("---") or s.startswith("|"):
            continue
        ki.append(s)
    return ki

doc = alap_dokumentum()
oldalszam_fejlecbe(doc)

# ============================================================ 1. CIMOLDAL
SZERZOK = [
    ("Dézsi Csilla",        "1,2,3,4"),
    ("Gulyás-Oldal Viktor", "1,2"),
    ("Gálóczi Imre",        "1,2"),
    ("Lábodi László",       "4"),
    ("Marusin Ildikó",      "4"),
    ("Szili Károly",        "1,2,3,4"),
    ("Nagy Sándor",         "1,2"),
]
AFFILIACIOK = [
    ("1", "Széchenyi István Egyetem, Szülészeti és Nőgyógyászati Tanszék, Győr"),
    ("2", "Széchenyi István Egyetem, RGDI [a doktori iskola teljes hivatalos nevét és "
          "helységnevét kérjük kiegészíteni]"),
    ("3", "Szegedi Tudományegyetem, Szent-Györgyi Albert Orvostudományi Kar, "
          "Szülészeti és Nőgyógyászati Klinika, Szeged"),
    ("4", "S.O.S. 24 Kft. – 48. Családorvosi Rendelő, Szeged"),
]
LEVELEZO = "Szili Károly"

def szerzosor(doc, szerzok):
    """Szerzonev + felso indexes affiliacio-szamok, vesszovel elvalasztva."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.5
    for i, (nev, idx) in enumerate(szerzok):
        r = p.add_run(nev)
        r.bold = True
        r.font.size = Pt(12)
        r.font.name = "Times New Roman"
        f = p.add_run(idx)
        f.font.superscript = True
        f.font.size = Pt(12)
        f.font.name = "Times New Roman"
        if i < len(szerzok) - 1:
            v = p.add_run(", ")
            v.font.size = Pt(12)
            v.font.name = "Times New Roman"
    return p

def affiliacio_sor(doc, jel, szoveg):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(2)
    f = p.add_run(jel)
    f.font.superscript = True
    f.font.size = Pt(11)
    f.font.name = "Times New Roman"
    r = p.add_run(" " + szoveg)
    r.font.size = Pt(11)
    r.font.name = "Times New Roman"
    return p

cim(doc, "Inkretin-alapú terápiák a gyermeknőgyógyászati praxisban: "
         "a GLP-1 receptor agonisták hatása a serdülőkori reproduktív axisra",
    meret=14, kozep=True, utana=12)
bekezdes(doc, "**Alcím / rövid cím:** Inkretinek a serdülőkori reproduktív axison",
         igazit=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()

szerzosor(doc, SZERZOK)
doc.add_paragraph()
for _jel, _aff in AFFILIACIOK:          # NB: a ciklusvaltozo nem lehet 'szoveg',
    affiliacio_sor(doc, _jel, _aff)     # mert modulszinten felulirna a kezirat szoveget
doc.add_paragraph()

bekezdes(doc, f"**Kapcsolattartó (levelező) szerző:** {LEVELEZO} · szilikaroly@gmail.com · "
              "levelezési cím: …………………………………… *(kitöltendő)*",
         meret=11, sorkoz=1.2, igazit=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
bekezdes(doc, "A szerzői útmutató szerint még kiegészítendő: (a) a szerzők neve után a „dr.” "
              "megjelölés ott, ahol ez indokolt; (b) minden intézménynél az intézményvezető neve; "
              "(c) a 2. affiliáció teljes hivatalos megnevezése és helységneve; "
              "(d) a levelezési cím. A kísérőlevélhez az első szerző fényképét is csatolni kell.",
         dolt=True, meret=10, sorkoz=1.2, igazit=WD_ALIGN_PARAGRAPH.CENTER)
uj_oldal(doc)

# ============================================================ 2. OSSZEFOGLALAS
cim(doc, "ÖSSZEFOGLALÁS", utana=6)
blokk = szakasz("## ÖSSZEFOGLALÁS", "## BEVEZETÉS")
for b in bekezdesek(blokk):
    if b.startswith("**Kulcsszavak"):
        doc.add_paragraph()
    bekezdes(doc, b)
uj_oldal(doc)

# ============================================================ 3. SZOVEG
torzs = szakasz("## BEVEZETÉS", "---\n\n## KÖSZÖNETNYILVÁNÍTÁS")
for sor in torzs.split("\n"):
    s = sor.strip()
    if not s or s.startswith("---"):
        continue
    if s.startswith("### "):
        cim(doc, s[4:], elotte=8, utana=2)
    elif s.startswith("## "):
        cim(doc, s[3:].upper(), elotte=12, utana=4)
    else:
        bekezdes(doc, s)

# ============================================================ 4-5. KOSZONET, ERDEKELTSEGEK
cim(doc, "KÖSZÖNETNYILVÁNÍTÁS", elotte=12, utana=4)
bekezdes(doc, "(a szerző tölti ki)", dolt=True)
cim(doc, "ÉRDEKELTSÉGEK, TÁMOGATÁSOK", elotte=12, utana=4)
bekezdes(doc, "A szerző(k)nek nincsenek érdekeltségei. "
              "A közlemény elkészítése külső támogatásban nem részesült.")
uj_oldal(doc)

# ============================================================ 6. IRODALOMJEGYZEK
cim(doc, "IRODALOMJEGYZÉK", utana=6)
for b in bekezdesek(szakasz("## IRODALOMJEGYZÉK", "## ENGLISH TITLE")):
    p = bekezdes(doc, b, sorkoz=1.5)
    p.paragraph_format.space_after = Pt(4)
uj_oldal(doc)

# ============================================================ 7. ANGOL CIM, ABSTRACT
cim(doc, "ENGLISH TITLE, ABSTRACT AND KEYWORDS", utana=6)
for b in bekezdesek(szakasz("## ENGLISH TITLE", "## TÁBLÁZATOK")):
    bekezdes(doc, b)
uj_oldal(doc)

# ============================================================ 8. TABLAZATOK
# A tablazatok a forras markdownbol keszulnek, igy nem tudnak elcsuszni tole.
tabl_blokk = szakasz("## TÁBLÁZATOK", "## ÁBRÁK ÉS ÁBRAALÁÍRÁSOK")
elso = True
for resz in re.split(r"^### ", tabl_blokk, flags=re.M)[1:]:
    sorok = resz.split("\n")
    if not elso:
        uj_oldal(doc)
    elso = False
    cim(doc, sorok[0].strip(), utana=6)
    buffer = []
    for sor in sorok[1:]:
        s2 = sor.strip()
        if s2.startswith("|"):
            cellak = [c.strip() for c in s2.strip("|").split("|")]
            if set("".join(cellak)) <= set("-: "):      # elvalaszto sor
                continue
            buffer.append(cellak)
            continue
        if buffer:                                       # a tabla veget ertuk
            tablazat(doc, buffer[0], buffer[1:])
            buffer = []
            doc.add_paragraph().paragraph_format.space_after = Pt(4)
        if s2 and not s2.startswith("---"):
            tiszta = re.sub(r"\*\*(.+?)\*\*", r"\1", s2).replace("*", "")
            bekezdes(doc, tiszta, dolt=s2.startswith("*"), meret=9, sorkoz=1.0)
    if buffer:
        tablazat(doc, buffer[0], buffer[1:])
uj_oldal(doc)

# ============================================================ 9. ABRAALAIRASOK
cim(doc, "ÁBRAALÁÍRÁSOK", utana=6)
for b in bekezdesek(szakasz("## ÁBRÁK ÉS ÁBRAALÁÍRÁSOK", "## MELLÉKLET")):
    p = bekezdes(doc, b, sorkoz=1.5)
    p.paragraph_format.space_after = Pt(8)
bekezdes(doc, "Mindhárom ábra színes; külön fájlban, 300 dpi TIFF és 600 dpi PNG "
              "formátumban kerül benyújtásra. Az ábrák szerkeszthető feliratokkal készültek, "
              "és fekete-fehér nyomtatásban is értelmezhetők, mert a színek mellett a "
              "vonalstílus és a sávpozíció is megkülönbözteti a három pályát.", dolt=True, meret=10)

doc.save(OUT)
print("elkeszult:", OUT)
