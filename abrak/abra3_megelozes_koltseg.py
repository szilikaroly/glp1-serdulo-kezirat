# 3. abra: Mi elozheto meg, mennyi tarsadalmi koltseggel, es mennyire biztos
# MINDEN ERTEK SZEMLELTETO MODELLEREDMENY, nem mert incidencia es nem mert koltseg.
# Tarsadalmi perspektiva: kozvetlen ellatas + munkahelyi tavolletek + reprodukcios veszteseg.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, json

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

# ============================ MODELL-FELTETELEZESEK ==========================
# kohorsz: 1000 obes leany, belepes 14 evesen, kovetes 65 eves korig, HUF, 2025
KOR        = np.arange(14, 66)
DISZKONT   = 0.03
HATAS      = 0.60     # a testsulymediált tobbletkockazat elharult hanyada
ACM_EXTRA  = 0.15     # tovabbi, fogyastol fuggetlen kockazatcsokkenes (LDL, glukoz, CRP, vernyomas)
ADHERENCIA = 1.00
AR_HAVI    = 20000.0  # Ft/ho (alapeset); a vizsgalt sav 5 000 - 35 000 Ft/ho
NAPIBER    = 30000.0  # Ft/munkanap, jarulekokkal (tarsadalmi ertek)

# --- kozvetlen ellatas (Ft/ev) ---
alap      = 40_000 + 3_600 * (KOR - 14) ** 1.25              # A palya
tobblet_B = 35_000 + 5_400 * (KOR - 14) ** 1.32              # obesitasra visszavezetheto
# a tobbletbol a kardiometabolikus hanyad, amelyre a fogyasfuggetlen hatas is vonatkozik
cm_hanyad = np.clip((KOR - 35) / 30.0, 0, 1) * 0.55          # 35 ev felett no, max 55%

# --- munkahelyi tavolletek (absenteizmus) ---
# obesitasra visszavezetheto tobblet-betegnapok/ev, csak munkaban toltott evekben
tobblet_nap = np.where(KOR >= 18, np.clip(1.0 + 0.18 * (KOR - 18), 0, 10), 0.0)
absent_B    = tobblet_nap * NAPIBER

# --- reprodukcios veszteseg ---
# anovulacios infertilitas miatti tobblet-ART ciklusok + GDM-szovodmenyes terhesseg
# + a kezelessel toltott ido munkabol valo kieses; 25-40 ev kozott oszolva
ART_CIKLUS   = 1_500_000.0   # Ft/ciklus (tarsadalmi koltseg, betegteherrel)
GDM_TOBBLET  =   600_000.0   # Ft/terhesseg
ART_TOBBLET_ARANY = 0.21     # B palyan a nok 21%-a igenyel ART-t (2. tablazat)
GDM_ARANY         = 0.18
ART_CIKLUS_SZAM   = 1.8
repro_evek = (KOR >= 25) & (KOR <= 40)
repro_B = np.where(repro_evek,
                   (ART_TOBBLET_ARANY * ART_CIKLUS_SZAM * ART_CIKLUS +
                    GDM_ARANY * GDM_TOBBLET) / repro_evek.sum(), 0.0)

def palyak(hatas=HATAS, acm=ACM_EXTRA, adh=ADHERENCIA, ar_havi=AR_HAVI,
           disz=DISZKONT, indirekt=True):
    dd = 1.0 / (1.0 + disz) ** (KOR - 14)
    # a kezeles ket uton csokkenti a tobbletet: testsulymediált + fogyasfuggetlen
    megmarad = (1 - hatas * adh) * (1 - acm * adh * cm_hanyad)
    tob_C   = tobblet_B * megmarad
    abs_C   = absent_B  * megmarad
    rep_C   = repro_B   * (1 - hatas * adh)      # reprodukcios ut: testsulymediált
    gysz    = ar_havi * 12 * adh
    if not indirekt:
        aB = np.zeros_like(absent_B); aC = np.zeros_like(absent_B)
        rB = np.zeros_like(repro_B);  rC = np.zeros_like(repro_B)
    else:
        aB, aC, rB, rC = absent_B, abs_C, repro_B, rep_C
    A = np.cumsum(alap * dd) / 1e6
    B = np.cumsum((alap + tobblet_B + aB + rB) * dd) / 1e6
    C = np.cumsum((alap + tob_C + aC + rC + gysz) * dd) / 1e6
    return A, B, C

