# -*- coding: utf-8 -*-
"""Build docs/covered/index.html (the course map / cover page) from tools/covered.json.

Edit covered.json, then run:  python tools/make_covered.py
"""
import html, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(io.open(os.path.join(HERE, "covered.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "..", "docs", "covered", "index.html")
BASE = "https://kyonversation-dot.github.io/ncea-l1-vocab/"

e = html.escape


def practice(it):
    """The materials for this topic: a link, plus Done / Again for Max's report."""
    rows = []
    for mid in it.get("use", []):
        m = DATA["materials"][mid]
        rows.append('<li class="mat" data-m="%s"><a href="%s" lang="ja">%s</a><span class="acts">'
                    '<label><input type="checkbox" data-k="done"> Done</label>'
                    '<label><input type="checkbox" data-k="again"> Again</label></span></li>'
                    % (e(mid), e(m["href"]), e(m["title"])))
    return '<ul class="mats">%s</ul>' % "".join(rows) if rows else ""


def row(it):
    topic = e(it["topic"])
    chips = []
    if it.get("kiyo"):
        chips.append('<span class="chip k"><b>Lessons</b>%s</span>' % e(it["kiyo"]))
    if it.get("school"):
        chips.append('<span class="chip s"><b>School</b>%s</span>' % e(it["school"]))
    done = it.get("done")
    mark = '<span class="mark" aria-label="Done">✓</span>' if done else '<span class="mark todo" aria-label="Not yet"></span>'
    return ('<li class="row%s" data-done="%s">%s<div class="body"><div class="topic" lang="ja">%s</div>%s%s</div></li>'
            % (" done" if done else "", "1" if done else "0", mark, topic,
               ('<div class="chips">%s</div>' % "".join(chips)) if chips else "", practice(it)))


sections, summary = [], []
total = total_done = 0
for y in DATA["years"]:
    items = y["items"]; d = sum(1 for i in items if i.get("done"))
    total += len(items); total_done += d
    pct = round(d * 100 / len(items)) if items else 0
    summary.append('<div class="sum"><b>%s</b><span class="n">%d of %d done</span>'
                   '<div class="bar" aria-hidden="true"><i style="width:%d%%"></i></div></div>' % (e(y["label"]), d, len(items), pct))
    sections.append('<section class="year" aria-labelledby="h-%s"><h2 id="h-%s">%s</h2><ul class="list">%s</ul></section>'
                    % (y["id"], y["id"], e(y["label"]), "".join(row(i) for i in items)))

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Japanese Course Map — NCEA L1</title>
<style>
  :root{
    --paper:#f6f7f6; --card:#ffffff; --ink:#151815; --muted:#5f6b62;
    --line:#dde3de; --line-soft:#ecefec;
    --accent:#1c6b4f; --accent-soft:#e3efe9; --accent-ink:#12503a;
    --warm:#8a5a2b; --warm-soft:#f5ecdf;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
    --jp:"Hiragino Kaku Gothic ProN","Yu Gothic","Yu Gothic UI",Meiryo,sans-serif;
  }
  @media (prefers-color-scheme:dark){
    :root:not([data-theme="light"]){ --paper:#101310; --card:#181c19; --ink:#e8ece8; --muted:#8f9a92;
      --line:#2a302c; --line-soft:#20251f; --accent:#6cc79c; --accent-soft:#1a2c23; --accent-ink:#8fd9b4;
      --warm:#d0a06a; --warm-soft:#2a2218; color-scheme:dark; }
  }
  :root[data-theme="dark"]{ --paper:#101310; --card:#181c19; --ink:#e8ece8; --muted:#8f9a92;
    --line:#2a302c; --line-soft:#20251f; --accent:#6cc79c; --accent-soft:#1a2c23; --accent-ink:#8fd9b4;
    --warm:#d0a06a; --warm-soft:#2a2218; color-scheme:dark; }
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.6;font-variant-numeric:tabular-nums}
  :focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
  .wrap{max-width:720px;margin:0 auto;padding:26px 18px 80px;display:flex;flex-direction:column;gap:20px}
  .eyebrow{font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
  h1{font-family:var(--serif);font-size:1.6rem;font-weight:600;margin:0;letter-spacing:-.01em;text-wrap:balance}
  .lede{color:var(--muted);font-size:.86rem;margin:0;max-width:62ch}
  .links{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
  .links a{display:flex;flex-direction:column;gap:2px;background:var(--card);border:1px solid var(--line);border-radius:8px;
    padding:10px 12px;text-decoration:none;color:var(--ink)}
  .links a:hover{border-color:var(--accent)}
  .links b{font-size:.95rem;color:var(--accent-ink)}
  .links span{font-size:.75rem;color:var(--muted)}
  h2{font-family:var(--serif);font-size:1.25rem;font-weight:600;margin:0 0 6px}
  .summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
  .sum{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;display:flex;flex-direction:column;gap:4px;min-width:0}
  .sum b{font-family:var(--serif);font-size:1.05rem}
  .sum .n{font-size:.78rem;color:var(--muted)}
  .bar{height:5px;background:var(--line-soft);border-radius:3px;overflow:hidden}
  .bar i{display:block;height:100%%;background:var(--accent)}
  .filters{display:flex;gap:8px;flex-wrap:wrap}
  .filters button{font:inherit;font-size:.85rem;border:1px solid var(--line);background:var(--card);color:var(--ink);
    border-radius:999px;padding:5px 12px;cursor:pointer}
  .filters button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--paper)}
  ul.list{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
  li.row{display:grid;grid-template-columns:26px minmax(0,1fr);gap:10px;padding:9px 2px;border-bottom:1px solid var(--line)}
  .mark{width:20px;height:20px;border-radius:50%%;background:var(--accent);color:var(--paper);font-size:.75rem;
    display:flex;align-items:center;justify-content:center;margin-top:2px}
  .mark.todo{background:transparent;border:1.5px solid var(--line)}
  .body{min-width:0;display:flex;flex-direction:column;gap:4px}
  .topic{font-family:var(--jp);font-size:.98rem;overflow-wrap:anywhere}
  .topic a{color:var(--accent)}
  li.done .topic{color:var(--muted)}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chip{font-size:.74rem;padding:1px 8px;border-radius:4px;overflow-wrap:anywhere;max-width:100%%}
  .chip b{margin-right:5px}
  .chip.k{background:var(--accent-soft);color:var(--accent-ink)}
  .chip.s{background:var(--warm-soft);color:var(--warm)}
  ul.mats{list-style:none;margin:2px 0 0;padding:0;display:flex;flex-direction:column;gap:4px}
  li.mat{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:2px 12px;font-size:.86rem;font-family:var(--jp)}
  li.mat a{color:var(--accent);overflow-wrap:anywhere}
  .acts{display:flex;gap:12px;font-family:var(--sans);font-size:.78rem;color:var(--muted)}
  .acts label{display:flex;align-items:center;gap:4px;cursor:pointer;min-height:28px}
  .acts input{width:16px;height:16px;margin:0;accent-color:var(--accent)}
  .report{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
  .report h2{font-size:1.05rem;margin:0}
  .report p{margin:0;font-size:.85rem;color:var(--muted)}
  .report .line{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
  .report button{font:inherit;font-size:.88rem;font-weight:600;border:0;border-radius:6px;padding:7px 14px;background:var(--accent);color:var(--paper);cursor:pointer}
  .report .count{font-size:.8rem;color:var(--muted)}
  .report textarea{width:100%%;min-height:150px;font:inherit;font-size:.82rem;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:8px}
  footer{font-size:.75rem;color:var(--muted);border-top:1px solid var(--line-soft);padding-top:12px}
  footer a{color:var(--accent)}
  @media (max-width:520px){ .summary{grid-template-columns:1fr} }
  [hidden]{display:none !important}
</style></head><body>
<div class="wrap">
  <div>
    <span class="eyebrow">NCEA Level 1 · Japanese</span>
    <h1>Course map</h1>
  </div>
  <p class="lede">Everything from Year&nbsp;9 to Year&nbsp;11 you are expected to know. A tick means we have finished it in our lessons. <b>Lessons</b> shows the dates we worked on it together; <b>School</b> shows where it comes up in your school course.</p>

  <nav class="links" aria-label="Study pages">
    <a href="%(base)s"><b>Words</b><span>Kanji, topics, numbers</span></a>
    <a href="%(base)sreading/"><b>Reading</b><span>Practice papers</span></a>
    <a href="%(base)slistening/"><b>Listening</b><span>Audio and questions</span></a>
    <a href="%(base)squiz/"><b>Quizzes</b><span>Short checks</span></a>
    <a href="%(base)sreview/"><b>Lesson reviews</b><span>What we did each lesson</span></a>
  </nav>

  <div class="summary">%(summary)s</div>

  <section class="report" aria-labelledby="h-report">
    <h2 id="h-report">Report your practice</h2>
    <p>Under each topic, tick <b>Done</b> when you have tried a page, and <b>Again</b> if you want to go over it in a lesson. Before each lesson, press the button and paste the report at the top of that day's lesson Doc.</p>
    <div class="line"><button type="button" id="copy">Copy my report</button><span class="count" id="count" aria-live="polite"></span></div>
    <textarea id="out" readonly hidden aria-label="Your report"></textarea>
  </section>

  <div class="filters" role="group" aria-label="Show">
    <button type="button" data-f="all" aria-pressed="true">All (%(total)d)</button>
    <button type="button" data-f="todo" aria-pressed="false">Not yet (%(todo)d)</button>
  </div>

  %(sections)s

  <footer>Updated %(updated)s.</footer>
</div>
<script>
(function(){
  var bs = document.querySelectorAll('.filters button');
  function apply(f){
    bs.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.f === f)); });
    document.querySelectorAll('li.row').forEach(function(li){ li.hidden = (f === 'todo' && li.dataset.done === '1'); });
    try { localStorage.setItem('covered-filter', f); } catch(e) {}
  }
  bs.forEach(function(b){ b.addEventListener('click', function(){ apply(b.dataset.f); }); });
  var f = 'all'; try { f = localStorage.getItem('covered-filter') || 'all'; } catch(e) {}
  apply(f);

  var KEY = 'covered-practice', S = {};
  try { S = JSON.parse(localStorage.getItem(KEY)) || {}; } catch(e) {}
  var boxes = document.querySelectorAll('.mat input');
  function name(li){ return li.querySelector('a').textContent; }
  function paint(){
    boxes.forEach(function(b){ b.checked = !!(S[b.closest('.mat').dataset.m] || {})[b.dataset.k]; });
    var all = {}, d = 0;
    document.querySelectorAll('.mat').forEach(function(li){ all[li.dataset.m] = 1; });
    Object.keys(all).forEach(function(m){ if ((S[m] || {}).done) d++; });
    document.getElementById('count').textContent = d + ' of ' + Object.keys(all).length + ' pages done';
  }
  boxes.forEach(function(b){ b.addEventListener('change', function(){
    var m = b.closest('.mat').dataset.m;
    S[m] = S[m] || {}; S[m][b.dataset.k] = b.checked;
    try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e) {}
    paint();
  }); });
  function report(){
    var seen = {}, done = [], again = [], todo = [];
    document.querySelectorAll('.mat').forEach(function(li){
      var m = li.dataset.m; if (seen[m]) return; seen[m] = 1;
      var s = S[m] || {};
      (s.done ? done : todo).push(name(li));
      if (s.again) again.push(name(li));
    });
    function part(t, a){ return t + ' (' + a.length + ')\\n' + (a.length ? a.map(function(x){ return '- ' + x; }).join('\\n') : '- none'); }
    return ['Practice report, ' + new Date().toLocaleDateString('en-NZ', {day:'numeric', month:'short'}),
            part('Done', done), part('Want to go over again', again), part('Not done yet', todo)].join('\\n\\n');
  }
  var btn = document.getElementById('copy'), out = document.getElementById('out');
  btn.addEventListener('click', function(){
    var t = report(); out.value = t; out.hidden = false;
    function ok(){ btn.textContent = 'Copied. Paste it into the lesson Doc'; }
    function manual(){ out.select(); btn.textContent = 'Select the text below and copy it'; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(ok, manual); else manual();
  });
  paint();
})();
</script>
</body></html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(PAGE % {
    "base": BASE, "summary": "".join(summary), "sections": "".join(sections),
    "total": total, "todo": total - total_done, "updated": e(DATA["updated"])})
print("wrote", OUT, total, "items,", total_done, "done")
