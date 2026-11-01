import json, os, urllib.request
user = os.environ.get("LOGIN", "MuhammadFaizan-prog")
tok = os.environ["GH_TOKEN"]
def get(url):
    r = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(r))
repos, page = [], 1
while True:
    b = get(f"https://api.github.com/users/{user}/repos?per_page=100&page={page}&type=owner")
    repos += b
    if len(b) < 100: break
    page += 1
totals = {}
for r in repos:
    if r.get("fork"): continue
    for k, v in get(r["languages_url"]).items():
        totals[k] = totals.get(k, 0) + v
colors = {"TypeScript":"#3178c6","JavaScript":"#f1e05a","Python":"#3572A5","HTML":"#e34c26","CSS":"#563d7c","Rust":"#dea584","Java":"#b07219","Dart":"#00B4AB","Kotlin":"#A97BFF","Swift":"#F05138","Go":"#00ADD8","Shell":"#89e051","PLpgSQL":"#336790","C++":"#f34b7d","C":"#555555","Jupyter Notebook":"#DA5B0B","Vue":"#41b883","SCSS":"#c6538c","PHP":"#4F5D95","Dockerfile":"#384d54"}
top = sorted(totals.items(), key=lambda x: -x[1])[:8]
s = sum(v for _, v in top) or 1
W, H = 495, 175
x, bar = 25, ""
for k, v in top:
    w = (W - 50) * v / s
    bar += f'<rect x="{x:.1f}" y="52" width="{w:.1f}" height="8" fill="{colors.get(k,"#BB2ACF")}"/>'
    x += w
items = ""
for i, (k, v) in enumerate(top):
    cx, cy = 25 + (i % 2) * 230, 85 + (i // 2) * 24
    items += f'<circle cx="{cx+5}" cy="{cy-4}" r="5" fill="{colors.get(k,"#BB2ACF")}"/><text x="{cx+16}" y="{cy}" class="t">{k} {100*v/s:.1f}%</text>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>.h{{font:600 18px 'Segoe UI',Ubuntu,sans-serif;fill:#ffffff}}.t{{font:400 12px 'Segoe UI',Ubuntu,sans-serif;fill:#daf7dc}}</style>
<rect width="{W}" height="{H}" rx="6" fill="#151515"/>
<text x="25" y="35" class="h">Most Used Languages</text>
<clipPath id="c"><rect x="25" y="52" width="{W-50}" height="8" rx="4"/></clipPath><g clip-path="url(#c)">{bar}</g>
{items}
</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/top-langs.svg", "w").write(svg)
print(top)
