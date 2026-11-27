"""Công cụ của bài toán A5 (Vận hành đào tạo: lịch, phòng, phân công) — NHÓM VIẾT.

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không.
Dữ liệu: data/schedule_data.json, sinh bằng `python data/build_schedule.py` từ data giả lập BTC (xem data/DATA_CARD.md).
Mọi kiểm tra trong check_conflicts và hậu kiểm trong draft_notice là CODE THUẦN, không gọi AI.
Không công cụ nào gửi tin hay sửa dữ liệu: draft_notice chỉ trả bản nháp chờ người duyệt.
"""
import json
import os
import re
from functools import lru_cache

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "schedule_data.json")

CLASSES = ("L3AB", "L2AB", "L3A", "L3B", "L2A", "L2B")
ROOM_RE = re.compile(r"\b[A-Z]\d{3}\b")
# "Bây giờ" của bản chạy thử = thời điểm xuất bảng phân công (data giả lập). "ngày mai" tính từ mốc này.
SNAPSHOT_DATE = "27/04"
NEXT_DAY = {"27/04": "28/04"}


@lru_cache(maxsize=1)
def _load_db() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _interval(s: dict):
    a, b = s["time"].split("-")
    return _minutes(a), _minutes(b)


def _overlap(s1: dict, s2: dict) -> bool:
    a1, b1 = _interval(s1)
    a2, b2 = _interval(s2)
    return a1 < b2 and a2 < b1


def _cite(s: dict) -> str:
    return "[K9-GD1/%s]" % ",".join(s["official_cells"])


def _parse_query(query: str) -> dict:
    """Tách ngày, lớp, mã buổi, ca, nhóm từ câu tự nhiên. Không đoán: thiếu gì ghi vào 'missing'."""
    q_up, q_low = query.upper(), query.lower()
    dates = ["%02d/%02d" % (int(d), int(m)) for d, m in re.findall(r"(?<!\d)(\d{1,2})\s*[/-]\s*(\d{1,2})(?!\d)", query)]
    relative = None
    if re.search(r"\b(ngày mai|sáng mai|chiều mai|mai)\b", q_low):
        relative = "ngày mai"
        dates.append(NEXT_DAY[SNAPSHOT_DATE])
    elif re.search(r"\bhôm nay\b", q_low):
        relative = "hôm nay"
        dates.append(SNAPSHOT_DATE)
    classes = list(dict.fromkeys(re.findall(r"\b(L3AB|L2AB|L3A|L3B|L2A|L2B)\b", q_up)))
    sessions = ["%s %s" % (m.group(1), m.group(2)) for m in re.finditer(r"\b(LAB|LEC)\s*(\d+)\b", q_up)]
    if "HACKATHON" in q_up:
        sessions.append("HACKATHON")
    kinds = []
    if not sessions:
        if re.search(r"\blab\b", q_low):
            kinds.append("LAB")
        if re.search(r"\b(lec|buổi giảng|lý thuyết)\b", q_low):
            kinds.append("LEC")
    shift = "Sáng" if "sáng" in q_low else ("Chiều" if ("chiều" in q_low or "tối" in q_low and "tối nay" not in q_low) else None)
    groups = [int(g) for g in re.findall(r"nhóm\s*(\d+)", q_low)]
    return {"dates": list(dict.fromkeys(dates)), "relative": relative, "classes": classes, "sessions": sessions,
            "kinds": kinds, "shift": shift, "groups": groups}


def _class_match(s: dict, classes: list) -> bool:
    if not classes:
        return True
    targets = set(s.get("applies_to", [])) | {s["class_name"]}
    return any(c in targets or (c == "L3AB" and targets & {"L3A", "L3B"}) or (c == "L2AB" and targets & {"L2A", "L2B"})
               for c in classes)


