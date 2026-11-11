#!/usr/bin/env python3
"""Bouwt de artikelpagina's in stories/ uit tools/stories.json.

Gebruik (vanuit de hoofdmap van de site):  python3 tools/build_stories.py
Tekst aanpassen doe je in tools/stories.json, daarna dit script opnieuw draaien.
"""
import html
import json
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://cltrhead.com/"

try:
    from PIL import Image
except ImportError:  # zonder Pillow krijgen foto's een vaste verhouding
    Image = None

CSS = """
:root{--bg:#f1eee8;--ink:#161614;--mute:#77736b;--line:rgba(22,22,20,.18);--mono:'Courier Prime','Courier New',monospace;--serif:'Newsreader',Georgia,serif;--hand:'Reenie Beanie','Segoe Script',cursive}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:16px/1.8 var(--mono);overflow-x:hidden}
a{color:inherit}
header{position:fixed;inset:0 0 auto 0;z-index:30;display:flex;justify-content:space-between;padding:28px;mix-blend-mode:difference;color:#fff;font-size:12px;letter-spacing:.06em;text-transform:uppercase;line-height:1.55}
header a{text-decoration:none}
header nav{display:flex;gap:26px}
.ph{background:linear-gradient(160deg,#3a352f,#1b1917);overflow:hidden}
.ph img,.ph video{width:100%;height:100%;object-fit:cover;display:block}
.hero{min-height:100svh;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6vw;padding:120px 28px 56px;align-items:end}
.hero .l{display:flex;flex-direction:column;justify-content:space-between;min-height:calc(100svh - 176px)}
.vol{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.name{font-family:var(--serif);font-weight:400;font-size:clamp(48px,8vw,128px);line-height:.95;letter-spacing:-.02em;margin:3vh 0 2vh;text-wrap:balance}
.name.long{font-size:clamp(38px,5.4vw,88px)}
.role{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.hq{font-family:var(--serif);font-style:italic;font-size:clamp(22px,2.3vw,34px);line-height:1.25;max-width:20em;margin-top:5vh;text-wrap:balance}
.scroll{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-top:4vh}
.hero .r .ph{aspect-ratio:9/16;height:calc(100svh - 176px);max-height:760px}
.intro{max-width:880px;margin:0 auto;padding:12vh 28px 12vh;font-family:var(--serif);font-size:clamp(24px,2.6vw,36px);line-height:1.35;text-align:center;text-wrap:balance}
.main{display:grid;grid-template-columns:260px minmax(0,640px);gap:6vw;justify-content:center;padding:0 28px 12vh}
.main.solo{grid-template-columns:minmax(0,640px)}
.side{position:sticky;top:96px;align-self:start;font-size:12px;letter-spacing:.04em;text-transform:uppercase;line-height:1.5}
.side ol{list-style:none;margin-bottom:34px}
.side li{border-top:1px solid var(--line)}
.side li:last-child{border-bottom:1px solid var(--line)}
.side a{display:flex;gap:12px;padding:9px 0;text-decoration:none;color:var(--mute);transition:color .2s}
.side a span{min-width:2ch}
.side a.on,.side a:hover{color:var(--ink)}
.about{text-transform:none;letter-spacing:0;font-size:13px;line-height:1.65;color:var(--mute)}
.about b{display:block;font-weight:400;text-transform:uppercase;letter-spacing:.06em;font-size:11px;color:var(--ink);margin-bottom:6px}
.sec{padding-top:8vh;scroll-margin-top:40px}
.sec:first-child{padding-top:0}
.sec h2{font-weight:400;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin-bottom:22px;display:flex;gap:12px}
.sec p{margin-bottom:1.15em}
.sec p.first{font-size:18px}
blockquote{font-family:var(--serif);font-style:italic;font-size:clamp(26px,2.9vw,40px);line-height:1.2;letter-spacing:-.01em;margin:5vh 0;text-wrap:balance}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:6vh 0}
.pair.one{grid-template-columns:1fr}
.src{margin-top:8vh;padding-top:18px;border-top:1px solid var(--line);font-size:12px;color:var(--mute);line-height:1.7}
.sign{font-family:var(--hand);font-size:clamp(34px,3.4vw,48px);line-height:.9;transform:rotate(-2deg);transform-origin:left;margin-top:8vh}
.next{border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr}
.next a{padding:6vh 28px;text-decoration:none;display:flex;flex-direction:column;gap:8px;transition:background .25s}
.next a:hover{background:rgba(22,22,20,.05)}
.next a+a{text-align:right;border-left:1px solid var(--line)}
.next small{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.next strong{font-family:var(--serif);font-weight:400;font-size:clamp(24px,3vw,44px);line-height:1.1}
footer{display:flex;justify-content:space-between;padding:28px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);border-top:1px solid var(--line)}
footer a{text-decoration:none}
@media (max-width:860px){
 header{padding:20px}
 .hero{grid-template-columns:1fr;padding:96px 20px 40px;gap:32px;align-items:start}
 .hero .l{min-height:0}
 .hero .r .ph{height:auto;max-height:none;width:min(100%,340px)}
 .hq{margin-top:4vh}
 .intro{padding:8vh 20px 8vh}
 .main,.main.solo{grid-template-columns:minmax(0,1fr);gap:0;padding:0 20px 10vh}
 .side{position:static;margin-bottom:8vh}
 .next{grid-template-columns:1fr}
 .next a{padding:4vh 20px}
 .next a+a{text-align:left;border-left:0;border-top:1px solid var(--line)}
 footer{padding:20px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

JS = """
var secs=[].slice.call(document.querySelectorAll('.sec[id]')),links=[].slice.call(document.querySelectorAll('#toc a'));
function spy(){var y=window.innerHeight*.35,cur=0;secs.forEach(function(s,i){if(s.getBoundingClientRect().top<y)cur=i});links.forEach(function(a,i){a.classList.toggle('on',i===cur)})}
if(links.length){addEventListener('scroll',spy,{passive:true});spy()}
[].forEach.call(document.querySelectorAll('img'),function(i){i.addEventListener('error',function(){var p=i.closest('.pair');i.parentNode.style.display='none';if(p&&!p.querySelector('.ph:not([style*=none])'))p.style.display='none'})});
"""


def esc(text):
    return html.escape(text, quote=False)


def asset(name):
    return "../" + quote(name)


def ratio(files):
    """Gezamenlijke beeldverhouding voor een fotopaar: de minst hoge van de twee."""
    best = None
    if Image:
        for f in files:
            try:
                w, h = Image.open(os.path.join(ROOT, f)).size
                best = max(best or 0, w / h)
            except OSError:
                pass
    return round(best, 3) if best else 0.8


def body_html(story):
    """Zet de blokken om naar genummerde secties. Geeft (html, [(id, nr, titel)])."""
    parts, toc, open_sec, first, n = [], [], False, True, 0

    def start(sec_id=None, heading=None, nr=None):
        nonlocal open_sec
        if open_sec:
            parts.append("</section>")
        attr = f' id="{sec_id}"' if sec_id else ""
        parts.append(f'<section class="sec"{attr}>')
        if heading:
            parts.append(f"<h2><span>{nr}</span>{esc(heading)}</h2>")
        open_sec = True

    blocks = [{"type": "text", "content": t} for t in story["opening"]] + story["body"]
    for b in blocks:
        kind, content = b["type"], b["content"]
        if kind == "heading":
            n += 1
            nr = f"{n:02d}"
            start(f"s{n}", content, nr)
            toc.append((f"s{n}", nr, content))
            continue
        if not open_sec:
            start()
        if kind == "text":
            cls = ' class="first"' if first else ""
            first = False
            parts.append(f"<p{cls}>{esc(content)}</p>")
        elif kind == "quote":
            parts.append(f"<blockquote>“{esc(content)}”</blockquote>")
        elif kind == "photos":
            files = [f for f in content if f and os.path.exists(os.path.join(ROOT, f))]
            if files:
                r = ratio(files)
                cls = "pair one" if len(files) == 1 else "pair"
                imgs = "".join(
                    f'<div class="ph" style="aspect-ratio:{r}"><img src="{asset(f)}" alt="" loading="lazy"></div>'
                    for f in files
                )
                parts.append(f'<div class="{cls}">{imgs}</div>')
    if open_sec:
        parts.append("</section>")
    return "\n".join(parts), toc


def page(story, older, newer):
    name, role, vol = story["name"], story["role"], story["vol"]
    body, toc = body_html(story)
    desc = story["desc"] or story["intro"] or f"{name}, {role}. Een verhaal van Culture Head."
    url = f"{SITE}stories/{story['slug']}.html"
    long_name = " long" if len(name) > 18 else ""
    quote_html = f'<p class="hq">“{esc(story["quote"])}”</p>' if story["quote"] else ""
    if story["video"]:
        media = (f'<video controls preload="none" playsinline poster="{asset(story["thumb"])}" '
                 f'src="{asset(story["video"])}"></video>')
    else:
        media = f'<img src="{asset(story["thumb"])}" alt="{esc(name)}">'
    intro = f'<p class="intro">{esc(story["intro"])}</p>' if story["intro"] else '<div style="height:8vh"></div>'

    side = ""
    if len(toc) > 1 or story["about"]:
        items = "".join(f'<li><a href="#{i}"><span>{nr}</span>{esc(t)}</a></li>' for i, nr, t in toc)
        about = (f'<div class="about"><b>Over {esc(name.split()[0])}</b>{esc(story["about"])}</div>'
                 if story["about"] else "")
        ol = f'<ol id="toc">{items}</ol>' if len(toc) > 1 else ""
        side = f'<aside class="side">{ol}{about}</aside>'
    main_cls = "main" if side else "main solo"

    src = ""
    if story["sources"]:
        links = " &middot; ".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a>' for t, u in story["sources"])
        src = f'<p class="src">Meer over {esc(name.split()[0])}: {links}</p>'

    def nav(s, label, arrow_left):
        if not s:
            return ('<a href="../index.html#index"><small>Alle verhalen</small><strong>Index</strong></a>')
        small = f"&larr; Vol. {s['vol']}" if arrow_left else f"Vol. {s['vol']} &rarr;"
        return f'<a href="{s["slug"]}.html"><small>{small}</small><strong>{esc(s["name"])}</strong></a>'

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(name)} | Culture Head</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="../culture_head_logo.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Culture Head">
<meta property="og:title" content="{html.escape(name)} | Culture Head">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{quote(story['thumb'])}">
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=Courier+Prime&family=Reenie+Beanie&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header><a href="../index.html">&larr; Culture Head</a><nav><span>Vol. {vol}</span><a href="../index.html#index">Index</a></nav></header>

<section class="hero">
  <div class="l">
    <div class="vol">Vol. {vol}</div>
    <div>
      <h1 class="name{long_name}">{esc(name)}</h1>
      <div class="role">{esc(role)}</div>
      {quote_html}
    </div>
    <div class="scroll">Scroll &darr;</div>
  </div>
  <div class="r"><div class="ph">{media}</div></div>
</section>

{intro}

<div class="{main_cls}">
{side}
<article>
{body}
{src}
<div class="sign">Culture Head</div>
</article>
</div>

<nav class="next">{nav(older, "", True)}{nav(newer, "", False)}</nav>
<footer><a href="../index.html">Culture Head &middot; Amsterdam</a><a href="https://instagram.com/cltrhead" target="_blank" rel="noopener">Instagram</a><span>&copy; Culture Head</span></footer>
<script>{JS}</script>
</body>
</html>
"""


def main():
    stories = json.load(open(os.path.join(ROOT, "tools", "stories.json"), encoding="utf-8"))
    out_dir = os.path.join(ROOT, "stories")
    os.makedirs(out_dir, exist_ok=True)
    for i, s in enumerate(stories):  # volgorde: nieuwste eerst
        newer = stories[i - 1] if i > 0 else None
        older = stories[i + 1] if i + 1 < len(stories) else None
        with open(os.path.join(out_dir, s["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page(s, older, newer))
    urls = [SITE] + [f"{SITE}stories/{s['slug']}.html" for s in stories]
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc></url>\n")
        f.write("</urlset>\n")
    print(f"{len(stories)} pagina's gebouwd in stories/ en sitemap.xml bijgewerkt")


if __name__ == "__main__":
    main()
