"""
server.py
=========
Servidor HTTP leve institucional para o JP Morgan & Charlie Munger B3 Terminal.
Fornece:
1. Hospedagem estática de index.html na porta 8000.
2. Endpoint POST /api/refresh: Dispara scraping em tempo real no Fundamentus,
   recalcula os scores de qualidade e valuation, e retorna o novo dataset.
3. Endpoint GET /api/data: Retorna os dados em cache no formato JSON.
4. Suporte a CORS para conexões locais e fallback offline.
"""

from __future__ import annotations
import http.server
import json
import logging
import os
import sys
import threading
from urllib.parse import urlparse

from build_standalone_data import compile_standalone_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

import socket

def get_available_port(preferred_port=8050):
    for p in range(preferred_port, preferred_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return preferred_port

PORT = get_available_port(int(os.environ.get("PORT", 8050)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cache", "standalone_data.json")

# Lock para evitar scrapings simultâneos concorrentes
scrape_lock = threading.Lock()


class MungerTerminalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Habilita CORS para todas as origens locais e file://
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Request-Private-Network")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.path = "/index.html"
            return super().do_GET()

        elif path == "/api/data":
            self.handle_get_data()

        elif path == "/api/refresh":
            self.handle_refresh()

        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/refresh":
            self.handle_refresh()
        else:
            self.send_error(404, "Endpoint desconhecido")

    def handle_get_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
                body = data.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                self.send_error(500, f"Erro ao ler dados: {e}")
        else:
            self.send_error(404, "Arquivo de dados ainda não compilado")

    def handle_refresh(self):
        logger.info("Requisição de atualização ao vivo recebida de %s", self.client_address[0])
        
        if scrape_lock.locked():
            err_body = json.dumps({"error": "Atualização já em andamento. Aguarde..."}).encode("utf-8")
            self.send_response(429)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(err_body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(err_body)
            return

        with scrape_lock:
            try:
                logger.info("Executando pipeline de extração e auditoria no Fundamentus...")
                dataset = compile_standalone_dataset(force_refresh=True)

                # Recompila index.html com os novos dados embutidos
                try:
                    import subprocess
                    subprocess.run([sys.executable, "build_standalone_html.py"], cwd=BASE_DIR, check=True)
                except Exception as e_build:
                    logger.warning("Falha ao recompilar index.html: %s", e_build)

                resp_body = json.dumps(dataset, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(resp_body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(resp_body)
                logger.info("Atualização concluída com sucesso. %d ativos enviados (%d bytes).", len(dataset["stocks"]), len(resp_body))

            except Exception as e:
                logger.error("Erro durante atualização do Fundamentus: %s", e, exc_info=True)
                err_resp = json.dumps({"error": f"Falha na extração do Fundamentus: {str(e)}"}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_resp)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(err_resp)


def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, MungerTerminalHandler)
    logger.info("==================================================================")
    logger.info("🏛️ JP MORGAN & CHARLIE MUNGER B3 TERMINAL (SERVER ATIVO)")
    logger.info("Aplicação Web disponível em: http://localhost:%d/index.html", PORT)
    logger.info("Endpoint de dados:          http://localhost:%d/api/data", PORT)
    logger.info("Endpoint de atualização:    http://localhost:%d/api/refresh", PORT)
    logger.info("Pressione Ctrl+C para encerrar.")
    logger.info("==================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Encerrando servidor...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
