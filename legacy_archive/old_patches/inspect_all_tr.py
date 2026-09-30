with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "tr.innerHTML =" in line:
        print(f"=== FOUND AT LINE {i+1} ===")
        for j in range(i, min(len(lines), i + 25)):
            clean = lines[j].strip().encode('ascii', 'replace').decode('ascii')
            print(f"  {j+1}: {clean}")
