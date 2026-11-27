# Nhật ký dùng AI trong quá trình làm bài (`docs/ai-usage.md`)

> Ghi rõ nhóm đã dùng công cụ AI / Coding Agent nào vào việc gì, và thành viên nào trong nhóm đã kiểm tra / sửa lại phần nào.

## 1. Công cụ AI đã sử dụng
- **Coding Agent (Antigravity):** Hỗ trợ phân tích đề tài A5 (`detai.md`), cấu trúc hóa dữ liệu lịch mẫu sang `data/schedule_data.json`, viết khung code cho 3 công cụ (`get_schedule`, `check_conflicts`, `draft_notice`) trong `codebase/tools.py` và luồng workflow cố định trong `codebase/agent.py`.

## 2. Phần việc con người trực tiếp quyết định và kiểm tra
- **Vũ Đức Thắng (Đội trưởng):** Chốt lát cắt một câu, quyết định kiến trúc Workflow cố định và chốt ngưỡng chuẩn "đạt" bằng số ở `spec.md` §7 trước 19:30 Thứ Sáu 27/11 (CP2).
- **Vũ Văn Hảo:** Trực tiếp thực hiện phỏng vấn người dùng thật (Key Coach / Trợ giảng L3A), thu thập bằng chứng `evidence/` và chấm chéo độc lập 5 output theo `eval/metric_spec.yaml`.
- **Bùi Mạnh Linh:** Kiểm tra tay toàn bộ 10 bản ghi buổi học, 9 bản ghi lịch sử chỉnh sửa và 15 nhóm học viên trong `data/schedule_data.json`; kiểm thử lệnh `python run.py` đảm bảo chốt chặn hậu kiểm không bao giờ báo phòng dự kiến (`dk`) thành phòng đã chốt.
- **Nguyễn Mạnh Quyền:** Rà soát từng câu trong 20 câu thử của `eval/benchmark.csv` và 4 metric trong `eval/metric_spec.yaml`, đảm bảo mọi `pass_criterion` đều kiểm chứng được bằng mắt đọc.