def netto(**kw):
    A, B, C = palyak(**kw)
    return C[-1] - B[-1]          # millio Ft/fo; negativ = megtakaritas

def kuszobar(indirekt=True, **kw):
    """Az a havi ar (Ft), amelynel a netto merleg nulla."""
    lo, hi = 0.0, 200_000.0
    for _ in range(60):
        k = (lo + hi) / 2
        if netto(ar_havi=k, indirekt=indirekt, **kw) < 0: lo = k
        else: hi = k
    return (lo + hi) / 2

A, B, C = palyak()
NETTO      = netto()
KUSZOB     = kuszobar()
KUSZOB_DIR = kuszobar(indirekt=False)

esemenyek = [
    ("PCOS-fenotípus\n(klinikai diagnózis)",        420, 0.55),
    ("Anovulációs infertilitás\n(kezelést igénylő)",210, 0.55),
    ("Gestatiós diabetes",                          180, 0.60),
    ("Hypertensiv kórkép",                          340, 0.55),
    ("2-es típusú diabetes",                        260, 0.65),
    ("Endometrium- és\nemlőcarcinoma",               72, 0.35),
    ("Mozgásszervi / autoimmun\nterhelés (kezelt)", 300, 0.45),
]

fig = plt.figure(figsize=(24.0, 9.6))
gs = fig.add_gridspec(2, 3, wspace=0.30, hspace=0.44)

# ---------------- (a) elharithato esemenyek ----------------
ax1 = fig.add_subplot(gs[0, 0])
cim = [e[0] for e in esemenyek]
Bv  = np.array([e[1] for e in esemenyek], float)
Cv  = Bv * (1 - np.array([e[2] for e in esemenyek], float) * HATAS)
y   = np.arange(len(cim))[::-1]
ax1.barh(y, Bv, height=0.62, color="#f2c3bd", edgecolor="#b4453a", lw=1.0,
         label="B pálya – obesitas, kezelés nélkül")
ax1.barh(y, Cv, height=0.62, color="#2a5d8f", edgecolor="#1f4e79", lw=1.0,
         label="C pálya – GLP-1RA + tartós fenntartás")
for yi, b, c in zip(y, Bv, Cv):
    ax1.text(b + 8, yi, f"−{int(round(b-c))}", va="center", ha="left",
             fontsize=8.4, color="#b4453a", fontweight="bold")
ax1.set_yticks(y); ax1.set_yticklabels(cim, fontsize=8.0)
ax1.set_xlabel("Esemény 1000 nőre, 14–65 éves kor között (modellezett)", fontsize=8.8)
ax1.set_xlim(0, max(Bv) * 1.55); ax1.set_ylim(-1.15, len(cim) - 0.4)
ax1.set_title("(a)  Elhárítható vagy késleltethető megbetegedések",
              fontsize=10.4, fontweight="bold", loc="left", color="#12263a")
ax1.legend(fontsize=7.6, loc="lower right", bbox_to_anchor=(1.0, -0.02), framealpha=0.95)
ax1.spines[["top", "right"]].set_visible(False)
ax1.grid(axis="x", lw=0.5, color="#e3e8ee"); ax1.set_axisbelow(True)

# ---------------- (b) kumulalt tarsadalmi koltseg ----------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(KOR, A, lw=2.2, color="#3f7a48", label="A – normál testalkat")
ax2.plot(KOR, B, lw=2.4, color="#b4453a", label="B – obesitas, kezelés nélkül")
for ar, szin, ls in ((5000, "#7fb3d5", "-"), (20000, "#2a5d8f", "-"), (35000, "#12263a", "--")):
    _, _, Ci = palyak(ar_havi=ar)
    ax2.plot(KOR, Ci, lw=1.9, color=szin, ls=ls, label=f"C – {ar:,} Ft/hó".replace(",", " "))
ax2.set_xlabel("Életkor (év)", fontsize=8.8)
ax2.set_ylabel("Kumulált, diszkontált társadalmi költség\n(millió Ft/fő)", fontsize=8.8)
ax2.set_title("(b)  Élettartamra vetített társadalmi költség",
              fontsize=10.4, fontweight="bold", loc="left", color="#12263a")
ax2.legend(fontsize=7.4, loc="upper left", framealpha=0.95)
ax2.spines[["top", "right"]].set_visible(False)
ax2.grid(lw=0.5, color="#e3e8ee"); ax2.set_axisbelow(True); ax2.set_xlim(14, 65)

