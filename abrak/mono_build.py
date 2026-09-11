# Fekete-feher (szurkearnyalatos) valtozat eloallitasa a negy abrabol.
# A szerzoi utmutato fekete-feher ertelmezhetoseget is elvar, ezert minden
# szinliteralt megkulonboztetheto vilagossagu szurkere cserelunk, a vonalakat
# pedig vonaltipussal is elkulonitjuk.
import pathlib, runpy

SZURKE = {
    # eredeti (1-3. abra) paletta
    "#1f4e79": "#262626", "#3d6f9e": "#666666", "#2a5d8f": "#404040",
    "#12263a": "#000000", "#a33b3b": "#1a1a1a", "#b4453a": "#8c8c8c",
    "#3f7a48": "#5e5e5e", "#f2f6fa": "#f4f4f4", "#fdf3f3": "#e9e9e9",
    "#eef7ef": "#fbfbfb", "#fdf0ee": "#f0f0f0", "#eef3fa": "#e4e4e4",
    "#f2c3bd": "#dcdcdc", "#d9e6f2": "#e0e0e0", "#cfe0ef": "#e0e0e0",
    "#5a6b7a": "#4d4d4d", "#dde4ea": "#cccccc", "#fbfcfd": "#fdfdfd",
    "#e3e8ee": "#dcdcdc", "#7fb3d5": "#a8a8a8", "#c9d6e4": "#d4d4d4",
    # 4. abra palettaja
    "#0E6E76": "#1f1f1f", "#C0503C": "#8c8c8c", "#C98A20": "#5e5e5e",
    "#6B5296": "#707070", "#4F7A57": "#3d3d3d",
    "#e9f3f4": "#f2f2f2", "#f4fafa": "#fafafa", "#fcf4e4": "#ededed",
    "#fefaf2": "#fbfbfb", "#f2eff7": "#f0f0f0", "#f9f7fc": "#fafafa",
    "#fbeeeb": "#eaeaea", "#fdf6f4": "#f7f7f7", "#eef4ef": "#f4f4f4",
    "#cfe8ea": "#e6e6e6",
}

# a 3. abra vonalait vonaltipussal is elkulonitjuk
VONAL3 = [
    ('ax2.plot(KOR, A, lw=2.2, color="#3f7a48"',
     'ax2.plot(KOR, A, lw=1.9, ls=(0, (1, 1.2)), color="#3f7a48"'),
    ('ax2.plot(KOR, B, lw=2.4, color="#b4453a"',
     'ax2.plot(KOR, B, lw=2.2, ls=(0, (6, 2)), color="#b4453a"'),
    ('for ar, szin, ls in ((5000, "#7fb3d5", "-"), (20000, "#2a5d8f", "-"), (35000, "#12263a", "--")):',
     'for ar, szin, ls in ((5000, "#7fb3d5", (0, (3, 1, 1, 1))), (20000, "#2a5d8f", "-"), (35000, "#12263a", (0, (5, 2, 1, 2)))):'),
]

SCRIPTS = [
    ("abra1_mechanizmus.py",        "1_abra_mechanizmus"),
    ("abra2_eletut_flowchart.py",   "2_abra_eletut_flowchart"),
    ("abra3_megelozes_koltseg.py",  "3_abra_megelozes_koltseg"),
    ("abra4_biokemiai_kaszkad.py",  "4_abra_biokemiai_kaszkad"),
]

here = pathlib.Path(__file__).parent
for src, alap in SCRIPTS:
    kod = (here / src).read_text(encoding="utf-8")
    if src.startswith("abra3"):
        for a, b in VONAL3:
            kod = kod.replace(a, b)
    for szin, szurke in SZURKE.items():
        kod = kod.replace(szin, szurke)
    kod = kod.replace(f'"{alap}.png"', f'"{alap}_bw.png"')
    kod = kod.replace(f'"{alap}.tif"', f'"{alap}_bw.tif"')
    kod = kod.replace('open("../ellenorzes/gazdasagi_modell.json","w",encoding="utf-8")',
                      'open("../ellenorzes/gazdasagi_modell_bw_dummy.json","w",encoding="utf-8")')
    tmp = here / f"_bw_{src}"
    tmp.write_text(kod, encoding="utf-8")
    runpy.run_path(str(tmp), run_name="__main__")
    tmp.unlink()
    print("kesz:", alap + "_bw")
(here / "../ellenorzes/gazdasagi_modell_bw_dummy.json").unlink(missing_ok=True)
