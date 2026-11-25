#!/usr/bin/env python3
"""Builds the guides, llms.txt and sitemap.xml of Tally's site (index, guide and privacy pages are edited by hand).

    python3 src/build_guides.py

Every number in the tables is computed here. Facts about the app follow README.md and docs/app-store.md in the app's repo.
"""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://coderalert0.github.io/tally-takeoff-site/"
APP_ID = "6822083779"
APP = f"https://apps.apple.com/us/app/id{APP_ID}"
UPDATED = "2026-11-24"
INDEXNOW = "5f0c1f7be2a94d6f9f4a3c0d8a61b27e"
GUIDES = []


def app_link(ct):
    return f"https://apps.apple.com/us/app/apple-store/id{APP_ID}?pt=128557981&ct={ct}&mt=8"


def table(head, rows):
    return ('<div class="table-scroll"><table class="g"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


def steps(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def guide(slug, title, short, desc, answer, body, faq):
    GUIDES.append(dict(slug=slug, title=title, short=short, desc=desc, answer=answer, body=body, faq=faq))


# --- 1 ---
guide("pdf-takeoff-on-ipad", "How to do a takeoff from a PDF plan on an iPad", "Takeoff from a PDF on an iPad",
      "Step by step: open the plan set, set each sheet's scale, count, measure runs and areas, price it and export. On an iPad, iPhone or Mac.",
      "<p>Open the plan set PDF in a takeoff app, set the scale of each sheet before measuring anything on it, then go trade by trade: count what is counted, trace what is measured in feet, outline what is measured in square feet. Check one known dimension on every sheet.</p>",
      steps(["<b>Get the PDF, not a picture of it.</b> A plan set saved from CAD has lines an app can snap to. A scan or a photo can still be measured, but taps land where you put them.",
             "<b>Import it and pick an item list</b> for your trade, so you are not typing item names on a ladder.",
             "<b>Set the scale of each sheet.</b> Use the scale printed on the sheet, or calibrate from a dimension you trust. Details and enlarged plans on the same sheet often have their own scale.",
             "<b>Check it.</b> Measure a second printed dimension. If it is off, the sheet was resized: calibrate from the dimension instead.",
             "<b>Count</b> symbols one item at a time across the sheet, so a missed corner shows.",
             "<b>Measure runs</b> (conduit, pipe, base, wall) by tapping along them, and <b>areas</b> (floor, slab, roof) by their corners. Cut out openings.",
             "<b>Split by floor or area</b> if you will be asked for it; it is far quicker now than later.",
             "<b>Price and export.</b> Add unit costs and waste, then overhead, profit and tax, and send the quantities to Excel or as a marked-up plan."])
      + "<h2>In Tally</h2><p>Tally does each of these on iPad, iPhone and Mac, offline, with no account. Taps snap to the drawing's own lines. Counting, measuring, markup and pricing are free on up to three takeoffs at a time; Find all, rooms in one tap and exports are in Tally Pro, a subscription with a 7-day free trial.</p>",
      [("Can I do a takeoff on an iPhone?", "Yes. Counting works well on a phone; tracing long runs is easier on an iPad or a Mac."),
       ("Do I need an internet connection?", "Not with Tally: the plan and the takeoff are on the device."),
       ("What if the plan is a scan?", "Calibrate from a printed dimension, and check a second one near the opposite corner: scans can be stretched.")])

# --- 2 ---
ARCH = [("3\"", 4), ("1 1/2\"", 8), ("1\"", 12), ("3/4\"", 16), ("1/2\"", 24), ("3/8\"", 32), ("1/4\"", 48), ("3/16\"", 64), ("1/8\"", 96), ("3/32\"", 128), ("1/16\"", 192)]
ENG = [10, 20, 30, 40, 50, 60, 100]


def inches(n):
    """n inches as feet and inches."""
    f, i = divmod(n, 12)
    return " ".join(([f"{f} ft"] if f else []) + ([f"{i} in"] if i else []))


guide("plan-scales", "Architectural and engineering plan scales, and how to set them", "Plan scales explained",
      "What 1/4\" = 1'-0\" and 1\" = 20' mean as ratios, how far an inch on the sheet is, and why a half-size set measures wrong.",
      "<p>A scale says how much real length one inch of the sheet stands for. 1/4\" = 1'-0\" means one inch is 4 feet, a ratio of 1:48. 1\" = 20' means one inch is 20 feet, 1:240. If the sheet was printed or saved at another size, the printed scale is wrong: calibrate from a dimension.</p>",
      "<h2>Architectural scales</h2>" + table(["Scale", "Ratio", "One inch on the sheet is"], [[f"{s} = 1'-0\"", f"1:{r}", inches(r)] for s, r in ARCH])
      + "<h2>Engineering scales</h2>" + table(["Scale", "Ratio", "One inch on the sheet is"], [[f"1\" = {n}'", f"1:{n*12}", f"{n} ft"] for n in ENG])
      + "<h2>Half-size sets</h2><p>An ARCH D sheet (36 by 24 in) printed on 17 by 11 in paper is a little under half size. On an exact half-size print, 1/4\" = 1'-0\" measures as 1/8\" = 1'-0\", so a length taken at the printed scale comes out half what it is, and an area a quarter. Look for a graphic scale bar: it shrinks with the sheet, so it stays true.</p>"
      + "<h2>How to check a scale</h2>" + steps(["Find the longest dimension string on the sheet.", "Measure it at the scale you set.", "Off by a fixed factor: the sheet was resized, so calibrate from that dimension.", "Right across and wrong up and down: the scan is stretched. Measure in each direction from a dimension in that direction."])
      + "<h2>In Tally</h2><p>Tally offers the scale printed on the sheet in one tap, the architectural and engineering presets, and calibration from a dimension typed as 20', 20' 6\" or 3.5 m. A scale can be copied to every sheet.</p>",
      [("What ratio is 1/8\" = 1'-0\"?", "1:96. One inch on the sheet is 8 feet."), ("What does NTS mean?", "Not to scale: do not measure it. Use the dimensions written on it."),
       ("Why are my areas about a quarter of what they should be?", "The sheet is at half size and measured at its full-size scale. Lengths come out half, so areas come out a quarter.")])

# --- 3 ---
def sf_per_cy(d):
    return 27 * 12 / d


CONC = [3, 3.5, 4, 5, 6, 8, 10, 12]
guide("concrete-cubic-yards-from-plans", "How to get cubic yards of concrete from a plan", "Concrete takeoff in cubic yards",
      "Area times depth over 324: the formula, how many square feet a cubic yard covers at each depth, footings and walls, and waste.",
      "<p>Cubic yards = area in square feet × depth in inches ÷ 324. A 4 inch slab takes one cubic yard for every 81 square feet. (324 is 27 cubic feet in a yard times 12 inches in a foot.)</p>",
      "<h2>What a cubic yard covers</h2>" + table(["Depth", "Square feet per cubic yard", "Cubic yards for 1,000 sq ft"], [[f"{d:g} in", f"{sf_per_cy(d):.1f}".rstrip('0').rstrip('.'), f"{1000*d/324:.2f}"] for d in CONC])
      + "<h2>Footings, walls and pads</h2>" + table(["Element", "Measure on the plan", "Cubic yards"], [
          ["Continuous footing", "Length in feet", "length × width (ft) × depth (ft) ÷ 27"], ["Foundation wall", "Length in feet", "length × height (ft) × thickness (in) ÷ 324"],
          ["Pad or pier footing", "Count", "count × length × width × depth (all in ft) ÷ 27"], ["Round pier", "Count", "count × 0.7854 × diameter² (ft) × depth (ft) ÷ 27"]])
      + f"<p>Example: a footing 120 ft long, 24 in wide and 12 in deep is 120 × 2 × 1 ÷ 27 = {120*2*1/27:.2f} cubic yards. A wall 120 ft long, 8 ft high and 8 in thick is 120 × 8 × 8 ÷ 324 = {120*8*8/324:.2f}.</p>"
      + "<h2>Before you order</h2>" + steps(["Take thickened edges, turn-downs and haunches separately; they are not in the slab's area.", "Subtract openings and pits, not small sleeves.", "Add waste for spillage, uneven grade and over-excavation. The amount is your judgment and depends on the subgrade; keep it as its own line.", "Round up to what the plant delivers."])
      + "<h2>In Tally</h2><p>Outline the slab, give the area item a depth in inches and it shows cubic yards, priced per yard if you like. Cut-outs are subtracted. Footings are runs and pads are counts.</p>",
      [("How many square feet does a yard of concrete cover at 4 inches?", "81 square feet."), ("And at 6 inches?", f"{sf_per_cy(6):g} square feet."), ("Why divide by 324?", "27 cubic feet make a cubic yard and 12 inches make a foot: 27 × 12 = 324.")])

# --- 4 ---
guide("drywall-takeoff-from-plans", "How to do a drywall takeoff from a floor plan", "Drywall takeoff",
      "Wall length times height times sides, less openings, plus ceilings, divided by the sheet's area. With sheet sizes and a worked example.",
      "<p>Wall area = length of wall × height × the number of sides that get board. Subtract large openings, add ceilings, add waste, and divide by the area of the sheet you hang: 32 square feet for 4×8, 48 for 4×12.</p>",
      "<h2>Sheets</h2>" + table(["Sheet", "Square feet", "Sheets for 1,000 sq ft, no waste"], [[f"4 × {n} ft", 4*n, f"{1000/(4*n):.1f}"] for n in (8, 9, 10, 12, 14)])
      + "<h2>Steps</h2>" + steps(["Read the wall types legend first. A partition with one layer each side and one with two layers on one side are different items.", "Trace each wall type as its own run, at the sheet's scale.", "Multiply by height. Board to deck and board to ceiling are different heights on the same plan; the sections say which.", "Multiply by sides, and by layers where the type calls for two.", "Take doors and windows off if you price labor by area; many leave small openings in because the cut-outs are waste.", "Outline ceilings by type from the reflected ceiling plan, not the floor plan."])
      + f"<h2>Worked example</h2><p>180 ft of partition, 9 ft high, one layer both sides: 180 × 9 × 2 = {180*9*2:,} sq ft. Take off six 3 × 7 ft doors on both sides: 6 × 21 × 2 = {6*21*2} sq ft, leaving {180*9*2-6*21*2:,}. With 10% for waste that is {(180*9*2-252)*1.1:,.0f} sq ft, or {-(-((180*9*2-252)*1.1)//48):.0f} sheets of 4 × 12.</p>"
      + "<h2>In Tally</h2><p>Give a run a wall height and it totals wall area as well as length; waste is per item. Starter lists include drywall and framing, and a count of sheets or studs can hang off each item as an assembly.</p>",
      [("How many square feet is a 4×12 sheet?", "48."), ("Do I subtract doors and windows?", "It depends on how you price. Taking out large openings is usual; leaving small ones in covers cutting waste. Do the same on every job."),
       ("Where do ceiling areas come from?", "The reflected ceiling plan, which shows each ceiling type's extent.")])

# --- 5 ---
guide("count-symbols-on-electrical-plans", "How to count fixtures and devices on electrical plans", "Counting electrical symbols",
      "Read the legend, count one symbol at a time, sheet by sheet, and catch what is missed: type letters, look-alikes, enlarged plans and risers.",
      "<p>Start from the legend and fixture schedule, count one symbol at a time across a whole sheet, and mark each as you go, so what is left unmarked is what you have missed. Then compare your totals with the schedule and the panel schedules.</p>",
      steps(["<b>Read the legend and the abbreviations.</b> The same circle can be a receptacle, a junction box or a smoke detector on different jobs.",
             "<b>Split by type letter.</b> A 2×4 troffer tagged A and one tagged A-EM are two items.",
             "<b>One symbol, one whole sheet.</b> Jumping between symbols is how devices are counted twice.",
             "<b>Mark what you count.</b> On paper a highlighter; in an app, a mark on each one, or the counted ones covered up.",
             "<b>Watch for repeats.</b> Enlarged plans, unit plans and typical floors show the same devices again. Count a typical unit once and multiply.",
             "<b>Check details and risers</b> for devices no floor plan shows: rooftop disconnects, panels, fire alarm risers.",
             "<b>Compare</b> with the fixture schedule's types: a type with no count is the first place to look."])
      + "<h2>Look-alikes</h2>" + table(["Easily confused", "Tell them apart by"], [["Duplex and quad receptacles", "Number of lines or a filled half; check the legend"], ["GFCI and weatherproof duplex", "The letters beside it: GFI, WP"], ["Single-pole, 3-way and dimmer switches", "The subscript: S, S3, SD"], ["Exhaust fan and light-fan", "The tag and the mechanical plan"]])
      + "<h2>In Tally</h2><p>Tap a symbol and it is counted. Find all (Tally Pro) looks for copies of one you tap, rotated ones included, and proposes them for you to check and add in one step; it works best on plans saved from CAD and finds fewer on scans and photos. Hide counted covers what you have done, so what is left stands out.</p>",
      [("Can software count every symbol by itself?", "Not reliably. Treat what it proposes as a first pass and check it, above all on scans."), ("How do I handle typical floors?", "Count one and multiply, and note which sheets you multiplied."),
       ("Why don't my counts match the schedule?", "Common causes are enlarged plans counted twice, alternates, and devices shown only on a riser or detail.")])

ICON = 'icons.svg'
CSS = """<style>
.g-wrap{max-width:780px;margin:0 auto;padding:32px 20px 64px;line-height:1.65}
.g-wrap h1{font-size:clamp(1.7rem,4.6vw,2.5rem);line-height:1.2;margin:.2em 0 .5em}
.g-wrap h2{margin:1.6em 0 .5em}
.g-wrap li{margin:.45em 0}
.g-answer{border-left:4px solid #f5a623;padding:4px 0 4px 18px;margin:18px 0}
.table-scroll{overflow-x:auto}
table.g{border-collapse:collapse;width:100%;font-size:.95em}
table.g th,table.g td{border-bottom:1px solid rgba(128,128,128,.35);padding:8px 10px;text-align:left;vertical-align:top}
.g-cta{margin:34px 0 10px;padding:20px 22px;border:1px solid rgba(128,128,128,.35);border-radius:14px}
.g-meta{opacity:.7;font-size:.9em}
</style>"""


def page(g):
    others = [x for x in GUIDES if x is not g]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "dateModified": UPDATED, "datePublished": UPDATED,
           "mainEntityOfPage": BASE + g["slug"] + ".html", "author": {"@type": "Organization", "name": "Construction Takeoff - Tally"}},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(g['title'], quote=False)}</title>
