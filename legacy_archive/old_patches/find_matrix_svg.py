with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
in_matrix = False
for i, line in enumerate(lines):
    if "function renderMatrix" in line:
        in_matrix = True
    if in_matrix:
        if "svg.innerHTML" in line or "<rect" in line or "background" in line or "fill=" in line:
            print(f"Line {i+1}: {line.strip()[:100]}")
        if "function " in line and "function renderMatrix" not in line and in_matrix:
            if i > 3000:
                break
