# Claims (UNTRUSTED — re-verified by the adversary from clean state)

## CLAIM S1
what: Single self-contained landing page at docs/index.html covering all 9 planned sections, with the design system, responsiveness, a11y, reduced-motion, and copy-to-clipboard.
files: docs/index.html
run-to-prove: from repo root, run the script below; it exits 0 iff structure + required content present, em-dash/emoji absent, and the inline JS parses.
expected: prints "ALL CHECKS PASS" and "JS OK", exit 0.

```bash
cd /c/Users/a/projects/skill-ab-eval && python3 - <<'PY'
import sys, re, os
from html.parser import HTMLParser
p = "docs/index.html"
html = open(p, encoding="utf-8").read()
errs = []
class P(HTMLParser):
    def error(self, m): raise Exception(m)
try:
    P(convert_charrefs=True).feed(html)
except Exception as e:
    errs.append("parse error: %s" % e)
h1 = len(re.findall(r"<h1[ >]", html, re.I))
if h1 != 1: errs.append("h1 count %d != 1" % h1)
for tok in ["<!doctype html", "<html lang", "<title", "<header", "<nav", "<main", "<footer"]:
    if tok not in html.lower(): errs.append("missing structure: %s" % tok)
need = ["with_skill","without_skill",
        "git clone https://github.com/cskwork/skill-ab-eval ~/.claude/skills/skill-ab-eval",
        "github.com/cskwork/skill-ab-eval","+0.50","+0.38","leaderboard",
        "prefers-reduced-motion","@media (max-width",":focus-visible","aria-live",
        "skill-ab-eval task","skill-ab-eval runners"]
for n in need:
    if n not in html: errs.append("missing content: %s" % n)
if "—" in html: errs.append("em-dash U+2014 present")
if "–" in html: errs.append("en-dash U+2013 present")
emoji = re.findall(r"[\U0001F000-\U0001FAFF]", html)
if emoji: errs.append("emoji present: %r" % emoji[:5])
# external links must declare rel=noopener when target=_blank
tb = len(re.findall(r'target="_blank"', html))
no = len(re.findall(r'rel="noopener', html))
if tb > no: errs.append("target=_blank (%d) > rel=noopener (%d)" % (tb, no))
if not os.path.exists("docs/.nojekyll"): errs.append(".nojekyll missing")
# extract inline JS for a syntax check
m = re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", html, re.S|re.I)
open("/tmp/sae_inline.js","w",encoding="utf-8").write("\n;\n".join(m))
if errs:
    print("FAIL"); [print(" -", e) for e in errs]; sys.exit(1)
print("ALL CHECKS PASS")
PY
node --check /tmp/sae_inline.js && echo "JS OK"
```

## CLAIM S2
what: GitHub Pages deploy scaffolding present so the static page serves verbatim.
files: docs/.nojekyll
run-to-prove: `test -f /c/Users/a/projects/skill-ab-eval/docs/.nojekyll && echo NOJEKYLL_OK`
expected: prints NOJEKYLL_OK, exit 0.
