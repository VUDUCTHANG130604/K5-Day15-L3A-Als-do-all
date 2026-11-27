"""Công cụ của bài toán A5 (Vận hành đào tạo: lịch, phòng, phân công) — NHÓM VIẾT.

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không.
Công cụ có tác động ra ngoài: KHÔNG tự làm, chỉ trả về bản nháp chờ người duyệt.
"""
import json
import os
import re
from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "schedule_data.json")


def _load_db() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _parse_query(query: str) -> dict:
    """Trích xuất ngày, lớp, buổi (LAB/LEC/HACKATHON), ca học (Sáng/Chiều) và nhóm từ câu hỏi tự nhiên."""
    q_upper = query.upper()
    q_lower = query.lower()

    # 1. Tìm ngày dạng DD/MM hoặc DD-MM
    dates = re.findall(r"\b(\d{1,2})[/-](\d{1,2})\b", query)
    norm_dates = ["%02d/%02d" % (int(d), int(m)) for d, m in dates]

    # 2. Tìm tên lớp (L3A, L3B, L2A, L2B, L3AB)
    classes = re.findall(r"\b(L3AB|L3A|L3B|L2A|L2B)\b", q_upper)
    classes = list(dict.fromkeys(classes))

    # 3. Tìm mã buổi (LAB 5, LAB 10, LEC 8, HACKATHON...)
    sessions = []
    for m in re.finditer(r"\b(LAB|LEC)\s*(\d+)\b", q_upper):
        sessions.append("%s %s" % (m.group(1), m.group(2)))
    if "HACKATHON" in q_upper:
        sessions.append("HACKATHON")

    # 4. Tìm ca học (Sáng / Chiều)
    shift = None
    if "sáng" in q_lower or "sang" in q_lower:
        shift = "Sáng"
    elif "chiều" in q_lower or "chieu" in q_lower:
        shift = "Chiều"

    # 5. Tìm nhóm cụ thể (Nhóm 1, Nhóm 2...)
    groups = [int(g) for g in re.findall(r"nhóm\s*(\d+)", q_lower)]

    return {
        "dates": norm_dates,
        "classes": classes,
        "sessions": sessions,
        "shift": shift,
        "groups": groups,
    }


@tool
def get_schedule(query: str) -> dict:
    """Tên: get_schedule · Tra cứu lịch phân công chính thức, lịch sử sửa, bảng lab coach và danh sách nhóm.
    Input: query (str) — câu hỏi chứa ngày, lớp (L3A/L3B/L2A/L2B) hoặc mã buổi (LAB/LEC).
    Output: dict gồm matched_sessions, same_slot_sessions (để kiểm tra trùng phòng), groups và metadata.
    Tác động ra ngoài: Không (chỉ đọc dữ liệu từ data/schedule_data.json)."""
    db = _load_db()
    parsed = _parse_query(query)
    all_sessions = db.get("sessions", [])

    matched = []
    for s in all_sessions:
        date_ok = (not parsed["dates"]) or (s["date"] in parsed["dates"])
        s_classes = [s["class_name"]] + s.get("also_applies_to", [])
        class_ok = (not parsed["classes"]) or any(c in s_classes for c in parsed["classes"])
        sess_ok = (not parsed["sessions"]) or (s["session_code"] in parsed["sessions"])
        shift_ok = (not parsed["shift"]) or (parsed["shift"].lower() in s["shift"].lower())

        # Cần khớp ít nhất ngày hoặc mã buổi cụ thể
        if (parsed["dates"] or parsed["sessions"]) and date_ok and class_ok and sess_ok and shift_ok:
            matched.append(s)

    # Nếu lọc có ca học (shift) mà rỗng, thử bỏ điều kiện shift (ví dụ buổi đổi sang Chiều-Tối)
    if not matched and (parsed["dates"] or parsed["sessions"]):
        for s in all_sessions:
            date_ok = (not parsed["dates"]) or (s["date"] in parsed["dates"])
            s_classes = [s["class_name"]] + s.get("also_applies_to", [])
            class_ok = (not parsed["classes"]) or any(c in s_classes for c in parsed["classes"])
            sess_ok = (not parsed["sessions"]) or (s["session_code"] in parsed["sessions"])
            if date_ok and class_ok and sess_ok:
                matched.append(s)

    # Lấy các buổi học khác cùng ngày & cùng khung giờ để check_conflicts phát hiện trùng phòng/trùng người
    matched_ids = {s["session_id"] for s in matched}
    matched_dates = {s["date"] for s in matched}
    same_slot = [
        s for s in all_sessions
        if s["date"] in matched_dates and s["session_id"] not in matched_ids
    ]

    # Lấy danh sách nhóm của các lớp liên quan
    target_classes = parsed["classes"] or list({s["class_name"] for s in matched if s["class_name"] in db["groups"]})
    class_groups = {c: db["groups"].get(c, []) for c in target_classes if c in db["groups"]}

    return {
        "parsed_query": parsed,
        "metadata": db.get("metadata", {}),
        "matched_sessions": matched,
        "same_slot_sessions": same_slot,
        "class_groups": class_groups,
        "staff_aliases": db.get("staff_aliases", {}),
        "available_sessions_summary": [
            "%s %s (%s - %s)" % (s["date"], s["class_name"], s["session_code"], s["shift"])
            for s in all_sessions
        ],
    }