# ---------------- (c) az ar hatasa ----------------
ax3 = fig.add_subplot(gs[0, 2])
arak = np.linspace(5000, 35000, 120)
n_tarsadalmi = [netto(ar_havi=a) for a in arak]
n_direkt     = [netto(ar_havi=a, indirekt=False) for a in arak]
ax3.plot(arak, n_tarsadalmi, lw=2.4, color="#2a5d8f",
         label="társadalmi perspektíva\n(+ absenteizmus, reprodukciós veszteség)")
ax3.plot(arak, n_direkt, lw=2.0, color="#b4453a", ls="--",
         label="csak közvetlen ellátási költség")
ax3.axhline(0, color="#5a6b7a", lw=1.0, ls=":")
ax3.fill_between(arak, n_tarsadalmi, 0, where=(np.array(n_tarsadalmi) < 0),
                 color="#3f7a48", alpha=0.14)
for kv, szin in ((KUSZOB, "#2a5d8f"), (KUSZOB_DIR, "#b4453a")):
    if 5000 <= kv <= 35000:
        ax3.plot([kv], [0], "o", ms=7, color=szin, zorder=5)
        ax3.annotate(f"{kv:,.0f} Ft/hó".replace(",", " "), xy=(kv, 0),
                     xytext=(kv, max(n_tarsadalmi) * 0.30), ha="center", fontsize=8.0,
                     color=szin, fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color=szin, lw=0.9))
ax3.set_xlabel("A GLP-1 receptor agonista havi ára (Ft)", fontsize=8.8)
ax3.set_ylabel("Nettó élettartam-mérleg a B pályához képest\n(millió Ft/fő; negatív = megtakarítás)",
               fontsize=8.8)
ax3.set_title("(c)  A megtérülés ára", fontsize=10.4, fontweight="bold",
              loc="left", color="#12263a")
ax3.legend(fontsize=7.4, loc="upper left", framealpha=0.95)
ax3.spines[["top", "right"]].set_visible(False)
ax3.grid(lw=0.5, color="#e3e8ee"); ax3.set_axisbelow(True)
ax3.set_xlim(5000, 35000)
ax3.set_xticks([5000, 10000, 15000, 20000, 25000, 30000, 35000])
ax3.set_xticklabels(["5 000", "10 000", "15 000", "20 000", "25 000", "30 000", "35 000"], fontsize=8)

# ---------------- (d) egyiranyu erzekenysegi elemzes ----------------
ax4 = fig.add_subplot(gs[1, 0])
param = [
    ("Havi ár\n5 000–35 000 Ft",          dict(ar_havi=5000.0),  dict(ar_havi=35000.0)),
    ("Testsúlymediált hatás\n40–80%",     dict(hatas=0.80),      dict(hatas=0.40)),
    ("Fogyásfüggetlen hatás\n0–30%",      dict(acm=0.30),        dict(acm=0.00)),
    ("Adherencia\n50–100%",               dict(adh=0.50),        dict(adh=1.00)),
    ("Indirekt költségek\nbe / ki",       dict(indirekt=True),   dict(indirekt=False)),
    ("Diszkontráta\n0–5%",                dict(disz=0.00),       dict(disz=0.05)),
]
cimkek, lo, hi = [], [], []
for nev, kedv, ellen in param:
    cimkek.append(nev); lo.append(netto(**kedv)); hi.append(netto(**ellen))
yy = np.arange(len(cimkek))[::-1]
for yi, l, h in zip(yy, lo, hi):
    ax4.plot([l, h], [yi, yi], lw=9, color="#c9d6e4", solid_capstyle="butt", zorder=1)
    ax4.plot([l], [yi], "o", ms=7, color="#3f7a48", zorder=3)
    ax4.plot([h], [yi], "o", ms=7, color="#b4453a", zorder=3)
ax4.axvline(NETTO, color="#1f4e79", lw=1.6, zorder=2)
ax4.axvline(0, color="#5a6b7a", lw=1.0, ls=":", zorder=2)
ax4.annotate(f"alapeset {NETTO:+.1f}", xy=(NETTO, 0.02), xycoords=("data", "axes fraction"),
             xytext=(6, 0), textcoords="offset points", ha="left", va="bottom",
             fontsize=7.8, color="#1f4e79", fontweight="bold")
