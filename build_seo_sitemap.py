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
    
    for s in stocks:
        ticker = s.get("ticker", "").upper().strip()
        if not ticker:
            continue
        sitemap_lines.extend([
            '  <url>',
            f'    <loc>https://moatterminal.com.br/empresa.html?ticker={ticker}</loc>',
            f'    <lastmod>{today_str}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>0.8</priority>',
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

if __name__ == "__main__":
    generate_seo_assets()
