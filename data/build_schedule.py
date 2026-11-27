"""Trích lịch Khoá 9 từ bộ data giả lập của BTC (data/training-ops/*.xlsx) sang data/schedule_data.json.

Chạy lại được:  python data/build_schedule.py [thư_mục_chứa_xlsx]
    Mặc định đọc data-btc/ (thư mục này nằm trong .gitignore — không commit nguyên file BTC).
Chỉ dùng thư viện chuẩn (zipfile + xml.etree): không cần pandas / openpyxl.

Đọc 3 nguồn:
    teaching-schedule.xlsx · sheet "Khoá 9 (GĐ1)"        → bảng phân công CHÍNH THỨC (nguồn sự thật về phòng/giờ)
    teaching-schedule.xlsx · sheet "Lịch sử chỉnh sửa"   → các lần sửa ô (bắt "đổi phòng sau khi đã xác nhận")
    teaching-schedule.xlsx · sheet "Nhan_su"             → bảng tên gõ lệch → tên khớp chuẩn
    lab-coach-schedule.xlsx · sheet "Lịch lab 2604-0805" → bảng PHỤ của đội lab coach (phòng, coach, key coach)
    lab-coach-schedule.xlsx · sheet "Lịch lab 1504-2404" → bảng phụ đợt 1 (không có cột phòng)
Thêm danh sách nhóm học viên TỰ DỰNG (synthetic, seed cố định) vì bộ đề không có.
Mã trích dẫn: [K9-GD1/<ô>] = ô trong sheet "Khoá 9 (GĐ1)"; [LSCS/<dòng>] = dòng trong sheet "Lịch sử chỉnh sửa";
[LAB2/<dòng>] / [LAB1/<dòng>] = dòng đầu nhóm trong sheet lịch lab đợt 2 / đợt 1. Ai mở xlsx cũng kiểm lại được.
"""
import json
import os
import random
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data-btc")
OUT = os.path.join(ROOT, "data", "schedule_data.json")
SEED = 42

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
ROOM_RE = re.compile(r"\b[A-Z]\d{3}\b")
DEFAULT_TIME = {"Sáng": "09:00-13:00", "Chiều": "14:00-18:00"}


def load_sheet(path, sheet):
    """Trả dict {"A1": "giá trị"} của một sheet (hỗ trợ sharedStrings và inlineStr)."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        ss = ["".join(t.text or "" for t in si.iter(M + "t"))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(M + "si")]
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    for sh in wb.find(M + "sheets"):
        if sh.get("name") != sheet:
            continue
        target = rels[sh.get(R + "id")].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        cells = {}
        for c in ET.fromstring(z.read(target)).iter(M + "c"):
            if c.get("t") == "inlineStr":
                cells[c.get("r")] = "".join(x.text or "" for x in c.iter(M + "t"))
                continue
            v = c.find(M + "v")
            if v is not None:
                cells[c.get("r")] = ss[int(v.text)] if c.get("t") == "s" else v.text
        return cells
    raise KeyError("Không thấy sheet %r trong %s" % (sheet, path))


def rooms_in(text):
    return ROOM_RE.findall(text or "")


def norm_time(t):
    return t.replace("–", "-").replace(" ", "")


def norm_code(code):
    """'HACKATHON 15' (bảng lab coach) và 'HACKATHON' (bảng chính thức) là cùng một buổi."""
    code = re.sub(r"\s+", " ", (code or "").strip())
    return "HACKATHON" if code.startswith("HACKATHON") else code


# ---------------------------------------------------------------- bảng chính thức
def parse_cell(text, header_room):
    """Tách một ô lịch nhiều dòng thành các trường. header_room: phòng mặc định theo tiêu đề cột (H209/H210)."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    info = {"online": False, "time": None, "topic": None, "status": None, "rooms": [], "planned_rooms": [],
            "extra_rooms": [], "lecturers": [], "raw_room_line": None, "anomalies": []}
    for l in lines[1:]:
        if l == "Online":
            info["online"] = True
        elif re.match(r"^\d{1,2}:\d{2}\s*[–-]\s*\d{1,2}:\d{2}$", l):
            info["time"] = norm_time(l)
        elif l.startswith("Phòng thêm:"):
            info["extra_rooms"] = rooms_in(l)
        elif l.startswith("Phòng dự kiến:"):
            info["status"], info["planned_rooms"], info["raw_room_line"] = "PENDING", rooms_in(l), l
        elif l.startswith("Phòng:"):
            info["raw_room_line"] = l
            if "chờ xác nhận" in l:
                info["status"] = "PENDING"
            else:
                info["status"], info["rooms"] = "CONFIRMED", rooms_in(l)
        elif l.startswith("Giảng Viên"):
            m = re.match(r"^Giảng Viên:?\s*(?:([A-Z]\d{3}):?\s*)?(.*)$", l)
            name = (m.group(2) if m else "").strip()
            if not name:
                info["anomalies"].append("Ô ghi giảng viên trống: %r" % l)
            elif not l.startswith("Giảng Viên:"):
                info["anomalies"].append("Dòng giảng viên sai định dạng: %r" % l)
            if name:
                info["lecturers"].append({"room": m.group(1), "name": name})
        elif info["topic"] is None:
            info["topic"] = l
    lec_rooms = [x["room"] for x in info["lecturers"] if x["room"]]
    if info["online"]:
        info["status"] = "ONLINE"
    elif info["status"] is None and header_room and any(r != header_room for r in lec_rooms):
        # Ô không có dòng "Phòng:" nhưng dòng giảng viên lại ghi một phòng khác tiêu đề cột → không đoán
        info["status"] = "UNCLEAR"
        info["anomalies"].append("Không có dòng 'Phòng:'; tiêu đề cột ghi %s nhưng dòng giảng viên ghi %s — không xác định được phòng"
                                 % (header_room, ", ".join(lec_rooms)))
    elif info["status"] is None and header_room:
        # Ô LEC không ghi dòng "Phòng:" → học phòng theo tiêu đề cột (quy ước ở data/training-ops/README.md)
        info["status"], info["rooms"] = "CONFIRMED", [header_room]
        info["room_from_header"] = True
    elif info["status"] is None:
        info["status"] = "UNKNOWN"
        info["anomalies"].append("Ô không ghi phòng")
    return info


