with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
print("--- CSS SEARCH ---")
for m in re.findall(r"\.glass-panel\s*\{[^}]*\}", text):
    print(m)

print("--- TAG SEARCH ---")
for line in text.splitlines():
    if "<header" in line or 'id="view-home"' in line or 'id="matrixContainer"' in line or 'id="view-matrix"' in line:
        print(line[:120])
