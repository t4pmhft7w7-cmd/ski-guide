"""Builds the Ski Guide website (GitHub Pages): privacy.html from ../ios/PRIVACY.md, plus the support page and the icon.
Run after changing the policy:  python ski-guide-site/build.py   then commit and push this folder."""
import html, os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
md = open(os.path.join(ROOT, "ios", "PRIVACY.md"), encoding="utf-8").read()

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"([\w.+-]+@[\w-]+\.[\w.]+)", r'<a href="mailto:\1">\1</a>', s)
    return s

out, lines, i = [], md.splitlines(), 0
while i < len(lines):
    l = lines[i]
    if l.startswith("# "): out.append(f"<h1>{inline(l[2:])}</h1>")
    elif l.startswith("## "): out.append(f"<h2>{inline(l[3:])}</h2>")
    elif l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"): rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
        head, body = rows[0], [r for r in rows[2:]]
        out.append('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                   + "".join("<tr>" + "".join(f'<td data-h="{html.escape(head[k])}">{inline(c)}</td>' for k, c in enumerate(r)) + "</tr>" for r in body) + "</tbody></table></div>")
        continue
    elif l.startswith("- "):
        items = []
        while i < len(lines) and lines[i].startswith("- "): items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
        out.append("<ul>" + "".join(items) + "</ul>"); continue
    elif l.strip(): out.append(f"<p>{inline(l)}</p>")
    i += 1

def page(title, desc, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="icon" href="icon.png"><link rel="stylesheet" href="style.css">
</head><body><header><a class="brand" href="./"><img src="icon.png" alt="" width="40" height="40"><span>Ski Guide</span></a>
<nav><a href="./">Support</a><a href="privacy.html">Privacy</a></nav></header>
<main>{body}</main>
<footer>Ski Guide · <a href="mailto:jani.jesenovecj@gmail.com">jani.jesenovecj@gmail.com</a></footer></body></html>
"""

open(os.path.join(HERE, "privacy.html"), "w", encoding="utf-8").write(page("Ski Guide Privacy Policy", "How the Ski Guide iPhone app handles your data.", "\n".join(out)))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page("Ski Guide Support", "Help and contact for the Ski Guide iPhone app.", """
<h1>Ski Guide</h1>
<p class="lead">3D maps of ski mountains with live wind, snowpack and runs, your ski stats and badges, Ski sessions you can replay, and friends on the mountain.</p>
<h2>Support</h2>
<p>Questions, bug reports or feedback: email <a href="mailto:jani.jesenovecj@gmail.com">jani.jesenovecj@gmail.com</a>. We usually answer within a few days.</p>
<h2>Common questions</h2>
<ul>
<li><strong>My location isn't showing.</strong> Turn on <strong>My location</strong> in the app, and allow location for Ski Guide in Settings › Privacy &amp; Security › Location Services.</li>
<li><strong>Friends or posts don't load.</strong> Social features use your iCloud account: check you're signed in to iCloud in Settings and have a connection.</li>
<li><strong>Restoring purchases.</strong> In the app, open a paywall (Ski Together or the Ski Trip Planner) and tap <strong>Restore purchases</strong>.</li>
<li><strong>Reporting a person or a post.</strong> Use <strong>Report</strong> on a friend request, a friend's stats, or a post's ••• menu, or email us.</li>
<li><strong>Deleting your account.</strong> In the app: Friends › Add friend › <strong>Delete my account</strong>. See the <a href="privacy.html">privacy policy</a> for what's removed.</li>
</ul>
<h2>Data sources</h2>
<p>Weather and snow: NOAA / National Weather Service and NOHRSC. Terrain and imagery: USGS. Ski runs, lifts and lodges: © OpenStreetMap contributors (ODbL). Resort names identify places only; Ski Guide isn't affiliated with any resort.</p>
"""))
shutil.copy(os.path.join(ROOT, "ios", "branding", "SkiGuide-AppStore-1024.png"), os.path.join(HERE, "icon.png"))
print("site built:", HERE)