@tool
def get_schedule(query: str) -> dict:
    """Tên: get_schedule · Tra lịch của buổi học trong bảng phân công chính thức + lịch sử sửa + bảng lab coach.
    Input: query (str) — câu tự nhiên có ngày (dd/mm, "ngày mai"), lớp (L3A/L3B/L2A/L2B) và/hoặc mã buổi (LAB n, LEC n).
    Output: dict {parsed, missing, matched_sessions, day_sessions, no_match_reason, metadata} — mỗi buổi kèm
            trạng thái chính thức, phòng, mã ô nguồn, các lần sửa liên quan và dòng bảng lab coach (nếu có).
    Tác động ra ngoài: Không (chỉ đọc data/schedule_data.json)."""
    db = _load_db()
    p = _parse_query(query)
    sessions = db["sessions"]
    edits = {e["code"]: e for e in db["edit_history"]}

    missing = []
    if not p["classes"]:
        missing.append("lớp (L3A / L3B / L2A / L2B)")
    if not p["dates"] and not p["sessions"]:
        missing.append("ngày (dd/mm) hoặc mã buổi (vd LAB 9)")

    matched, reason = [], None
    if p["dates"] or p["sessions"]:
        for s in sessions:
            if p["dates"] and s["date"] not in p["dates"]:
                continue
            if s["class_name"] != "ALL":
                if not _class_match(s, p["classes"]):
                    continue
                if p["sessions"] and s["session_code"] not in p["sessions"]:
                    continue
                if p["kinds"] and s["kind"] not in p["kinds"]:
                    continue
            elif p["sessions"]:
                continue
            if p["shift"] and s["shift"] != p["shift"]:
                continue
            matched.append(s)
        if not matched and p["shift"]:   # bỏ điều kiện ca nếu lọc ca làm rỗng (vd buổi lệch giờ 16:30–20:00)
            matched = [s for s in sessions if (not p["dates"] or s["date"] in p["dates"]) and
                       (s["class_name"] == "ALL" or (_class_match(s, p["classes"]) and
                        (not p["sessions"] or s["session_code"] in p["sessions"])))]
        if not matched:
            day_has = [s for s in sessions if s["date"] in p["dates"]]
            if p["dates"] and not day_has:
                reason = "Ngày %s không có trong bảng phân công Khoá 9 (15/04–08/05/2027)." % ", ".join(p["dates"])
            else:
                reason = "Không có buổi nào khớp %s trong bảng phân công." % ", ".join(
                    x for x in [", ".join(p["dates"]), ", ".join(p["classes"]), ", ".join(p["sessions"] + p["kinds"])] if x)

    # G10: chưa biết lớp thì không soạn cho buổi nào — chỉ liệt kê các buổi trong ngày để người dùng chọn.
    # (Ngày nghỉ lễ / không có lớp áp dụng cho mọi lớp nên vẫn trả về.)
    if not p["classes"] and any(s["class_name"] != "ALL" for s in matched):
        matched = []

    out_sessions = []
    for s in matched:
        item = dict(s)
        item["citation"] = _cite(s)
        item["edits"] = [edits[c] for c in s.get("edit_codes", []) if c in edits]
        out_sessions.append(item)

    day_sessions = []
    if missing and p["dates"]:
        day_sessions = ["%s %s %s (%s %s)" % (s["date"], s["class_name"], s["session_code"], s["shift"], s["time"])
                        for s in sessions if s["date"] in p["dates"] and s["class_name"] != "ALL"]

    return {"parsed": p, "missing": missing, "matched_sessions": out_sessions, "day_sessions": day_sessions,
            "no_match_reason": reason, "metadata": db["metadata"]}


def _allocate_groups(s: dict, groups: dict) -> list:
    """Đề xuất chia nhóm vào phòng (code, deterministic): chia lần lượt các nhóm thành khối liền nhau, đều theo số phòng.
    Danh sách nhóm là synthetic — đây là ĐỀ XUẤT để key coach sửa, không phải phân công thật."""
    rooms = s.get("official_rooms", [])
    if s.get("kind") != "LAB" or not rooms:
        return []
    cls_groups = []
    for c in s.get("applies_to", [s["class_name"]]):
        cls_groups += groups.get(c, [])
    n, k = len(cls_groups), len(rooms)
    out, start = [], 0
    for i, room in enumerate(rooms):
        size = n // k + (1 if i < n % k else 0)
        chunk = cls_groups[start:start + size]
        start += size
        out.append({"room": room, "groups": [g["name"] for g in chunk], "students": sum(g["size"] for g in chunk)})
    return out


