# 4. abra: Az inkretintengely biokemiai kaszkadja a reproduktiv axis fele
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

fig, ax = plt.subplots(figsize=(15.2, 9.2))
ax.set_xlim(0, 158); ax.set_ylim(0, 100); ax.axis("off")

TXT   = "#12263a"
NAVY  = "#0E6E76"
CORAL = "#C0503C"
AMBER = "#C98A20"
VIOL  = "#6B5296"
SAGE  = "#4F7A57"
GREY  = "#5a6b7a"

def doboz(x, y, w, h, sorok, ec, fc, fs=7.9, bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.4",
                                fc=fc, ec=ec, lw=1.2))
    if bold_first:
        ax.text(x + w/2, y + h - 2.6, sorok[0], ha="center", va="top",
                fontsize=fs + 0.5, fontweight="bold", color=ec)
        if len(sorok) > 1:
            ax.text(x + w/2, y + h - 7.0, "\n".join(sorok[1:]), ha="center", va="top",
                    fontsize=fs, color=TXT, linespacing=1.55)
    else:
        ax.text(x + w/2, y + h/2, "\n".join(sorok), ha="center", va="center",
                fontsize=fs, color=TXT, linespacing=1.55)

def nyil(p1, p2, color, lw=1.5, ls="-", rad=0.0, style="-|>"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=13, lw=lw,
                                 color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=3, shrinkB=3))

# ================= forras =================
ax.add_patch(FancyBboxPatch((1.5, 34), 22, 34, boxstyle="round,pad=0.5,rounding_size=1.6",
                            fc="#0E6E76", ec="#0E6E76"))
ax.text(12.5, 64.5, "Inkretintengely", ha="center", va="top", fontsize=10.2,
        fontweight="bold", color="white")
ax.text(12.5, 59.5, "bél L-sejt → GLP-1\nbél K-sejt → GIP\nDPP-4: t½ ≈ 2 perc\n\nanalóg: t½ órák–1 hét\n(zsírsav-konjugáció,\nalbuminkötés)",
        ha="center", va="top", fontsize=7.6, color="#cfe8ea", linespacing=1.5)

# ================= 5 utvonal =================
X1, W1 = 29.0, 32.0      # kozepso oszlop
X2, W2 = 66.0, 38.0      # biokemiai lepes
X3, W3 = 108.0, 42.0     # reproduktiv kimenet

# --- 1. hepatikus-metabolikus ---
doboz(X1, 78, W1, 18, ["1. Hepatikus-metabolikus út",
                       "zsigeri zsír ↓ · májzsír ↓",
                       "de novo lipogenezis ↓"], NAVY, "#e9f3f4")
doboz(X2, 78, W2, 18, ["HNF-4α ↑  →  SHBG-promoter ↑",
                       "SHBG ↑  →  szabad tesztoszteron ↓",
                       "(az összes tesztoszteron alig változik)"], NAVY, "#f4fafa")
doboz(X3, 78, W3, 18, ["Hyperandrogen fenotípus enyhül",
                       "acne, hirsutismus ↓",
                       "ovulációs ciklusok aránya ↑"], NAVY, "#e9f3f4")

# --- 2. leptin-kisspeptin ---
doboz(X1, 57, W1, 18, ["2. Zsírszövet–leptin út",
                       "zsírtömeg ↓  →  leptin ↓",
                       "(permisszív jel gyengül)"], AMBER, "#fcf4e4")
doboz(X2, 57, W2, 18, ["POMC → α-MSH → MC3/4R",
                       "→ Kiss1-neuron (nucl. arcuatus)",
                       "→ GnRH-pulzus → LH, FSH"], AMBER, "#fefaf2")
doboz(X3, 57, W3, 18, ["A nemi érés időzítése",
                       "a pubertás késleltetése lehetséges",
                       "humán adat inkretin mellett: nincs"], AMBER, "#fcf4e4")

