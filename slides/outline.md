# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☐ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☐ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☐ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☐ |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☐ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☐ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☐ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần) — *đề xuất theo phân công ở `TEAMS.md`, nhóm chốt*:

| Trang | Người nói |
|---|---|
| 1, 2 | Vũ Văn Hảo |
| 3, 7, 8 | Vũ Đức Thắng |
| 4 (demo) | Bùi Mạnh Linh |
| 5 | Nguyễn Mạnh Quyền |
| 6 | Vũ Văn Hảo |

**Nguồn slide:** `slides/demo-slides.html`. Ô tô vàng là chỗ chờ số. Xuất PDF: mở file bằng Edge / Chrome → In → Lưu thành PDF → Lề: Không, bật "Đồ hoạ nền" → lưu `demo-slides.pdf` ở thư mục gốc.

## Kịch bản video dự phòng *(khoảng 90 giây, quay màn hình với model thật)*

1. `python run.py`, quay rõ dòng cuối có tên model và số token.
2. Ca thường: `Soạn thông báo phòng cho L3A LAB 9 sáng 27/04.` → chỉ 4 phòng và mã ô.
3. Ca khó: câu B14 (phòng dự kiến của bảng lab coach) → nhãn CHƯA XÁC NHẬN.
4. Thiếu thông tin: câu B19 → hỏi lại lớp, "gọi model 0 lần".
5. Từ chối: câu B24 (tự chốt và tự gửi) → G1 chặn.

Không để `.env` hoặc API key xuất hiện trên màn hình.