ax4.set_yticks(yy); ax4.set_yticklabels(cimkek, fontsize=7.8)
ax4.set_xlabel("Nettó élettartam-mérleg (millió Ft/fő; negatív = megtakarítás)", fontsize=8.8)
ax4.set_ylim(-1.25, len(cimkek) - 0.30)
ax4.set_title("(d)  Egyirányú érzékenységi elemzés", fontsize=10.4,
              fontweight="bold", loc="left", color="#12263a")
ax4.spines[["top", "right", "left"]].set_visible(False)
ax4.grid(axis="x", lw=0.5, color="#e3e8ee"); ax4.set_axisbelow(True)


# ---------------- (e) valoszinusegi erzekenysegi elemzes (PSA) ----------------
ax5 = fig.add_subplot(gs[1, 1])
rng = np.random.default_rng(20260911)
N = 4000

def psa_netto(ar_havi, minta):
    """Vektorizalt netto merleg N parameterhuzasra, adott havi aron."""
    hatas, acm, adh, k_dir, k_abs, k_rep = minta
    dd = 1.0 / (1.0 + DISZKONT) ** (KOR - 14)
    ki = np.empty(len(hatas))
    for i in range(len(hatas)):
        megmarad = (1 - hatas[i] * adh[i]) * (1 - acm[i] * adh[i] * cm_hanyad)
        tB = tobblet_B * k_dir[i]; aB = absent_B * k_abs[i]; rB = repro_B * k_rep[i]
        dC = (tB * megmarad + aB * megmarad + rB * (1 - hatas[i] * adh[i])
              + ar_havi * 12 * adh[i])
        ki[i] = np.sum((dC - (tB + aB + rB)) * dd) / 1e6
    return ki

minta = (
    np.clip(rng.normal(0.60, 0.10, N), 0.30, 0.85),      # testsulymediált hatas
    np.clip(rng.normal(0.15, 0.08, N), 0.00, 0.35),      # fogyasfuggetlen hatas
    np.clip(rng.normal(0.75, 0.15, N), 0.30, 1.00),      # adherencia
    np.clip(rng.normal(1.00, 0.25, N), 0.40, 2.00),      # kozvetlen koltseg szorzo
    np.clip(rng.normal(1.00, 0.35, N), 0.20, 2.50),      # absenteizmus szorzo
    np.clip(rng.normal(1.00, 0.35, N), 0.20, 2.50),      # reprodukcios veszteseg szorzo
)
arak_psa = np.linspace(5000, 35000, 25)
p_megtak = np.array([np.mean(psa_netto(a, minta) < 0) for a in arak_psa])
ax5.plot(arak_psa, p_megtak * 100, lw=2.6, color="#2a5d8f")
ax5.fill_between(arak_psa, 0, p_megtak * 100, color="#2a5d8f", alpha=0.12)
ax5.axhline(50, color="#5a6b7a", lw=1.0, ls=":")
# az 50%-os atmetszes
if p_megtak.min() < 0.5 < p_megtak.max():
    k50 = np.interp(0.5, p_megtak[::-1], arak_psa[::-1])
    ax5.plot([k50], [50], "o", ms=7, color="#b4453a", zorder=5)
    ax5.annotate(f"50%: {k50:,.0f} Ft/hó".replace(",", " "), xy=(k50, 50),
                 xytext=(k50 * 0.99, 74), ha="center", fontsize=8.2,
                 color="#b4453a", fontweight="bold",
                 arrowprops=dict(arrowstyle="-", color="#b4453a", lw=0.9))
ax5.set_xlabel("A GLP-1 receptor agonista havi ára (Ft)", fontsize=8.8)
ax5.set_ylabel("A megtakarítás valószínűsége (%)", fontsize=8.8)
ax5.set_title("(e)  Valószínűségi érzékenységi elemzés", fontsize=10.4,
              fontweight="bold", loc="left", color="#12263a")
ax5.set_xlim(5000, 35000); ax5.set_ylim(0, 100)
ax5.set_xticks([5000, 15000, 25000, 35000])
ax5.set_xticklabels(["5 000", "15 000", "25 000", "35 000"], fontsize=8)
ax5.spines[["top", "right"]].set_visible(False)
ax5.grid(lw=0.5, color="#e3e8ee"); ax5.set_axisbelow(True)
ax5.text(0.97, 0.05, f"{N} Monte Carlo-futtatás", transform=ax5.transAxes,
         ha="right", va="bottom", fontsize=7.4, color="#5a6b7a", style="italic")

