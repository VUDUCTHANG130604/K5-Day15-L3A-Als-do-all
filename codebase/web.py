"""Giao diện chat để demo: python codebase/web.py [cổng] → mở http://127.0.0.1:8765

Chỉ dùng thư viện chuẩn. Gọi đúng answer() trong agent.py như `python run.py`; không gửi tin, không sửa dữ liệu.
Chỉ nghe trên 127.0.0.1 (máy đang chạy), không mở ra mạng.
"""
import json
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai  # noqa: E402
import tracing  # noqa: E402
from agent import answer  # noqa: E402

PAGE = os.path.join(HERE, "web.html")
MAX_BODY = 20_000
LOCK = threading.Lock()  # tracing dùng biến chung → mỗi lúc chỉ chạy một câu


def ask(text: str) -> dict:
    with LOCK:
        tracing.begin("web")
        t0 = time.perf_counter()
        output, error = "", ""
        try:
            output = answer(text)["output"]
        except Exception as e:  # lỗi gọi model: hiện lên giao diện, server vẫn chạy
            error = "%s: %s" % (type(e).__name__, e)
            if ai.API_KEY:
                error = error.replace(ai.API_KEY, "***")
        summary, _ = tracing.end()
    return {"output": output, "error": error, "models": summary["models"], "model_calls": summary["model_calls"],
            "tool_calls": summary["tool_calls"], "tokens_in": summary["tokens_in"],
            "tokens_out": summary["tokens_out"], "seconds": round(time.perf_counter() - t0, 1)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code, data):
        self._send(code, json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _local(self):
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        return host in ("127.0.0.1", "localhost")

    def do_GET(self):
        if not self._local():
            return self._json(403, {"error": "Chỉ dùng trên máy này."})
        if self.path == "/":
            with open(PAGE, "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if self.path == "/api/info":
            return self._json(200, {"provider": ai.MODEL_PROVIDER, "model": ai.MODEL_NAME})
        return self._json(404, {"error": "Không có trang này."})

    def do_POST(self):
        # Bắt buộc Content-Type JSON: trang web khác không gửi chéo được để tiêu lượt gọi model.
        if not self._local() or not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._json(403, {"error": "Yêu cầu không hợp lệ."})
        if self.path != "/api/ask":
            return self._json(404, {"error": "Không có địa chỉ này."})
        try:
            size = int(self.headers.get("Content-Length") or 0)
            if not 0 < size <= MAX_BODY:
                raise ValueError
            text = json.loads(self.rfile.read(size).decode("utf-8"))["text"].strip()
            if not text:
                raise ValueError
        except (ValueError, KeyError, TypeError, AttributeError):
            return self._json(400, {"error": "Câu nhập trống hoặc quá dài."})
        return self._json(200, ask(text))

    def log_message(self, fmt, *args):
        pass


class Server(ThreadingHTTPServer):
    allow_reuse_address = os.name != "nt"  # Windows: bật cờ này thì hai chương trình nghe trùng cổng mà không báo lỗi


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    try:
        server = Server(("127.0.0.1", port), Handler)
    except OSError as e:
        sys.exit("Không mở được cổng %d (%s). Thử cổng khác: python codebase/web.py 8766" % (port, e))
    url = "http://127.0.0.1:%d" % port
    print("Giao diện demo: %s  ·  model: %s  ·  Thoát: Ctrl+C" % (url, ai.MODEL_NAME or ai.MODEL_PROVIDER))
    if not os.environ.get("NO_BROWSER"):
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
