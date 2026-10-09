import json
import os
from datetime import datetime

def generate_seo_assets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "cache", "standalone_data.json")
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    stocks = data.get("stocks", [])
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        '    <loc>https://moatterminal.com.br/</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ]
    
    sitemap_lines.extend([
        '  <url>',
        '    <loc>https://moatterminal.com.br/empresa.html</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.5</priority>',
        '  </url>'
    ])
    
    for s in stocks:
        ticker = s.get("ticker", "").upper().strip()
        if not ticker:
            continue
        sitemap_lines.extend([
            '  <url>',
            f'    <loc>https://moatterminal.com.br/acoes/{ticker.lower()}/</loc>',
            f'    <lastmod>{today_str}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>0.9</priority>',
            '  </url>'
        ])
        
    sitemap_lines.extend([
        '  <url>',
        '    <loc>https://moatterminal.com.br/privacidade.html</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.3</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://moatterminal.com.br/termos.html</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.3</priority>',
        '  </url>',
        '</urlset>'
    ])
    
    sitemap_content = "\n".join(sitemap_lines)
    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
        
    robots_content = """User-agent: *
Allow: /

Sitemap: https://moatterminal.com.br/sitemap.xml
"""
    robots_path = os.path.join(base_dir, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
        
    print(f"Generated {sitemap_path} with {len(stocks) + 4} URLs")
    print(f"Generated {robots_path}")

    # Garante que todo o diretório acoes/ esteja no git stage para o commit do bot
    import shutil
    import subprocess
    git_bin = shutil.which("git")
    if not git_bin and os.name == "nt":
        for c in [r"C:\Users\dougl\AppData\Local\Programs\MinGit\cmd\git.exe", r"C:\Program Files\Git\cmd\git.exe"]:
            if os.path.exists(c):
                git_bin = c
                break
    if git_bin:
        try:
            subprocess.run([git_bin, "add", "acoes/"], cwd=base_dir, check=False)
            print("[Sitemap] Diretório acoes/ adicionado ao stage do Git.")
        except Exception as e:
            print(f"[Sitemap] Nota: git add acoes/ ignorado: {e}")

if __name__ == "__main__":
    generate_seo_assets()
