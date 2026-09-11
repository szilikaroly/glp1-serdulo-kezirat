## MELLÉKLET: KÉPPROMPTOK (nem a kézirat része)

*A melléklet két csoportot tartalmaz. Az **A. csoport** a közlésre szánt négy ábra részletes, szerkezeti leírása — olyan pontossággal, hogy generatív képalkotó rendszer vagy grafikus kollégát bevonva az ábra újraépíthető legyen belőle. A **B. csoport** szabad, illusztratív képekre való, a közlemény tartalmának vizuális összefoglalására.*

*Figyelem: a Magyar Nőorvosok Lapja szerzői útmutatója tiltja a prezentációra jellemző díszítést, és több kiadó külön tiltja a generatív úton előállított ábrákat. A közlésre szánt 1–4. ábra ezért adatvezérelten, szerkeszthető feliratokkal, matplotlib-bel készült (a forráskód a repóban), 600 dpi PNG és 300 dpi TIFF formátumban, színes és szürkeárnyalatos változatban egyaránt. Az alábbi promptok a kommunikációs másodfelhasználást szolgálják — előadás, poszter, sajtóanyag —, nem a beküldött ábrákat helyettesítik.*

---

## KÖZÖS STÍLUSMEGKÖTÉS

Minden prompthoz hozzáfűzendő:

