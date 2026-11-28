# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`):

  | Persona | Tỉ lệ | Phiên / người / tháng | Lượt hỏi / phiên | Nguồn |
  |---|---:|---:|---:|---|
  | `key_coach_it` | 40% | 2 | 1 | Khảo sát O1 (n = 3); tỉ lệ *(tự ước tính)* |
  | `key_coach_vua` | 40% | 6 | 2 | Đếm data giả lập (4–9 buổi / key coach trong ~3,5 tuần); số lượt *(tự ước tính)* |
  | `day_lead_nhieu` | 20% | 20 | 3 | *(tự ước tính)* |

- **Số người soạn thông báo** 3 kịch bản: thấp 6 · cơ sở 10 · cao 15. Nguồn: cơ sở = số key coach khác nhau trong bảng lab coach của data giả lập; thấp và cao *(tự ước tính)*. Chưa có số thật của khoá.
- **Giá** (USD / 1 triệu token, vào – ra; https://ai.google.dev/gemini-api/docs/pricing, theo bảng giá BTC xem 25/11/2026): `gemini-3.1-flash-lite` 0,25 – 1,50 · `gemini-4-hydrogen` 1,50 – 7,50
- **Tỉ lệ đạt** dùng để tính: 25/28 (89%) — lượt `run-3` (lượt 2 sau cải tiến)
- Đo token trên `gemini-3.1-flash-lite`, tính giá `gemini-3.1-flash-lite` và `gemini-4-hydrogen`

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-141820` · 50 phiên (0 lỗi) · seed 42

Chép từ `cost/simulate-1-summary.md`:

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite | $0.00096 | $0.0011 | $0.0600 | $0.0999 | $0.1499 | $0.0100 |
| gemini-4-hydrogen *(token đo trên flash-lite, tính giá model này)* | $0.0052 | $0.0058 | $0.3236 | $0.5393 | $0.8090 | $0.0539 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): 180 phút (7,2 phiên theo persona × 25 phút) đến 500 phút (20 lần × 25 phút). 25 phút / lần là *(tự ước tính)*, là thời gian làm tay, chưa trừ thời gian duyệt bản nháp.
- Chi phí / người / tháng (cơ sở, `gemini-3.1-flash-lite`): $0.010
- **Kết luận một dòng — đáng làm không:** tiền model không phải rào cản (khoảng 1 cent / người / tháng so với vài giờ làm tay); điều cần chứng minh tiếp là thời gian tiết kiệm thật và độ ổn định đầu ra.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