@tool
def check_conflicts(schedule_bundle: dict) -> dict:
    """Tên: check_conflicts · Kiểm tra xung đột lịch, lệch bảng, đổi phòng, vượt sức chứa và chuẩn hóa tên bằng code Python thuần.
    Input: schedule_bundle (dict) — kết quả trả về từ get_schedule.
    Output: dict gồm status_summary, mismatches, room_changes, time_changes, overlaps, capacity_warnings, name_warnings.
    Tác động ra ngoài: Không (chạy bằng logic code thuần, không gọi AI)."""
    matched = schedule_bundle.get("matched_sessions", [])
    same_slot = schedule_bundle.get("same_slot_sessions", [])
    class_groups = schedule_bundle.get("class_groups", {})
    aliases = schedule_bundle.get("staff_aliases", {})

    mismatches = []
    room_changes = []
    time_changes = []
    overlaps = []
    capacity_warnings = []
    name_warnings = []
    session_statuses = []

    for s in matched:
        sid = "%s %s %s (%s)" % (s["date"], s["class_name"], s["session_code"], s["official_cell"])
        off_status = s.get("official_status", "UNKNOWN")
        off_rooms = s.get("official_rooms", [])
        lab_status = s.get("lab_sheet_status", "")
        lab_rooms = s.get("lab_sheet_rooms", [])
        lab_code = s.get("lab_sheet_code", "LAB-SHEET")

        session_statuses.append({
            "session_id": s["session_id"],
            "label": sid,
            "official_status": off_status,
            "official_cell": s["official_cell"],
            "official_rooms": off_rooms,
            "lab_sheet_rooms": lab_rooms,
        })

        # 1. Kiểm tra lệch giữa Bảng phân công chính thức và Bảng Lab Coach
        if off_status == "CONFIRMED" and lab_status == "PENDING_IN_LAB_SHEET":
            mismatches.append(
                "LỆCH BẢNG [%s vs %s]: Bảng phân công chính thức [%s] ĐÃ CHỐT phòng (%s), "
                "nhưng bảng Lab Coach [%s] vẫn đang ghi 'chờ xác nhận' (bản cũ chưa cập nhật)."
                % (s["official_cell"], lab_code, s["official_cell"], ", ".join(off_rooms), lab_code)
            )
        elif off_status == "CONFIRMED" and lab_status == "DK_SAME_ROOM":
            mismatches.append(
                "LỆCH TRẠNG THÁI [%s vs %s]: Bảng phân công chính thức [%s] ĐÃ XÁC NHẬN phòng (%s), "
                "còn bảng Lab Coach [%s] vẫn để nhãn dự kiến (%s)."
                % (s["official_cell"], lab_code, s["official_cell"], ", ".join(off_rooms), lab_code, ", ".join(lab_rooms))
            )
        elif off_status == "CONFIRMED" and lab_status == "STALE_CONFIRMED":
            mismatches.append(
                "LỆCH PHÒNG NGUY HIỂM [%s vs %s]: Bảng phân công chính thức [%s] đã đổi sang phòng mới (%s), "
                "nhưng bảng Lab Coach [%s] vẫn lưu phòng cũ (%s)!"
                % (s["official_cell"], lab_code, s["official_cell"], ", ".join(off_rooms), lab_code, ", ".join(lab_rooms))
            )
        elif off_status == "PENDING" and lab_status == "DK_WHILE_OFFICIAL_PENDING":
            mismatches.append(
                "CẢNH BÁO NGUỒN SỰ THẬT [%s vs %s]: Bảng phân công chính thức [%s] đang ghi 'Phòng: chờ xác nhận' (CHƯA CHỐT), "
                "trong khi bảng Lab Coach [%s] ghi phòng dự kiến (%s). TUYỆT ĐỐI KHÔNG báo các phòng dự kiến này như phòng đã chốt!"
                % (s["official_cell"], lab_code, s["official_cell"], lab_code, ", ".join(lab_rooms))
            )
        elif off_status == "MISSING_IN_OFFICIAL":
            mismatches.append(
                "CHƯA CÓ TRÊN BẢNG CHÍNH THỨC [%s]: Buổi %s %s ngày %s chỉ mới có trên bảng Lab Coach [%s] (%s), "
                "nhưng ô [%s] trên bảng phân công chính thức đang TRỐNG. Cần xác minh với Ban đào tạo trước khi thông báo!"
                % (s["official_cell"], s["class_name"], s["session_code"], s["date"], lab_code, ", ".join(lab_rooms), s["official_cell"])
            )
        elif off_status == "ONLINE" and lab_status == "STALE_DK":
            mismatches.append(
                "CHUYỂN ONLINE [%s vs %s]: Bảng phân công chính thức [%s] đã chuyển buổi học sang ONLINE, "
                "không dùng phòng dự kiến cũ (%s) trên bảng phụ."
                % (s["official_cell"], lab_code, s["official_cell"], ", ".join(lab_rooms))
            )

        # 2. Kiểm tra lịch sử đổi phòng / đổi giờ sau khi đã xác nhận
        if s.get("changed_after_confirm"):
            prev = ", ".join(s.get("previous_rooms", [])) or "phòng dự kiến trước đó"
            curr = ", ".join(off_rooms)
            edits = s.get("edit_history", [])
            last_edit = edits[-1] if edits else {}
            room_changes.append(
                "ĐỔI PHÒNG KHẨN [%s · %s lúc %s]: Phòng cũ (%s) -> Phòng mới (%s). Chi tiết: %s"
                % (s["official_cell"], last_edit.get("code", "EDIT"), last_edit.get("time", ""), prev, curr, last_edit.get("after", ""))
            )

        if s.get("time_changed"):
            edits = s.get("edit_history", [])
            last_edit = edits[-1] if edits else {}
            time_changes.append(
                "ĐỔI KHUNG GIỜ HỌC [%s · %s]: Giờ cũ (%s) -> Giờ mới (%s)."
                % (s["official_cell"], last_edit.get("code", "EDIT"), s.get("previous_time", "14:00-18:00"), s["time"])
            )

        # 3. Kiểm tra trùng phòng & trùng Lab Coach với các lớp khác cùng ngày/ca
        for other in same_slot:
            if other.get("time") == s.get("time") or other.get("shift") == s.get("shift"):
                common_rooms = sorted(set(off_rooms) & set(other.get("official_rooms", [])))
                if common_rooms:
                    overlaps.append(
                        "TRÙNG PHÒNG HỌC: Phòng %s ngày %s (%s) đang bị xếp trùng giữa %s %s [%s] và %s %s [%s]."
                        % (", ".join(common_rooms), s["date"], s["time"],
                           s["class_name"], s["session_code"], s["official_cell"],
                           other["class_name"], other["session_code"], other["official_cell"])
                    )
                s_coaches = {c["standard_name"] for c in s.get("coaches", [])}
                o_coaches = {c["standard_name"] for c in other.get("coaches", [])}
                common_coaches = sorted(s_coaches & o_coaches)
                if common_coaches:
                    overlaps.append(
                        "TRÙNG NHÂN SỰ (LAB COACH): %s đang bị phân công trùng ca %s ngày %s ở cả %s %s [%s] và %s %s [%s]."
                        % (", ".join(common_coaches), s["time"], s["date"],
                           s["class_name"], s["session_code"], s["official_cell"],
                           other["class_name"], other["session_code"], other["official_cell"])
                    )

        # 4. Kiểm tra sức chứa phòng so với sĩ số nhóm học viên
        c_groups = {g["name"]: g["size"] for g in class_groups.get(s["class_name"], [])}
        for c_info in s.get("coaches", []):
            assigned_groups = c_info.get("groups", [])
            total_students = sum(c_groups.get(g_name, 23) for g_name in assigned_groups)
            cap = c_info.get("capacity", 50)
            if total_students > cap:
                capacity_warnings.append(
                    "VƯỢT SỨC CHỨA PHÒNG [%s]: Phòng %s có sức chứa tối đa %d chỗ nhưng được xếp cho %s (tổng %d học viên, vượt %d chỗ)."
                    % (s["official_cell"], c_info["room"], cap, " + ".join(assigned_groups), total_students, total_students - cap)
                )

        # 5. Kiểm tra tên Giảng viên / Lab Coach gõ lệch danh sách chuẩn
        if s.get("lecturer"):
            raw_lec = s["lecturer"].get("raw_name", "")
            std_lec = s["lecturer"].get("standard_name", aliases.get(raw_lec, raw_lec))
            if raw_lec != std_lec:
                name_warnings.append("Chuẩn hóa tên Giảng viên [%s]: '%s' -> '%s'." % (s["official_cell"], raw_lec, std_lec))

        for c_info in s.get("coaches", []):
            raw_c = c_info.get("raw_name", "")
            std_c = c_info.get("standard_name", aliases.get(raw_c, raw_c))
            if raw_c != std_c:
                name_warnings.append("Chuẩn hóa tên nhân sự [%s]: '%s' -> '%s' (phòng %s)." % (s["official_cell"], raw_c, std_c, c_info["room"]))

    return {
        "found_count": len(matched),
        "session_statuses": session_statuses,
        "mismatches": mismatches,
        "room_changes": room_changes,
        "time_changes": time_changes,
        "overlaps": overlaps,
        "capacity_warnings": capacity_warnings,
        "name_warnings": name_warnings,
        "has_any_issue": bool(mismatches or room_changes or time_changes or overlaps or capacity_warnings or name_warnings),
    }