> Full colour, richly saturated but harmonious palette — deep teal (#0E6E76), warm coral (#C0503C), golden amber (#C98A20), soft violet (#6B5296), sage green (#4F7A57) — on a warm off-white ground (#FAF7F2). Modern medical-editorial illustration: flat vector with subtle gradient shading, clean geometry, generous negative space. Crisp hairline rules, rounded-rectangle containers with 1 px coloured borders. No photorealism, no stock-photo clichés, no drop shadows, no watermarks. High resolution, print quality.

**Feliratokról:** az A. csoport promptjaiban a feliratok szándékosan szerepelnek, mert az ábra szerkezete nélkülük értelmetlen. Generatív rendszerek a szöveget rendszerint elrontják, ezért az A. csoport ajánlott használata: a képet **felirat nélkül** generáltatni (a prompt végére: *„no text or lettering anywhere in the image"*), majd a feliratokat vektoros szerkesztőben ráhelyezni.

---

# A. CSOPORT — A KÖZLEMÉNY NÉGY ÁBRÁJA

## A1 prompt – 1. ábra: öt hatásdomén és közös kimenetük

> A radial concept diagram on a warm off-white ground, landscape 5:3. **Centre:** a wide rounded-rectangle panel in solid deep teal, containing a two-line white caption block (upper line large and bold, lower line small and pale) — this is the drug node. **Five satellite panels** in rounded rectangles with thin coloured borders and very pale tinted fills, arranged around the centre: three across the top edge, two across the bottom-left and bottom-right corners. Each satellite has a bold coloured heading line and four short body lines beneath it. **A sixth panel**, bottom centre, is visually distinct — warm coral border and a pale coral fill instead of the blue-grey of the others — marking the shared outcome. **Arrows:** five straight teal arrows radiate from the central panel to the five satellites; five coral arrows converge from the satellites into the bottom-centre outcome panel, two of them curving gently around the central node without touching it. Arrowheads are slim and filled. A small italic footnote line runs along the bottom edge. Balanced, symmetric, textbook-clean.

## A2 prompt – 2. ábra: életút flow-chart, három pálya

> A three-lane horizontal swimlane diagram on a warm off-white ground, wide 16:9. **Top:** a row of six deep-teal rounded header tabs of equal width, evenly spaced, each containing a bold white line over a smaller pale-blue line. **Below:** three horizontal lanes, each on a barely-tinted background strip with a hairline border. Each lane begins on the left with a tall solid-colour rounded label block — the first lane sage green, the second terracotta, the third deep blue — followed by six pale rounded content cards aligned under the header tabs. The cards carry three short bulleted lines each, vertically centred. Small solid arrowheads connect consecutive cards within each lane, in the lane's own colour. **One vertical arrow**, heavier than the rest and deep blue, drops from the second card of the middle lane down into the second card of the bottom lane, with a short bold label beside it. A single italic caption line runs across the bottom. The visual logic: the top lane stays calm and green, the middle lane accumulates terracotta density, the bottom lane cools back toward blue.

## A3 prompt – 3. ábra: hatpaneles egészséggazdasági tabló

> A six-panel analytical figure laid out as two rows of three, on a warm off-white ground, very wide 8:3. Each panel has a small bold left-aligned title prefixed by a bracketed letter. **Panel (a):** a horizontal bar chart, seven rows, each row a long pale-coral bar with a shorter deep-blue bar overlaid from the same left baseline; a small bold coral number sits just past the end of each pale bar. Two-line row labels on the left, a legend box in the lower right. **Panel (b):** a line chart with five smooth rising curves — one sage green staying low, one terracotta rising steeply, and three blues of increasing darkness, the darkest dashed; legend upper left. **Panel (c):** two straight rising lines crossing a dotted horizontal zero line — one solid blue, one dashed terracotta — with a pale green shaded wedge beneath the zero line on the left; two small filled circles mark where each line crosses zero, each with a short bold label on a thin leader line. **Panel (d):** a tornado diagram — six horizontal pale-grey capsules, each with a sage-green dot at one end and a terracotta dot at the other, a solid vertical navy reference line and a dotted vertical zero line. **Panel (e):** a single thick blue S-curve falling from top-left to bottom-right, the area beneath it pale blue, a dotted horizontal line at mid-height, and one coral dot where the curve crosses it, labelled on a thin leader. **Panel (f):** no axes at all — a dense left-aligned block of small plain text with short all-caps sub-headings, reading as a specification sheet. A long italic caption spans the full width beneath everything.

## A4 prompt – 4. ábra: biokémiai kaszkád

> A left-to-right cascade diagram on a warm off-white ground, landscape 5:3. **Far left:** a tall solid deep-teal rounded panel, vertically centred, carrying a bold white heading and a small pale multi-line body — the source node. **To its right: four horizontal rows**, each a triplet of pale rounded cards connected left to right by two arrows. Each row has its own colour identity applied to the card borders, the headings and the arrows: row one deep teal, row two golden amber, row three soft violet, row four warm coral. The violet row's arrows and borders are **dashed** rather than solid, marking it as hypothetical; its third card carries a single bold all-caps word. Each card has a bold coloured heading over two smaller dark body lines. **Four coloured arrows** fan out from the right edge of the source panel to the first card of each row. **Beneath all four rows:** a wide pale sage-green banner with a hairline border, a bold sage heading and two lines of smaller body text. **On the far right margin:** a long dashed sage-green arrow runs from the banner vertically upward alongside the cards, turning inward at the top toward the second row, with a small rotated bold label beside it. A small italic note sits above the whole diagram.

---

# B. CSOPORT — ILLUSZTRATÍV KÉPEK

## B1 prompt – A metabolikus gyökér

> A stylised adolescent female silhouette rendered in deep teal at the centre of a warm off-white field. From her abdominal region, luminous coral and amber filaments radiate outward to five glowing nodes arranged in a wide circle, each node a different colour and a different abstract motif: a cluster of soft spheres, an interlocking ring pair, an unfurling bud, a radiating warm halo, and a long tapering ribbon receding into the distance. Colour-coded connections, luminous gradient glow at each node. No text or lettering anywhere in the image.

## B2 prompt – A biokémiai kaszkád, szabadon

> A luminous four-lane molecular cascade flowing left to right across a warm off-white ground. At the far left, a deep-teal gut wall releases two glowing peptide ribbons that pass through a fracturing enzyme motif and re-form as longer, fatty-acid-tailed molecules bound to a large albumin sphere. The four lanes then diverge in distinct colours: a teal hepatic lane where a shrinking lipid droplet lets a transcription-factor ribbon rise and a globular carrier protein bloom, releasing a bound steroid molecule; an amber adipose lane where a shrinking fat cell dims a signalling halo that travels through a chain of three neurons into a pulsing hypothalamic node; a violet lane of dashed, uncertain filaments touching a small pituitary sphere and an ovarian follicle; and a coral lane where macrophage forms retreat from fat tissue and a liver protein marker fades. Every molecule abstract and geometric, never photorealistic. No text or lettering anywhere in the image.

## B3 prompt – A hormonális mérleg (SHBG és a szabad androgén)

> A luminous balance-scale composition on a warm off-white ground. On one side, a cluster of small golden-amber steroid molecules floats free; on the other, the same molecules are captured inside large translucent teal carrier spheres. Between them, a liver form rendered in deep teal glows from within as a bright transcription-factor ribbon unwinds, while a shrinking lipid droplet fades to pale violet beneath it. The free-molecule side visibly rises. Abstract, geometric, flat vector with gradient glow. No text or lettering anywhere in the image.

## B4 prompt – A megtört trajektória

> Two diverging curved ribbons rising from a single bright amber point low on the left. The upper ribbon steepens and deepens into saturated coral and crimson, growing thicker and more turbulent as it climbs to the right. The lower ribbon bends flat, cooling into teal and sage, thinning and smoothing as it travels right. Small colour-coded abstract glyphs float along each ribbon suggesting clinical milestones — a cycle spiral, a rounded pregnancy form, a joint hinge, a dividing cell. Luminous gradients, warm off-white ground. No text or lettering anywhere in the image.

## B5 prompt – A kétirányú tengely

> A single vertical luminous axis on a warm off-white ground, with a bright sage-green node at its centre representing a pulse generator. From the left, a heavy golden-amber mass presses inward and the node glows too brightly, over-saturated; from the right, the amber mass has almost vanished and the node dims to a faint cold violet. A narrow band of balanced, healthy teal light sits between the two extremes. Luminous gradient composition, abstract and geometric, no figures. No text or lettering anywhere in the image.

## B6 prompt – Az életút-mérleg

> A long horizontal timeline sweeping left to right across a warm off-white ground, splitting midway into two branches: the upper branch thickens into dense stacked blocks of coral and crimson rising like a bar landscape, the lower branch stays slender in teal and sage with far fewer, lower blocks. A translucent amber wedge fills the widening gap between the two branches, and a thin violet line traces a third, intermediate path. Abstract, colour-coded, luminous flat-vector style, no currency symbols. No text or lettering anywhere in the image.

## B7 prompt – A gondozási keret

> Four abstract human figures without faces arranged around a luminous circular table, each rendered in a distinct saturated colour — deep teal, sage green, warm coral and soft violet — connected by glowing amber lines to a small bright core at the centre of the table. Concentric translucent rings ripple outward from the core. Warm off-white ground, flat vector with gradient glow, no medical equipment. No text or lettering anywhere in the image.

## B8 prompt – A folytonosság feltétele

> A smooth descending ribbon in cool teal that thins, fractures into a dotted amber segment midway, then swells and rises again in saturated coral toward the right edge. A soft violet shadow trails beneath the rising portion. Abstract, minimal, luminous flat-vector composition on a warm off-white ground, generous negative space, no figures. No text or lettering anywhere in the image.
