import os
import sys
import json
import http.server
import socketserver
import threading
from urllib.parse import urlparse, parse_qs
import coupang_engine

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CoupangAutoServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/cart-summary':
            import importlib
            importlib.reload(coupang_engine)
            summary = coupang_engine.get_cart_summary()
            self._send_json(summary)
            return
        elif parsed.path == '/api/ping':
            self._send_json({"status": "ok", "message": "Coupang Auto Server is active!"})
            return
        elif parsed.path == '/api/partners/status':
            import importlib, coupang_partners
            importlib.reload(coupang_partners)
            self._send_json(coupang_partners.get_account_status())
            return
        elif parsed.path == '/api/partners/links':
            import importlib, coupang_partners
            importlib.reload(coupang_partners)
            self._send_json(coupang_partners.get_all_cached_links())
            return
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if parsed.path == '/api/add-to-cart':
            query = data.get('query', '')
            name = data.get('name', '')
            qty = int(data.get('qty', 1))
            spec = data.get('spec', '')
            if not query:
                self._send_json({"success": False, "error": "Query required"}, 400)
                return

            print(f"[API] Adding to cart: {query} ({name}) - targetQty: {qty}, spec: {spec}")
            import importlib
            importlib.reload(coupang_engine)
            result = coupang_engine.add_single_item(query, name, target_qty=qty, spec=spec)
            self._send_json(result)
            return

        elif parsed.path == '/api/batch-add':
            items = data.get('items', [])
            if not items:
                self._send_json({"success": False, "error": "No items provided"}, 400)
                return

            print(f"[API] Batch adding {len(items)} items...")
            results = []
            for it in items:
                q = it.get('query', '')
                n = it.get('name', '')
                qty = int(it.get('qty', 1))
                spec = it.get('spec', '')
                if q:
                    res = coupang_engine.add_single_item(q, n, target_qty=qty, spec=spec)
                    results.append(res)

            self._send_json({
                "success": True,
                "total": len(items),
                "added": len([r for r in results if r.get('success')]),
                "details": results
            })
            return

        elif parsed.path == '/api/open-cart':
            print("[API] Opening Coupang cart page in Chrome (Bringing to foreground)...")
            import importlib
            importlib.reload(coupang_engine)
            res = coupang_engine.open_cart_page()
            self._send_json({"success": True, "message": "Cart opened", "detail": res})
            return

        elif parsed.path == '/api/fix-quantities':
            print("[API] Auditing and fixing cart item quantities...")
            import importlib
            importlib.reload(coupang_engine)
            res = coupang_engine.audit_and_fix_cart_quantities()
        elif parsed.path == '/api/partners/deeplink':
            import importlib, coupang_partners
            importlib.reload(coupang_partners)
            query = data.get('query', '')
            url = data.get('url', '')
            if query:
                link = coupang_partners.get_deeplink_for_query(query)
                self._send_json({"success": True, "query": query, "shortenUrl": link})
            elif url:
                links = coupang_partners.generate_deeplinks([url])
                if links:
                    self._send_json({"success": True, "data": links[0]})
                else:
                    self._send_json({"success": False, "error": "Failed to generate deeplink"}, 500)
            else:
                self._send_json({"success": False, "error": "query or url required"}, 400)
            return

        self.send_error(404, "Endpoint not found")

    def _send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run():
    httpd = ThreadedHTTPServer(("", PORT), CoupangAutoServer)
    print(f"🚀 [Coupang Auto Server] Serving on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run()