@tool
def draft_notice(class_name: str, summary_text: str, check_result: dict) -> dict:
    """Tên: draft_notice · Đóng gói bản nháp thông báo lịch/phòng học kèm chốt chặn hậu kiểm mã phòng và mã nguồn.
    Input: class_name (str), summary_text (str) — nội dung AI soạn, check_result (dict) — kết quả từ check_conflicts.
    Output: dict {"draft": str, "approved": False, "guardrail_notes": list} — bản nháp chờ Key Coach duyệt.
    Tác động ra ngoài: Không (chỉ tạo bản nháp chờ người duyệt, tuyệt đối không tự động gửi)."""
    guardrail_notes = []
    statuses = check_result.get("session_statuses", [])

    # Hậu kiểm bằng code (Deterministic Guardrail G2):
    # 1. Nếu có buổi PENDING hoặc MISSING_IN_OFFICIAL, đảm bảo bản nháp có cảnh báo rõ CHƯA XÁC NHẬN
    for st in statuses:
        if st["official_status"] in ("PENDING", "MISSING_IN_OFFICIAL"):
            guardrail_notes.append(
                "CHỐT CHẶN AN TOÀN [%s]: Buổi học đang ở trạng thái '%s' trên bảng chính thức — CẤM báo phòng dự kiến (%s) như phòng đã chốt."
                % (st["official_cell"], st["official_status"], ", ".join(st["lab_sheet_rooms"]) or "trống")
            )

    # 2. Đảm bảo mọi mã nguồn chính thức [K9-GD1/...] đều có mặt trong bản nháp
    missing_sources = [
        st["official_cell"] for st in statuses
        if st["official_cell"] and st["official_cell"].split(" ")[0] not in summary_text
    ]
    if missing_sources:
        guardrail_notes.append("Tự động đính kèm mã nguồn chính thức: " + ", ".join("[%s]" % c for c in missing_sources))

    header = "=== [BẢN NHÁP CHỜ KEY COACH / TRỢ GIẢNG DUYỆT — HỆ THỐNG KHÔNG TỰ ĐỘNG GỬI] ==="
    footer_lines = [
        "--------------------------------------------------------------------------------",
        "Trạng thái: BẢN NHÁP (Chờ người duyệt trước khi đăng Discord/Zalo/Email)",
        "Nguồn đối chiếu gốc: teaching-schedule.xlsx (Bản xuất 21:00 27/04/2027) & lab-coach-schedule.xlsx",
    ]
    if guardrail_notes:
        footer_lines.insert(1, "Hậu kiểm an toàn (Code Guardrail): " + " | ".join(guardrail_notes))

    full_draft = "%s\n%s\n%s" % (header, summary_text.strip(), "\n".join(footer_lines))
    return {
        "class_name": class_name or "L3A/L3B",
        "approved": False,
        "guardrail_notes": guardrail_notes,
        "draft": full_draft,
    }