# ---------------- (f) a modell feltetelezesei ----------------
ax6 = fig.add_subplot(gs[1, 2]); ax6.axis("off")
ax6.set_title("(f)  A modell feltételezései", fontsize=10.4, fontweight="bold",
              loc="left", color="#12263a")
FELTETELEZESEK = [
    'Kohorsz  1000 obes leány, belépés 14 évesen, követés 65 éves korig',
    'Perspektíva  társadalmi; 3%/év diszkontálás; 2025-ös magyar árszint',
    '',
    'KÖLTSÉGTÉTELEK',
    '  1  közvetlen ellátás (obesitasra visszavezethető többlet)',
    '  2  munkahelyi távollétek: többlet-betegnapok × 30 000 Ft/nap,',
    '      18 éves kortól, évi legfeljebb 10 nap',
    '  3  reprodukciós veszteség: többlet ART-ciklusok (1,5 M Ft/ciklus,',
    '      1,8 ciklus, a nők 21%-a) + GDM-mel szövődött terhesség',
    '      (0,6 M Ft, 18%), a 25–40 éves sávban elosztva',
    '',
    'KEZELÉSI HATÁS',
    '  testsúlymediált  a többletkockázat 60%-a hárul el',
    '  fogyásfüggetlen  további 15% a kardiometabolikus hányadra',
    '      (35 év felett növekvő, legfeljebb 55%)',
    '  adherencia  alapeset 100%, a PSA-ban átlag 75%',
    '',
    'A PSA HÚZÁSAI (normális eloszlás, csonkítva)',
    '  testsúlymediált hatás  0,60 ± 0,10',
    '  fogyásfüggetlen hatás  0,15 ± 0,08',
    '  adherencia  0,75 ± 0,15',
    '  költségszorzók  1,00 ± 0,25 (direkt) / ± 0,35 (indirekt)',
    '',
    'NEM SZEREPEL A MODELLBEN',
    '  QALY-értékelés · a mellékhatások kezelésének költsége ·',
    '  a nyert életévek monetizálása · magyar regiszteradat',
]
ax6.text(0.0, 1.00, "\n".join(FELTETELEZESEK),
         transform=ax6.transAxes, ha="left", va="top", fontsize=6.8,
         color="#12263a", linespacing=1.52, family="DejaVu Sans")

fig.text(0.5, 0.015,
         "Szemléltető modelleredmény a 3. táblázatban közölt feltételezésekkel; nem mért incidencia- és nem mért költségadat. "
         "A fogyásfüggetlen hatás felnőtt, kardiovaszkuláris betegségben szenvedő populáció adatából származik, serdülőkori átültetése feltételezés. "
         "A valószínűségi elemzés a paraméterek együttes bizonytalanságát mutatja, a modell szerkezeti bizonytalanságát nem.",
         ha="center", va="top", fontsize=7.6, color="#5a6b7a", style="italic")

fig.savefig("3_abra_megelozes_koltseg.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("3_abra_megelozes_koltseg.tif", dpi=300, bbox_inches="tight", facecolor="white")

out = {
 "penznem": "millio Ft/fo, 3%/ev diszkontalva, tarsadalmi perspektiva",
 "alapeset_ar_Ft_ho": AR_HAVI,
 "kumulalt": {"A": round(A[-1],2), "B": round(B[-1],2), "C": round(C[-1],2)},
 "netto_alapeset": round(NETTO,2),
 "kuszobar_Ft_ho_tarsadalmi": round(KUSZOB),
 "kuszobar_Ft_ho_csak_direkt": round(KUSZOB_DIR),
 "netto_5000Ft": round(netto(ar_havi=5000.0),2),
 "netto_35000Ft": round(netto(ar_havi=35000.0),2),
 "netto_5000Ft_csak_direkt": round(netto(ar_havi=5000.0, indirekt=False),2),
 "netto_35000Ft_csak_direkt": round(netto(ar_havi=35000.0, indirekt=False),2),
 "erzekenyseg": {cimkek[i].replace("\n"," "): [round(lo[i],2), round(hi[i],2)] for i in range(len(cimkek))},
 "elharitott_esemeny_1000_nore": int(round((Bv-Cv).sum())),
 "psa_megtakaritas_valoszinusege": {str(int(a)): round(float(v), 3) for a, v in zip(arak_psa, p_megtak)},
}
print(json.dumps(out, ensure_ascii=False, indent=1))
open("../ellenorzes/gazdasagi_modell.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1))