@tool
def check_conflicts(schedule_bundle: dict) -> dict:
    """Tên: check_conflicts · Kiểm tra bằng CODE THUẦN (không AI) cho các buổi vừa tra được.
    Input: schedule_bundle (dict) — kết quả của get_schedule.
    Output: dict {session_statuses, mismatches, room_changes, time_changes, lecturer_changes, overlaps,
            anomalies, group_allocation, has_any_issue}: lệch bảng chính thức ↔ bảng lab coach, đổi phòng/giờ/giảng viên
            sau khi đã xác nhận, trùng phòng/trùng coach với buổi khác cùng giờ, ô ghi sai định dạng, đề xuất chia nhóm.
    Tác động ra ngoài: Không."""
    db = _load_db()
    all_sessions = db["sessions"]
    res = {k: [] for k in ("session_statuses", "mismatches", "room_changes", "time_changes", "lecturer_changes",
                           "overlaps", "anomalies", "group_allocation")}
    for s in schedule_bundle.get("matched_sessions", []):
        cite = s.get("citation") or _cite(s)
        label = "%s %s %s %s" % (s["date"], s["class_name"], s["session_code"], cite)
        lab = s.get("lab_sheet") or {}
        st = s["official_status"]
        res["session_statuses"].append({
            "label": label, "status": st, "official_rooms": s.get("official_rooms", []),
            "planned_rooms": s.get("planned_rooms", []), "extra_rooms": s.get("extra_rooms", []),
            "previous_rooms": s.get("previous_rooms", []), "lab_rooms": lab.get("lab_rooms", []),
            "citation": cite, "changed_after_confirm": bool(s.get("changed_after_confirm")),
            "time": s["time"], "class_name": s["class_name"], "session_code": s["session_code"], "date": s["date"],
        })

        # 1. Lệch giữa bảng chính thức và bảng lab coach (bảng phụ)
        if lab and lab.get("lab_status") != "NO_ROOM_COLUMN":
            lc, lst, lrooms = "[%s]" % lab["code"], lab["lab_status"], lab.get("lab_rooms", [])
            if st == "CONFIRMED" and lst == "PENDING":
                res["mismatches"].append("%s: bảng chính thức ĐÃ CHỐT %s, bảng lab coach %s vẫn ghi 'chờ xác nhận' (bảng phụ chưa cập nhật)."
                                         % (label, ", ".join(s["official_rooms"]), lc))
            elif st == "CONFIRMED" and lst == "DK" and sorted(lrooms) == sorted(s["official_rooms"]):
                res["mismatches"].append("%s: bảng chính thức ĐÃ CHỐT, bảng lab coach %s vẫn để nhãn 'dk' (cùng phòng)." % (label, lc))
            elif st == "CONFIRMED" and lrooms and sorted(lrooms) != sorted(s["official_rooms"]):
                res["mismatches"].append("%s: HAI BẢNG GHI KHÁC PHÒNG — chính thức %s, bảng lab coach %s ghi %s. Dùng bảng chính thức."
                                         % (label, ", ".join(s["official_rooms"]), lc, ", ".join(lrooms)))
            elif st == "PENDING" and lst == "DK":
                res["mismatches"].append("%s: bảng chính thức CHƯA XÁC NHẬN phòng, nhưng bảng lab coach %s ghi dự kiến %s. "
                                         "KHÔNG được báo các phòng này như phòng đã chốt." % (label, lc, ", ".join(lrooms)))
            elif st == "PENDING" and s.get("planned_rooms") and lst == "PENDING":
                res["mismatches"].append("%s: bảng chính thức có phòng DỰ KIẾN %s (chờ xác nhận); bảng lab coach %s ghi 'chờ xác nhận'."
                                         % (label, ", ".join(s["planned_rooms"]), lc))
            if s.get("changed_after_confirm") and lst == "PENDING":
                res["mismatches"].append("%s: phòng đã ĐỔI sau khi xác nhận nhưng bảng lab coach %s vẫn ghi 'chờ xác nhận' — coach có thể chưa biết."
                                         % (label, lc))

        # 2. Đổi phòng / giờ / giảng viên sau khi đã xác nhận (từ sheet Lịch sử chỉnh sửa)
        for e in s.get("edits", []):
            if e["type"] == "ROOM_CHANGED_AFTER_CONFIRM":
                res["room_changes"].append("%s: ĐỔI PHÒNG SAU KHI ĐÃ XÁC NHẬN lúc %s [%s] — phòng cũ %s → phòng mới %s."
                                           % (label, e["time"], e["code"], ", ".join(ROOM_RE.findall(e["before"])),
                                              ", ".join(ROOM_RE.findall(e["after"]))))
            elif e["type"] == "TIME_CHANGED":
                res["time_changes"].append("%s: ĐỔI GIỜ lúc %s [%s] — %s → %s." % (label, e["time"], e["code"], e["before"], e["after"]))
            elif e["type"] == "LECTURER_CHANGED":
                res["lecturer_changes"].append("%s: ĐỔI GIẢNG VIÊN lúc %s [%s] — %s → %s."
                                               % (label, e["time"], e["code"], e["before"], e["after"]))

        # 3. Trùng phòng / trùng coach với buổi khác cùng ngày, giờ chồng nhau
        my_rooms = set(s.get("official_rooms", [])) | set(s.get("extra_rooms", []))
        my_people = {c["name"] for c in lab.get("coaches", [])} | ({lab["key_coach"]} if lab.get("key_coach") else set())
        for o in all_sessions:
            if o["date"] != s["date"] or o.get("session_id") == s.get("session_id") or o["class_name"] == "ALL":
                continue
            if not _overlap(s, o):
                continue
            o_label = "%s %s %s" % (o["class_name"], o["session_code"], _cite(o))
            common = sorted(my_rooms & (set(o.get("official_rooms", [])) | set(o.get("extra_rooms", []))))
            if common:
                res["overlaps"].append("%s: TRÙNG PHÒNG %s với %s (%s)." % (label, ", ".join(common), o_label, o["time"]))
            ol = o.get("lab_sheet") or {}
            o_people = {c["name"] for c in ol.get("coaches", [])} | ({ol["key_coach"]} if ol.get("key_coach") else set())
            both = sorted(my_people & o_people)
            if both:
                res["overlaps"].append("%s: TRÙNG NGƯỜI %s — cũng có tên ở %s (%s) [%s, %s]."
                                       % (label, ", ".join(both), o_label, o["time"], lab.get("code"), ol.get("code")))

        # 4. Ô ghi sai định dạng / không xác định được phòng
        for a in s.get("anomalies", []):
            res["anomalies"].append("%s: %s" % (label, a))

        # 5. Đề xuất chia nhóm (synthetic) cho buổi LAB đã chốt phòng
        alloc = _allocate_groups(s, db["groups"])
        if alloc:
            res["group_allocation"].append({"label": label, "rooms": alloc})

    res["has_any_issue"] = any(res[k] for k in ("mismatches", "room_changes", "time_changes", "lecturer_changes",
                                                 "overlaps", "anomalies"))
    return res


