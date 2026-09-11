# 1. abra: GLP-1 receptor agonistak hatasa a serdulokori reproduktiv tengelyre
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

W, H = 11.0, 6.6
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

C_DRUG = "#1f4e79"
C_BOX  = "#f2f6fa"
C_EDGE = "#3d6f9e"
C_ACC  = "#a33b3b"
C_TXT  = "#12263a"

def box(x, y, w, h, title, lines, fc=C_BOX, ec=C_EDGE, tc=C_TXT, ts=9.2, ls=7.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.6",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h - 3.6, title, ha="center", va="top", fontsize=ts,
            fontweight="bold", color=tc)
    ax.text(x + w/2, y + h - 8.6, "\n".join(lines), ha="center", va="top",
            fontsize=ls, color=tc, linespacing=1.45)

def arrow(p1, p2, color=C_EDGE, lw=1.4, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=13,
                                 lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=2))

# --- kozponti elem ---
ax.add_patch(FancyBboxPatch((36, 44), 28, 15, boxstyle="round,pad=0.6,rounding_size=2",
                            fc=C_DRUG, ec=C_DRUG, lw=1.2))
ax.text(50, 54.5, "GLP-1 receptor agonista", ha="center", va="center",
        fontsize=11.5, fontweight="bold", color="white")
ax.text(50, 49.0, "liraglutid  ·  szemaglutid  ·  tirzepatid*",
        ha="center", va="center", fontsize=8.4, color="#d9e6f2")

# --- 5 hatasdomen ---
box(2.5, 74, 29, 22, "1. Testsúly és testösszetétel",
    ["BMI −16,1% (68 hét, 12–18 év)",
     "derékkörfogat, zsigeri zsír ↓",
     "ALT, lipidprofil javul",
     "a BMI-kategória visszalépése"])

box(35.5, 74, 29, 22, "2. Szteroidhormon-mintázat",
    ["szabad tesztoszteron ↓",
     "SHBG ↑ (inzulinrezisztencia ↓)",
     "androsztendion ↓",
     "perifériás ösztrogéntúlsúly ↓"])

box(68.5, 74, 29, 22, "3. Nemi érés és ciklus",
    ["menstruációs frekvencia ↑",
     "ovulációs ciklusok aránya ↑",
     "LH-csúcs modulációja (állat)",
     "pubertás időzítése: adat hiányos"])

box(2.5, 12, 29, 22, "4. Gyulladás",
    ["CRP-index ↓ (SMD −0,56)",
     "zsírszövet-eredetű citokinek ↓",
     "a testsúlytól részben független",
     "ízületi fájdalom mérséklődik"])

box(68.5, 12, 29, 22, "5. Longevity-tengely",
    ["kardiometabolikus rizikó ↓",
     "T2DM-konverzió késleltetése",
     "obesitas-asszociált daganatok",
     "expozíciós idő rövidül"])

# kozepso also doboz: kimenet
box(35.5, 12, 29, 22, "Reproduktív kimenet",
    ["PCOS-fenotípus enyhülése",
     "spontán fogamzóképesség ↑",
     "GDM / praeeclampsia kockázat ↓",
     "endometrium-védelem"], fc="#fdf3f3", ec=C_ACC)

# --- nyilak a kozponti elembol ---
arrow((44, 59), (20, 74))
arrow((50, 59), (50, 74))
arrow((56, 59), (80, 74))
arrow((44, 44), (20, 34))
arrow((56, 44), (80, 34))

# hatasdomenekbol a kimenet fele
arrow((17, 74), (40, 34), color=C_ACC, lw=1.1, rad=0.12)
arrow((50, 74), (50, 34), color=C_ACC, lw=1.1)
arrow((83, 74), (60, 34), color=C_ACC, lw=1.1, rad=-0.12)
arrow((26, 23), (35.5, 23), color=C_ACC, lw=1.1)
arrow((74, 23), (64.5, 23), color=C_ACC, lw=1.1)

ax.text(50, 5.2, "* a tirzepatid GIP/GLP-1 kettős agonista; 18 év alatt még nem törzskönyvezett indikáció",
        ha="center", va="center", fontsize=7.4, color="#5a6b7a", style="italic")

fig.savefig("1_abra_mechanizmus.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("1_abra_mechanizmus.tif", dpi=300, bbox_inches="tight", facecolor="white")
print("1. abra kesz")
