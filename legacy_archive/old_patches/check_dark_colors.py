with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
print("Dark colors in SVG or JS:")
for color in ["#05070A", "#06080C", "#080C14", "#0A0E1A", "#07090E", "#0B0F17", "#080A0F"]:
    count = text.count(color)
    print(f"{color}: {count} occurrences")