@tool
def draft_notice(class_name: str, summary_text: str, check_result: dict) -> dict:
    """Tên: draft_notice · Đóng gói bản nháp thông báo + HẬU KIỂM BẰNG CODE (G2) trước khi đưa người duyệt.
    Input: class_name (str), summary_text (str) — chữ model soạn, check_result (dict) — kết quả check_conflicts.
    Output: dict {draft, approved: False, guardrail_notes, unknown_rooms}.
        Hậu kiểm: (a) mã phòng nào trong bản nháp không có trong dữ liệu của buổi đó → gắn cờ [⚠ … không có căn cứ];
        (b) buổi chưa xác nhận / không rõ phòng mà bản nháp thiếu nhãn → chèn nhãn CHƯA XÁC NHẬN lên đầu;
        (c) buổi đổi phòng sau khi xác nhận mà bản nháp thiếu nhãn → chèn nhãn ĐỔI PHÒNG; (d) thiếu mã nguồn → đính kèm.
    Tác động ra ngoài: Không — chỉ tạo bản nháp chờ người duyệt, không gửi."""
    notes, banners = [], []
    statuses = check_result.get("session_statuses", [])
    allowed = set()
    for st in statuses:
        for k in ("official_rooms", "planned_rooms", "extra_rooms", "previous_rooms", "lab_rooms"):
            allowed |= set(st.get(k, []))
    for line in check_result.get("room_changes", []) + check_result.get("mismatches", []) + check_result.get("anomalies", []):
        allowed |= set(ROOM_RE.findall(line))

    text = summary_text.strip()
    unknown = sorted(set(ROOM_RE.findall(text)) - allowed)
    for r in unknown:
        text = re.sub(r"\b%s\b" % r, "[⚠ %s: không có căn cứ trong bảng phân công]" % r, text)
    if unknown:
        notes.append("Mã phòng không có trong dữ liệu của buổi này, đã gắn cờ: " + ", ".join(unknown))

    up = text.upper()
    for st in statuses:
        if st["status"] in ("PENDING", "UNCLEAR") and "CHƯA XÁC NHẬN" not in up:
            banners.append("⚠ PHÒNG CHƯA XÁC NHẬN — %s: bảng chính thức chưa chốt phòng. Không gửi như phòng đã chốt; hỏi lại ban đào tạo."
                           % st["label"])
        if st["changed_after_confirm"] and "ĐỔI PHÒNG" not in up:
            banners.append("⚠ ĐỔI PHÒNG — %s: phòng đã đổi sau khi xác nhận; phòng hiện hành: %s (phòng cũ: %s)."
                           % (st["label"], ", ".join(st["official_rooms"]), ", ".join(st["previous_rooms"])))
    if banners:
        notes.append("Đã chèn %d nhãn cảnh báo còn thiếu trong bản nháp" % len(banners))

    missing_cites = [st["citation"] for st in statuses if st["citation"] not in text]
    if missing_cites:
        notes.append("Đính kèm mã nguồn còn thiếu: " + ", ".join(missing_cites))

    parts = ["=== BẢN NHÁP CHỜ KEY COACH DUYỆT — HỆ THỐNG KHÔNG TỰ GỬI ==="]
    parts += banners
    parts.append(text)
    parts.append("-" * 60)
    if missing_cites:
        parts.append("Nguồn: " + ", ".join(missing_cites))
    if notes:
        parts.append("Hậu kiểm (code): " + " | ".join(notes))
    parts.append("Đối chiếu theo bảng phân công xuất lúc 21:00 27/04/2027 (data giả lập BTC). Phần do AI soạn — người duyệt chịu trách nhiệm trước khi gửi.")
    return {"class_name": class_name, "approved": False, "guardrail_notes": notes, "unknown_rooms": unknown,
            "draft": "\n".join(parts)}
