with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "const tbody = document.getElementById('portStocksTableBody');" in line:
        for j in range(i, min(len(lines), i + 45)):
            print(f"{j+1}: {lines[j].strip()[:90]}".encode('ascii', 'replace').decode('ascii'))
        break
