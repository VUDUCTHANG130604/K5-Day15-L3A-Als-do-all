"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()

URL_OPENAI = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_OLLAMA = "http://localhost:11434/api/chat"


RETRY_CODES = (429, 500, 502, 503, 504)
MAX_RETRIES = 3


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib).
    Lỗi tạm thời phía máy chủ (429 / 5xx / hết giờ chờ): thử lại tối đa MAX_RETRIES lần, chờ 5s, 10s, 20s.
    Token vẫn lấy từ usage của lần gọi thành công — lần lỗi không có phản hồi nên không có token."""
    req_data = json.dumps(body).encode("utf-8")
    hdrs = dict({"Content-Type": "application/json"}, **headers)
    for attempt in range(MAX_RETRIES + 1):
        req = urllib.request.Request(url, data=req_data, method="POST", headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = "HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300])
            if e.code not in RETRY_CODES or attempt == MAX_RETRIES:
                raise RuntimeError(msg)
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt == MAX_RETRIES:
                raise
        time.sleep(5 * (2 ** attempt))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"],
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


def call_claude(system, user):
    data = post_json(URL_CLAUDE,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


def call_ollama(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OLLAMA, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}


def call_gemini(system, user):
    model_id = MODEL_NAME or "gemini-3.1-flash-lite"
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model_id, API_KEY)
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, body)
    candidates = data.get("candidates") or []
    parts = (candidates[0].get("content", {}).get("parts") or []) if candidates else []
    text = "".join(p.get("text", "") for p in parts)
    u = data.get("usageMetadata", {})
    tok_in = u.get("promptTokenCount", 0)
    tok_out = u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
    return {"text": text, "tokens_in": tok_in, "tokens_out": tok_out}


def _synthesize_mock_reply(user: str) -> str:
    """Tạo phản hồi giả lập bám sát dữ liệu đối chiếu từ công cụ khi chạy ở chế độ fake (CP2)."""
    lines = user.strip().splitlines()
    last = (lines or [""])[-1]
    body = [l for l in lines if l and not l.startswith("[DỮ LIỆU ĐỐI CHIẾU") and not l.startswith("[YÊU CẦU")]
    summary = "\n".join(body[:25])
    return "[câu trả lời giả — chưa nối model] Yêu cầu: %s\n\n%s" % (last[:80], summary)


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        return {
            "text": _synthesize_mock_reply(user),
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }
    if MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    else:
        raise NotImplementedError(
            "Chưa hỗ trợ MODEL_PROVIDER=%s trong codebase/ai.py — dùng openai, anthropic, gemini hoặc ollama."
            % MODEL_PROVIDER
        )
    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
