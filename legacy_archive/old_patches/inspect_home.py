with open("build_standalone_html.py", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r'id=["\'](home-[^"\']+)["\']', content)
print("Found home- IDs in HTML:", matches)
