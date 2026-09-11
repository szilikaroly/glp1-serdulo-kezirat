# 2. abra: Eletut flow-chart - harom palya 8 evtol 65+ eves korig
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

fig, ax = plt.subplots(figsize=(15.5, 8.6))
ax.set_xlim(0, 160); ax.set_ylim(0, 92); ax.axis("off")

GREEN_F, GREEN_E = "#eef7ef", "#3f7a48"
RED_F,   RED_E   = "#fdf0ee", "#b4453a"
BLUE_F,  BLUE_E  = "#eef3fa", "#2a5d8f"
TXT = "#12263a"

EPOCHS = [
    ("8–12 év",  "praepubertas /\nkorai pubertas"),
    ("12–18 év", "serdülőkor"),
    ("18–30 év", "reproduktív kor"),
    ("30–45 év", "fertilitási ablak"),
    ("45–65 év", "peri- és\nposztmenopauza"),
    ("65+ év",   "időskor"),
]
X0, COLW, GAP = 16.0, 22.4, 1.6
def cx(i): return X0 + i*(COLW+GAP)

# --- fejlecsav ---
for i, (age, lab) in enumerate(EPOCHS):
    ax.add_patch(FancyBboxPatch((cx(i), 79.5), COLW, 9.0,
                 boxstyle="round,pad=0.35,rounding_size=1.2",
                 fc="#1f4e79", ec="#1f4e79"))
    ax.text(cx(i)+COLW/2, 86.0, age, ha="center", va="center",
            fontsize=10.2, fontweight="bold", color="white")
    ax.text(cx(i)+COLW/2, 82.0, lab, ha="center", va="center",
            fontsize=7.2, color="#cfe0ef", linespacing=1.2)

LANES = [
    ("A", "Normál testalkatú\nleány",            GREEN_F, GREEN_E, 57.0),
    ("B", "Obes leány\n(kezelés nélkül)",        RED_F,   RED_E,   33.0),
    ("C", "Obes leány\nGLP-1RA + tartós\nfenntartás", BLUE_F, BLUE_E, 8.5),
]
LANE_H = 17.5

CONTENT = {
"A": [
 ["BMI 50–75. pc","menarche ~12,5 év","alacsony hsCRP"],
 ["ovulációs ciklusok","normoandrogén állapot","alacsony zsigeri zsír"],
 ["PCOS-rizikó: alap","spontán fogamzás","endometriosis: alap-rizikó"],
 ["GDM-rizikó: alap","hypertonia: ritka","T2DM: ritka"],
 ["menopauza ~51 év","endometriumcarcinoma:\nalap-rizikó","mozgásszervi panasz: alap"],
 ["megtartott funkció","alacsony gyógyszerteher"],
],
"B": [
 ["BMI ≥ 97. pc","korai adrenarche /\nkorai menarche","hsCRP ↑"],
 ["oligo-/amenorrhoea","hyperandrogenismus","MASLD, dyslipidaemia"],
 ["PCOS-fenotípus rögzül","anovulációs infertilitás","endometrium-hyperplasia"],
 ["GDM, praeeclampsia","T2DM megjelenése","hypertonia"],
 ["endometrium- és\nemlőcarcinoma ↑","autoimmun és\nmozgásszervi terhek"],
 ["halmozott polymorbiditás","rövidebb egészségben\ntöltött évek"],
],
"C": [
 ["BMI-trajektória megtörik","érés időzítése:\nmonitorozandó","hsCRP ↓"],
 ["BMI −16%","ciklus regularizálódik","androgének ↓, SHBG ↑"],
 ["PCOS enyhébb fenotípus","spontán fogamzás ↑","washout a koncepció előtt"],
 ["GDM-rizikó ↓","T2DM késleltetve","vérnyomás ↓"],
 ["daganatos expozíciós\nidő rövidül","ízületi terhelés ↓"],
 ["megtartott funkció","fenntartó kezelés\nköltsége marad"],
],
}

for key, label, fc, ec, y in LANES:
    ax.add_patch(Rectangle((0.9, y-1.2), 157.5, LANE_H+2.4, fc="#fbfcfd",
                           ec="#dde4ea", lw=0.8, zorder=0))
    ax.add_patch(FancyBboxPatch((1.6, y), 13.4, LANE_H,
                 boxstyle="round,pad=0.35,rounding_size=1.2", fc=ec, ec=ec))
    ax.text(8.3, y+LANE_H/2, label, ha="center", va="center", fontsize=7.0,
            fontweight="bold", color="white", linespacing=1.35)
    for i in range(6):
        ax.add_patch(FancyBboxPatch((cx(i), y), COLW, LANE_H,
                     boxstyle="round,pad=0.35,rounding_size=1.2",
                     fc=fc, ec=ec, lw=1.0))
        items = CONTENT[key][i]
        ax.text(cx(i)+COLW/2, y+LANE_H/2,
                "\n".join("• "+s for s in items),
                ha="center", va="center", fontsize=7.2, color=TXT, linespacing=1.9)
        if i < 5:
            ax.add_patch(FancyArrowPatch((cx(i)+COLW+0.2, y+LANE_H/2),
                                         (cx(i+1)-0.2, y+LANE_H/2),
                                         arrowstyle="-|>", mutation_scale=10,
                                         lw=1.1, color=ec))

# B -> C atteres nyil
ax.add_patch(FancyArrowPatch((cx(1)+COLW/2, 33.0), (cx(1)+COLW/2, 8.5+LANE_H),
             arrowstyle="-|>", mutation_scale=13, lw=1.8, color="#2a5d8f",
             connectionstyle="arc3,rad=0.0"))
ax.text(cx(1)+COLW/2+1.2, 29.0, "terápiás beavatkozás", ha="left", va="center",
        fontsize=7.4, color="#2a5d8f", fontweight="bold", rotation=0)

ax.text(80, 3.0,
        "A pályák a jelenlegi bizonyítékokból levezetett, szemléltető kockázati trajektóriák; "
        "nem egyéni prognózis és nem mért incidenciaértékek.",
        ha="center", va="center", fontsize=7.4, color="#5a6b7a", style="italic")

fig.savefig("2_abra_eletut_flowchart.png", dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig("2_abra_eletut_flowchart.tif", dpi=300, bbox_inches="tight", facecolor="white")
print("2. abra kesz")
