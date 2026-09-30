with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'portStocksTableBody', text)]
for pos in matches:
    start = max(0, pos - 50)
    end = min(len(text), pos + 300)
    print(text[start:end].encode('ascii', 'replace').decode('ascii'))
    print("="*40)