# --- 3. kozvetlen gonadalis (hipotezis) ---
doboz(X1, 36, W1, 18, ["3. Közvetlen gonadális út",
                       "GLP-1R: hypothalamus, hypophysis,",
                       "ovarium (rágcsáló)"], VIOL, "#f2eff7")
doboz(X2, 36, W2, 18, ["preovulációs LH-csúcs ×2",
                       "érett tüszők száma ↑",
                       "humán juvenilis GLP-1R: nem igazolt"], VIOL, "#f9f7fc")
doboz(X3, 36, W3, 18, ["HIPOTÉZIS",
                       "a ciklusrendeződés egy része",
                       "innen is származhat"], VIOL, "#f2eff7")

# --- 4. gyulladas ---
doboz(X1, 15, W1, 18, ["4. Gyulladásos út",
                       "zsírszöveti makrofág-aktiváció ↓",
                       "IL-6 ↓ · TNF-α ↓ (nem mért)"], CORAL, "#fbeeeb")
doboz(X2, 15, W2, 18, ["hepatikus CRP ↓  (SMD −0,56)",
                       "adiponektin/leptin arány ↑",
                       "= downstream marker, nem mechanizmus"], CORAL, "#fdf6f4")
doboz(X3, 15, W3, 18, ["Endometrium- és peritonealis",
                       "mikrokörnyezet: nem vizsgált",
                       "mediációs elemzés szükséges"], CORAL, "#fbeeeb")

# --- 5. ellentetes irany ---
ax.add_patch(Rectangle((X1 - 1.2, 1.0), W3 + X3 - X1 + 3.4, 11.0, fc="#eef4ef",
                       ec=SAGE, lw=1.2, zorder=0))
ax.text(X1 + 1.0, 9.6, "5. Ellentétes irányú mechanizmus —  alacsony energia-hozzáférhetőség",
        ha="left", va="center", fontsize=8.6, fontweight="bold", color=SAGE)
ax.text(X1 + 1.0, 4.8,
        "gyors, nagy mértékű fogyás + tartósan alacsony energiabevitel  →  a GnRH-pulzusgenerátor gátlása  →  "
        "funkcionális hypothalamicus amenorrhoea.\nUgyanaz a leptin–kisspeptin lánc, ellenkező előjellel. "
        "Serdülőkorban, éretlen pulzusgenerátor mellett a kockázat elvben nagyobb — egyik vizsgálat sem mérte.",
        ha="left", va="center", fontsize=7.6, color=TXT, linespacing=1.6)

# ================= nyilak =================
for y, c in ((87, NAVY), (66, AMBER), (45, VIOL), (24, CORAL)):
    nyil((23.5, 51), (X1 - 0.4, y), c, lw=1.5, rad=0.0)
    ls = "--" if c == VIOL else "-"
    nyil((X1 + W1 + 0.4, y), (X2 - 0.4, y), c, lw=1.5, ls=ls)
    nyil((X2 + W2 + 0.4, y), (X3 - 0.4, y), c, lw=1.5, ls=ls)

# 5 ellenirany: a jobb margon felfele, dobozok erintese nelkul
nyil((X3 + W3 + 1.2, 12.2), (X3 + W3 + 1.2, 64), SAGE, lw=1.8, ls="--")
nyil((X3 + W3 + 1.2, 64), (X3 + W3 + 0.4, 66), SAGE, lw=1.8, ls="--")
ax.text(X3 + W3 + 2.6, 38, "ellentétes irány", rotation=90, ha="center", va="center",
        fontsize=7.6, color=SAGE, fontweight="bold")

ax.text(79, 97.5, "A vastag nyilak dokumentált, a szaggatott nyilak feltételezett útvonalat jelölnek.",
        ha="center", va="center", fontsize=7.8, color=GREY, style="italic")

fig.savefig("4_abra_biokemiai_kaszkad.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("4_abra_biokemiai_kaszkad.tif", dpi=300, bbox_inches="tight", facecolor="white")
print("4. abra kesz")