def build_sessions(T):
    sessions = {}
    date = weekday = None
    for r in range(6, 48):
        if T.get("A%d" % r):
            date, weekday = T["A%d" % r][:5], T.get("B%d" % r)
        shift = "Sáng" if "Sáng" in T.get("C%d" % r, "") else "Chiều"
        for col, header_room in (("D", "H209"), ("E", "H210"), ("F", None), ("G", None), ("H", None)):
            ref = "%s%d" % (col, r)
            text = T.get(ref, "")
            if not text or text == "không có lớp":
                continue
            head = text.split("\n")[0].strip()
            if head in ("NGHỈ LỄ",) or head.startswith("KHAI GIẢNG"):
                key = "%s|%s|%s" % (date, shift, head)
                sessions.setdefault(key, {"date": date, "weekday": weekday, "shift": shift, "time": DEFAULT_TIME[shift],
                                          "class_name": "ALL", "kind": "HOLIDAY" if head == "NGHỈ LỄ" else "OPENING",
                                          "session_code": head, "official_status": "NO_CLASS" if head == "NGHỈ LỄ" else "OPENING",
                                          "official_cells": [ref], "official_rooms": [], "topic": head})
                continue
            m = re.match(r"^(L\d(?:AB|A|B))\s*—\s*(.+)$", head)
            if not m:
                continue
            cls, code = m.group(1), m.group(2).strip()
            if code == "HACKATHON":
                code = "HACKATHON"
            info = parse_cell(text, header_room if code.startswith("LEC") and cls.startswith("L3") else None)
            key = "%s|%s|%s" % (date, cls, code)
            s = sessions.get(key)
            if s is None:
                s = sessions[key] = {
                    "session_id": "%s_%s_%s" % (date.replace("/", ""), cls, code.replace(" ", "")),
                    "date": date, "weekday": weekday, "shift": shift,
                    "time": info["time"] or DEFAULT_TIME[shift], "class_name": cls,
                    "applies_to": ["L3A", "L3B"] if cls == "L3AB" else (["L2A", "L2B"] if cls == "L2AB" else [cls]),
                    "kind": code.split(" ")[0], "session_code": code, "topic": info["topic"],
                    "official_cells": [], "official_status": info["status"], "official_rooms": [],
                    "planned_rooms": [], "extra_rooms": [], "lecturers": [], "anomalies": [],
                }
            s["official_cells"].append(ref)
            s["official_rooms"] += [x for x in info["rooms"] if x not in s["official_rooms"]]
            s["planned_rooms"] += [x for x in info["planned_rooms"] if x not in s["planned_rooms"]]
            s["extra_rooms"] += [x for x in info["extra_rooms"] if x not in s["extra_rooms"]]
            s["lecturers"] += info["lecturers"]
            s["anomalies"] += info["anomalies"]
            for st in ("PENDING", "UNCLEAR"):
                if info["status"] == st or s["official_status"] == st:
                    s["official_status"] = st
                    break
    for s in sessions.values():
        if s.get("official_status") in ("PENDING", "UNCLEAR"):
            s["official_rooms"] = []      # phòng chưa chốt: không có phòng chính thức, chỉ có "dự kiến"
    return sessions


