import json
import os
import shutil

CACHE_FILE = "cache/standalone_data.json"
INDEX_FILE = "index.html"
EMPRESA_FILE = "empresa.html"
BRAIN_INDEX = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41\munger_terminal.html"
BRAIN_EMPRESA = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41\empresa.html"

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False)

# Update index.html
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "let APP_DATA =" in line:
        lines[i] = f"    let APP_DATA = {json_str};\n"
        print(f"[OK] Replaced APP_DATA in {INDEX_FILE} at line {i+1}")
        break

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.writelines(lines)

# Update empresa.html
if os.path.exists(EMPRESA_FILE):
    with open(EMPRESA_FILE, "r", encoding="utf-8") as f:
        emp_lines = f.readlines()

    for i, line in enumerate(emp_lines):
        if "const APP_DATA =" in line:
            emp_lines[i] = f"    const APP_DATA = {json_str};\n"
            print(f"[OK] Replaced APP_DATA in {EMPRESA_FILE} at line {i+1}")
            break

    with open(EMPRESA_FILE, "w", encoding="utf-8") as f:
        f.writelines(emp_lines)

shutil.copy2(INDEX_FILE, BRAIN_INDEX)
if os.path.exists(EMPRESA_FILE):
    shutil.copy2(EMPRESA_FILE, BRAIN_EMPRESA)
print("[OK] Sincronizacao de dados e artefatos concluida com sucesso!")
