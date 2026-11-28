# Nhật ký dùng AI trong quá trình làm bài (`docs/ai-usage.md`)

> Ghi rõ nhóm đã dùng công cụ AI / coding agent nào vào việc gì, và ai trong nhóm kiểm lại phần nào. Mỗi người phải giải thích được phần có tên mình.

## 1. Công cụ AI đã dùng
- **Coding agent (Antigravity):** bản CP2 đầu tiên — phân tích đề A5 (`detai.md`), khung 3 công cụ, luồng workflow, nháp spec / benchmark / metric. Bản này có `data/schedule_data.json` viết tay lệch với xlsx gốc; đã thay ở bước dưới.
- **Coding agent (Claude Code):** đọc đề và rubric, viết `CONTEXT.md`; rà bản CP2; viết `data/build_schedule.py` (trích xlsx bằng thư viện chuẩn), viết lại `codebase/tools.py`, `codebase/agent.py` (G1 theo loại yêu cầu, G2 hậu kiểm mã phòng), viết lại 28 câu thử theo ô dữ liệu, cập nhật DATA_CARD, metric spec, spec, eval/README.
- **Coding agent (Claude Code), sáng 28/11 (CP4):** cài cải tiến hỏi lại bằng code trong `codebase/agent.py`; cập nhật spec, eval/report.md, eval/README.md, cost-estimate; sửa số lệch ở spec §1–§2; dựng slide.

## 2. Người kiểm lại *(mỗi người tự điền sau khi kiểm xong — chưa kiểm thì để trống)*
- **Vũ Đức Thắng (Đội trưởng):** lát cắt, kiến trúc, chuẩn "đạt" §7 — __
- **Vũ Văn Hảo:** __
- **Bùi Mạnh Linh:** đối chiếu vài buổi trong `schedule_data.json` với xlsx gốc (vd F18, F29, F36) — __
- **Nguyễn Mạnh Quyền:** đọc từng `expected` trong `eval/benchmark.csv` đối chiếu với ô xlsx ghi ở cột `source` — __
