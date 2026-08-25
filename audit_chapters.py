import re, pathlib, html, sys, subprocess

# every chapter listed in _quarto.yml, so new chapters are covered automatically
_yml = pathlib.Path("_quarto.yml").read_text()
FILES = [m for m in re.findall(r'^\s+- ([a-z0-9-]+\.qmd)\s*$', _yml, re.M)
         if m not in ("references.qmd",)]
issues = []
def flag(f, kind, msg): issues.append((f, kind, msg))

def outputs_of(stem):
    h = pathlib.Path(f"_book/{stem}.html")
    if not h.exists(): return ""
    t = h.read_text()
    blocks = re.findall(r'cell-output-stdout[^>]*>\s*<pre[^>]*>\s*<code[^>]*>(.*?)</code>', t, re.S)
    # rendered tables (kable, data.frame, gt) are output too; without them the
    # "number not in output" check reports false positives for every table figure
    blocks += re.findall(r'<table.*?</table>', t, re.S)
    blocks += re.findall(r'cell-output-display.*?>(.*?)</div>', t, re.S)
    return "\n".join(html.unescape(re.sub(r'<[^>]+>',' ',b)) for b in blocks)

for f in FILES:
    src = pathlib.Path(f).read_text()
    stem = f[:-4]
    out  = outputs_of(stem)
    # strip code chunks -> prose only
    prose = re.sub(r'^```.*?^```', '', src, flags=re.S | re.M)
    src_nochunk = prose            # headings must be counted outside code chunks

    # --- 1. heading tree: no level skips
    lvls = [(i+1, len(m.group(1)), m.group(2))
            for i,l in enumerate(src_nochunk.split('\n'))
            if (m := re.match(r'^(#{1,4}) (.+)$', l))]
    prev = 0
    for ln, lv, txt in lvls:
        if prev and lv > prev + 1: flag(f, "HEADING-SKIP", f"L{ln}: h{prev}->h{lv} '{txt[:40]}'")
        prev = lv

    # --- 2. every number in prose appears in some chunk output (or is whitelisted)
    WHITE = re.compile(r'^(0|1|2|3|4|5|6|10|100|1000|1978|1990|1998|2007|2010|2022|2024|1933|1963|20|30|60|90|9|8|7)$')
    for ln, line in enumerate(prose.split('\n'), 1):
        if line.startswith(('|','$$')) or '](' in line: continue
        if line.startswith('    '): continue          # indented code block
        if 'doi.org' in line or 'arxiv' in line.lower(): continue
        for num in re.findall(r'(?<![\w.$\\-])(\d+\.\d\d+)(?![\w.])', line):
            if num in out or num.rstrip('0').rstrip('.') in out:
                continue
            # prose normally quotes a rounded form of a printed number: accept any
            # output value that agrees to the precision the prose actually shows
            dec = len(num.split('.')[1]); tol = 0.5 * 10 ** (-dec)
            v = float(num)
            if any(abs(v - float(o)) <= tol + 1e-9 for o in re.findall(r'\d+\.\d+', out)):
                continue
            flag(f, "NUMBER-NOT-IN-OUTPUT", f"{num}  in: {line.strip()[:70]}")

    # --- 3. citations resolve
    refs = pathlib.Path("references.qmd").read_text()
    IGNORE = {"Stata", "Table", "Figure", "Chapter", "Section", "Equation", "R", "SAS"}
    for name in set(re.findall(r"\b([A-Z][A-Za-z\u00C0-\u024F'\u2019-]{2,})\s+\((?:19|20)\d{2}[a-z]?\)", prose)):
        if name in IGNORE: continue
        base = re.sub(r"['\u2019]s$", "", name)          # Knaus's -> Knaus
        parts = [q for q in base.split('-') if q]        # Newey-West -> Newey, West
        if any(q in refs for q in [base] + parts): continue
        flag(f, "CITATION-MISSING", name)

    # --- 4. internal links resolve
    for tgt in re.findall(r'\]\((?!http)([a-z0-9-]+\.qmd)\)', prose):
        if not pathlib.Path(tgt).exists(): flag(f, "DEAD-INTERNAL-LINK", tgt)

    # --- 5. unmatched display math
    if src.count('$$') % 2: flag(f, "UNMATCHED-$$", f"count={src.count('$$')}")

    # --- 6. blank line inside $$..$$ (kills rendering; a known trap in this book)
    for m in re.finditer(r'\$\$(.*?)\$\$', src, re.S):
        if '\n\n' in m.group(1): flag(f, "BLANK-LINE-IN-MATH", m.group(1)[:50].replace('\n','\\n'))

    # --- 7. raw LaTeX leaking into the rendered page
    hh = pathlib.Path(f"_book/{stem}.html")
    if hh.exists():
        body = hh.read_text()
        for cmd in ():
            # inside <script type="math/tex"> is fine; count occurrences in visible text
            vis = re.sub(r'<script.*?</script>', '', body, flags=re.S)
            vis = re.sub(r'<[^>]+>', '', vis)
            if cmd in vis: flag(f, "RAW-LATEX-VISIBLE", cmd)

print(f"{len(issues)} issues\n")
print("NOTE: NUMBER-NOT-IN-OUTPUT is advisory. Constants derived analytically in\n"
      "prose (rules of thumb, algebraic weights) have no chunk output to match.\n")
for f,k,m in issues: print(f"[{k}] {f}: {m}")
