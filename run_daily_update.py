import subprocess
import os
import sys
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
git_exe = r"C:\Users\dougl\.gemini\antigravity\scratch\tools\mingit\cmd\git.exe"

def run():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando atualizacao diaria dos dados B3...")
    
    # 1. Pipeline de Dados e Compilacao dos Balancos
    subprocess.run([sys.executable, "build_standalone_data.py"], cwd=base_dir, check=True)
    subprocess.run([sys.executable, "build_standalone_html.py"], cwd=base_dir, check=True)
    subprocess.run([sys.executable, "build_company_page.py"], cwd=base_dir, check=True)
    subprocess.run([sys.executable, "build_seo_sitemap.py"], cwd=base_dir, check=True)
    
    # 2. Git Add, Commit e Push para o GitHub Pages
    today = datetime.now().strftime("%d/%m/%Y")
    subprocess.run([git_exe, "add", "index.html", "empresa.html", "sitemap.xml", "cache/"], cwd=base_dir, check=True)
    
    res = subprocess.run([git_exe, "commit", "-m", f"chore(data): atualizacao automatica das cotacoes e multiplos B3 [{today}]"], cwd=base_dir, capture_output=True, text=True)
    print("Git Commit output:", res.stdout.strip() if res.stdout else res.stderr.strip())
    
    if "nothing to commit" in (res.stdout or "") or "nothing to commit" in (res.stderr or ""):
        print("Nenhuma alteracao nas cotacoes neste momento.")
    else:
        print("Enviando atualizacoes para o GitHub...")
        subprocess.run([git_exe, "push", "origin", "main"], cwd=base_dir, check=True)
        print("Deploy publicado com sucesso no GitHub Pages e moatterminal.com.br!")

if __name__ == "__main__":
    run()