# ---------------------------------------------------------------- lịch sử chỉnh sửa
def build_edits(H, sessions):
    by_cell = {}
    for s in sessions.values():
        for c in s["official_cells"]:
            by_cell.setdefault(c, []).append(s)
    edits = []
    for r in range(2, 200):
        if not H.get("A%d" % r):
            continue
        e = {"code": "LSCS/%d" % r, "time": H["A%d" % r], "editor": H.get("B%d" % r), "cells": H.get("D%d" % r, ""),
             "label": H.get("E%d" % r), "before": H.get("F%d" % r, ""), "after": H.get("G%d" % r, "")}
        b, a = e["before"], e["after"]
        if b.startswith("Phòng:") and "chờ" not in b and a.startswith("Phòng:"):
            e["type"] = "ROOM_CHANGED_AFTER_CONFIRM"
        elif ("chờ xác nhận" in b) and a.startswith("Phòng:"):
            e["type"] = "ROOM_CONFIRMED"
        elif b.startswith("Phòng thêm"):
            e["type"] = "EXTRA_ROOM_CHANGED"
        elif b.startswith("Giảng Viên"):
            e["type"] = "LECTURER_CHANGED"
        elif re.match(r"^\d{1,2}:\d{2}", b):
            e["type"] = "TIME_CHANGED"
        else:
            e["type"] = "OTHER"
        edits.append(e)
        for c in [x.strip() for x in e["cells"].split(",")]:
            for s in by_cell.get(c, []):
                s.setdefault("edit_codes", [])
                if e["code"] not in s["edit_codes"]:
                    s["edit_codes"].append(e["code"])
    for s in sessions.values():
        mine = [e for e in edits if e["code"] in s.get("edit_codes", [])]
        changes = [e for e in mine if e["type"] == "ROOM_CHANGED_AFTER_CONFIRM"]
        if changes:
            s["changed_after_confirm"] = True
            s["previous_rooms"] = rooms_in(changes[0]["before"])
        tchg = [e for e in mine if e["type"] == "TIME_CHANGED"]
        if tchg:
            s["time_changed"] = True
            s["previous_time"] = norm_time(tchg[0]["before"])
    return edits


# ---------------------------------------------------------------- bảng lab coach (bảng phụ)
def build_lab2(L):
    groups = {}
    order = []
    for r in range(1, 400):
        d, cls, ses = L.get("K%d" % r), L.get("L%d" % r), norm_code(L.get("M%d" % r))
        if not (d and cls and ses) or d == "Ngày":
            continue
        key = "%s|%s|%s" % (d[:5], cls, ses)
        g = groups.get(key)
        if g is None:
            raw = L.get("N%d" % r, "")
            main, _, extra = raw.partition("+")
            if raw.strip() == "chờ xác nhận" or main.strip().startswith("chờ xác nhận"):
                status = "PENDING"
            elif main.strip().startswith("dk:"):
                status = "DK"
            else:
                status = "CONFIRMED"
            g = groups[key] = {"code": "LAB2/%d" % r, "date": d[:5], "class_name": cls, "session_code": ses,
                               "shift": L.get("O%d" % r), "raw_room": raw, "lab_status": status,
                               "lab_rooms": rooms_in(main), "lab_extra_rooms": rooms_in(extra),
                               "key_coach": L.get("P%d" % r), "capacity_note": L.get("H%d" % r), "coaches": []}
            order.append(key)
        coach = L.get("D%d" % r)
        if coach:
            g["coaches"].append({"name": coach, "status": L.get("J%d" % r) or ""})
    return groups