<meta name="description" content="{html.escape(g['desc'])}">
<link rel="canonical" href="{BASE}{g['slug']}.html">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta name="theme-color" content="#0b1a30">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="icon.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{CSS}
</head>
<body>
<header class="topbar"><div class="topbar-in">
  <a class="brand" href="./"><img src="icon.png" alt=""><span>Tally</span></a>
  <nav class="nav" aria-label="Site"><a href="./">Home</a><a href="guide.html">User guide</a><a href="./#guides" aria-current="page">Guides</a><a href="privacy.html">Privacy</a></nav>
</div></header>
<main class="g-wrap">
<h1>{g['title']}</h1>
<div class="g-answer">{g['answer']}</div>
{g['body']}
<h2>Questions</h2>
{''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in g['faq'])}
<div class="g-cta"><b>Construction Takeoff - Tally</b><p>Count, measure and price plans on iPad, iPhone and Mac. Free on up to three takeoffs at a time.</p>
<a class="btn btn-primary" href="{html.escape(app_link('guide-' + g['slug'][:22]))}">Get Tally on the App Store</a></div>
<h2>More guides</h2><ul>{''.join(f'<li><a href="{x["slug"]}.html">{x["title"]}</a></li>' for x in others)}</ul>
<p class="g-meta">Updated November 24, 2026. Check quantities against the drawings and specifications before you bid.</p>
</main>
<footer class="site-footer"><div class="in"><a class="brand" href="./"><img src="icon.png" alt=""><span>Construction Takeoff - Tally</span></a>
<nav aria-label="Footer"><a href="./">Home</a><a href="guide.html">User guide</a><a href="privacy.html">Privacy Policy</a></nav></div></footer>
</body>
</html>
"""


def strip(s):
    import re
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


for g in GUIDES:
    (ROOT / f"{g['slug']}.html").write_text(page(g))
facts = ["Platforms: iPad and iPhone (iOS 17 or later) and Mac (macOS 14 or later). One App Store purchase covers them.",
         "Opens PDF plan sets, and JPEG, PNG or HEIC plan images. Works offline with no account; takeoffs sync through the user's own iCloud.",
         "Set scale from the sheet's printed scale, architectural or engineering presets, or calibration from a dimension; metric supported.",
         "Counts, linear runs with arcs, areas with cut-outs, wall height, roof pitch, volumes in cubic yards, assemblies, waste, overhead, profit and tax, zones.",
         "Markup: cloud, arrow, callout, note, highlight, pen, stamp, photo, dimension; tracked as a punch list.",
         "Free: counting, measuring, markup and pricing on up to three takeoffs at a time; every Pro feature works on the sample plan.",
         "Tally Pro (monthly or yearly subscription, 7-day free trial): Find all, rooms in one tap, exports (Excel, CSV, PDF report, marked-up plan), printing, revised sets, unlimited takeoffs.",
         "In English and Spanish."]
(ROOT / "llms.txt").write_text(f"# Construction Takeoff - Tally\n\n> A construction takeoff app for iPad, iPhone and Mac: open a plan set PDF, set the scale, count, measure, mark up and price it on the sheet.\n\nApp Store: {APP}\n\n## Facts\n"
                               + "".join(f"- {f}\n" for f in facts) + "\n## Pages\n" + f"- [Home and support]({BASE})\n- [User guide]({BASE}guide.html)\n- [Privacy]({BASE}privacy.html)\n"
                               + "".join(f"- [{g['title']}]({BASE}{g['slug']}.html): {g['desc']}\n" for g in GUIDES))
(ROOT / "llms-full.txt").write_text("# Construction Takeoff - Tally\n\n" + "".join(f"- {f}\n" for f in facts)
                                    + "".join(f"\n## {g['title']}\n\n{strip(g['answer'])}\n\n{strip(g['body'])}\n\n" + "".join(f"Q: {q}\nA: {a}\n" for q, a in g['faq']) for g in GUIDES))
urls = ["", "guide.html", "privacy.html"] + [g["slug"] + ".html" for g in GUIDES]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
(ROOT / f"{INDEXNOW}.txt").write_text(INDEXNOW)
print("guides", len(GUIDES), "urls", len(urls))
