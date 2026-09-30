import asyncio
import json
import os
import subprocess
import urllib.request
import websockets
import base64

async def test_tooltips():
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    port = 9488
    proc = subprocess.Popen([
        edge_path,
        '--headless',
        '--disable-gpu',
        f'--remote-debugging-port={port}',
        '--window-size=1440,1080',
        'about:blank'
    ])
    
    await asyncio.sleep(2.0)
    brain_dir = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41"

    try:
        req = urllib.request.urlopen(f'http://127.0.0.1:{port}/json')
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=20_000_000) as ws:
            msg_id = 1
            
            async def send_cmd(method, params=None):
                nonlocal msg_id
                mid = msg_id
                msg_id += 1
                payload = {"id": mid, "method": method}
                if params:
                    payload["params"] = params
                await ws.send(json.dumps(payload))
                while True:
                    resp = await ws.recv()
                    data = json.loads(resp)
                    if data.get("id") == mid:
                        return data.get("result", {})
            
            async def eval_js(expr):
                res = await send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
                return res.get("result", {}).get("value")
            
            async def snap(filepath):
                res = await send_cmd("Page.captureScreenshot", {"format": "png"})
                if "data" in res:
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(res["data"]))
                    print(f"Captured: {filepath}")

            # 1. Testar empresa.html?ticker=BLAU3
            print("--- Testing empresa.html?ticker=BLAU3 ---")
            await send_cmd("Page.navigate", {"url": "http://localhost:8050/empresa.html?ticker=BLAU3"})
            await asyncio.sleep(2.5)

            # Trigger tooltip on ROIC in essential multiples
            test_res_1 = await eval_js("""(() => {
                const el = document.querySelector('[data-tooltip="roic"]');
                if (!el) return { error: 'data-tooltip="roic" not found' };
                el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true }));
                const tip = document.getElementById('globalTooltip');
                return {
                    found: true,
                    hidden: tip.classList.contains('hidden'),
                    title: document.getElementById('gtTitle').textContent,
                    desc: document.getElementById('gtDesc').textContent,
                    top: tip.style.top,
                    left: tip.style.left
                };
            })()""")
            print("Empresa ROIC Tooltip status:", json.dumps(test_res_1, indent=2))
            await snap(os.path.join(brain_dir, "tooltip_empresa_roic.png"))

            # Trigger tooltip on Graham formula in valuation calculators
            test_res_2 = await eval_js("""(() => {
                const el = document.querySelector('[data-tooltip="graham"]');
                if (!el) return { error: 'data-tooltip="graham" not found' };
                el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true }));
                const tip = document.getElementById('globalTooltip');
                return {
                    found: true,
                    hidden: tip.classList.contains('hidden'),
                    title: document.getElementById('gtTitle').textContent,
                    desc: document.getElementById('gtDesc').textContent
                };
            })()""")
            print("Empresa Graham Tooltip status:", json.dumps(test_res_2, indent=2))
            await snap(os.path.join(brain_dir, "tooltip_empresa_graham.png"))

            # 2. Testar index.html (Terminal / Scanner / Dossiê)
            print("--- Testing index.html (Terminal / Scanner / Dossiê) ---")
            await send_cmd("Page.navigate", {"url": "http://localhost:8050/index.html"})
            await asyncio.sleep(2.5)

            # Switch to scanner view
            await eval_js("switchWorkspace('scanner')")
            await asyncio.sleep(1.0)

            # Trigger tooltip on Moat Score table header
            test_res_3 = await eval_js("""(() => {
                const el = document.querySelector('th [data-tooltip="quality_score"]');
                if (!el) return { error: 'header data-tooltip="quality_score" not found' };
                el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true }));
                const tip = document.getElementById('globalTooltip');
                return {
                    found: true,
                    hidden: tip.classList.contains('hidden'),
                    title: document.getElementById('gtTitle').textContent,
                    desc: document.getElementById('gtDesc').textContent
                };
            })()""")
            print("Scanner Moat Score Tooltip status:", json.dumps(test_res_3, indent=2))
            await snap(os.path.join(brain_dir, "tooltip_scanner_moat.png"))

            # Open Dossiê 360 for BLAU3 and trigger tooltip on Spread NTN-B KPI card
            test_res_4 = await eval_js("""(() => {
                openDossierDrawer('BLAU3');
                return { dossierOpened: true };
            })()""")
            await asyncio.sleep(1.0)

            test_res_5 = await eval_js("""(() => {
                const el = document.querySelector('#kpiGrid [data-tooltip="ey_spread"]');
                if (!el) return { error: 'dossier data-tooltip="ey_spread" not found' };
                el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true }));
                const tip = document.getElementById('globalTooltip');
                return {
                    found: true,
                    hidden: tip.classList.contains('hidden'),
                    title: document.getElementById('gtTitle').textContent,
                    desc: document.getElementById('gtDesc').textContent
                };
            })()""")
            print("Dossiê Spread NTN-B Tooltip status:", json.dumps(test_res_5, indent=2))
            await snap(os.path.join(brain_dir, "tooltip_dossie_spread.png"))

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(test_tooltips())