def build_lab1(L):
    """Đợt 1 (15/04–24/04): mỗi ngày một khối, không có cột phòng. Ô gộp → ghi ở dòng đầu nhóm."""
    groups = {}
    date = None
    cur = None
    for r in range(1, 400):
        a = L.get("A%d" % r, "")
        m = re.match(r"^Thứ .* - (\d{2}/\d{2})/\d{4}$", a)
        if m:
            date, cur = m.group(1), None
            continue
        if a in ("STT", "") or not a.isdigit():
            continue
        if L.get("B%d" % r):
            key = "%s|%s|%s" % (date, L["B%d" % r], norm_code(L.get("C%d" % r, "")))
            cur = groups[key] = {"code": "LAB1/%d" % r, "date": date, "class_name": L["B%d" % r],
                                 "session_code": L.get("C%d" % r, ""), "shift": L.get("F%d" % r),
                                 "raw_room": None, "lab_status": "NO_ROOM_COLUMN", "lab_rooms": [], "lab_extra_rooms": [],
                                 "key_coach": L.get("E%d" % r), "capacity_note": L.get("G%d" % r), "coaches": []}
        if cur is not None and L.get("D%d" % r):
            cur["coaches"].append({"name": L["D%d" % r], "status": L.get("I%d" % r) or ""})
    return groups


def build_aliases(N):
    aliases = {}
    for r in range(2, 200):
        raw, std = N.get("A%d" % r), N.get("B%d" % r)
        if raw and std and raw != std:
            aliases[raw] = std
    return aliases


def build_groups():
    """Danh sách nhóm học viên TỰ DỰNG (synthetic): bộ đề không có. Seed cố định để chạy lại ra cùng kết quả.
    Quy mô theo tiêu đề bảng phân công: L3A, L3B ~350 HV/lớp; L2A, L2B ~160 HV/lớp."""
    rnd = random.Random(SEED)
    plan = {"L3A": 12, "L3B": 12, "L2A": 6, "L2B": 6}
    out = {}
    for cls, n in plan.items():
        out[cls] = [{"group_id": "%s-N%02d" % (cls, i + 1), "name": "Nhóm %d" % (i + 1),
                     "size": rnd.randint(26, 31)} for i in range(n)]
    return out


def main():
    ts = os.path.join(SRC, "teaching-schedule.xlsx")
    lc = os.path.join(SRC, "lab-coach-schedule.xlsx")
    T = load_sheet(ts, "Khoá 9 (GĐ1)")
    sessions = build_sessions(T)
    edits = build_edits(load_sheet(ts, "Lịch sử chỉnh sửa"), sessions)
    lab = build_lab1(load_sheet(lc, "Lịch lab 1504-2404"))
    lab.update(build_lab2(load_sheet(lc, "Lịch lab 2604-0805")))
    # Nối bảng phụ vào buổi chính thức theo (ngày, lớp, mã buổi)
    for key, g in lab.items():
        s = sessions.get(key)
        if s is None and g["class_name"] in ("L3A", "L3B"):
            s = sessions.get("%s|L3AB|%s" % (g["date"], g["session_code"]))
        if s is not None:
            s["lab_sheet"] = g
    unmatched_lab = [g["code"] for k, g in lab.items() if k not in sessions and
                     "%s|L3AB|%s" % (g["date"], g["session_code"]) not in sessions]
    data = {
        "metadata": {
            "generated_by": "data/build_schedule.py",
            "source_export_time": T.get("D1", "").replace("Bản xuất ", ""),
            "snapshot_now": "27/04/2027 21:00",
            "official_source": "teaching-schedule.xlsx · sheet 'Khoá 9 (GĐ1)' + 'Lịch sử chỉnh sửa' (data giả lập BTC)",
            "secondary_source": "lab-coach-schedule.xlsx · sheet 'Lịch lab 1504-2404' + 'Lịch lab 2604-0805' (data giả lập BTC)",
            "groups_source": "synthetic, seed=%d (bộ đề không có danh sách nhóm)" % SEED,
            "label": "synthetic",
            "unmatched_lab_rows": unmatched_lab,
        },
        "staff_aliases": build_aliases(load_sheet(ts, "Nhan_su")),
        "groups": build_groups(),
        "sessions": sorted(sessions.values(), key=lambda s: (s["date"][3:], s["date"][:2], s["shift"] != "Sáng", s["class_name"])),
        "edit_history": edits,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    n_pending = sum(1 for s in sessions.values() if s["official_status"] == "PENDING")
    n_changed = sum(1 for s in sessions.values() if s.get("changed_after_confirm"))
    print("Đã ghi %s: %d buổi (%d chờ xác nhận, %d đổi phòng sau khi xác nhận) · %d lần sửa · %d nhóm bảng phụ"
          % (os.path.relpath(OUT, ROOT), len(sessions), n_pending, n_changed, len(edits), len(lab)))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
