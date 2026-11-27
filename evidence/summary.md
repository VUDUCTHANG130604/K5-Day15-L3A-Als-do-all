# Tổng hợp bằng chứng pain

> Guide bước 1.2 · rubric R1. Số dưới đây chạy lại được bằng `python evidence/survey/count.py`.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data | ☐ (không làm — data `training-ops` là giả lập, không tính) | — |
| Phỏng vấn | ☐ (không làm) | — |
| Khảo sát (ngưỡng rubric: ≥20 người ngoài nhóm, đúng người dùng) | **29 phiếu**, 26 học viên và 3 người vận hành. Xem giới hạn ở mục 6. | `evidence/survey/questions.md` · `results.csv` · `count.py` |

## 2. Số chính (29 phiếu: 26 học viên, 2 Lab Coach, 1 Key Coach / Day Lead; 25 L3A, 4 L3B)

| Đếm gì (4 tuần qua, trừ khi ghi khác) | x / N | % |
|---|---|---|
| Biết ≥1 buổi có phòng **đổi hoặc chỉ chốt trong 24 giờ** trước giờ học (C1) | 27/29 | 93% |
| Biết ≥3 buổi như vậy (C1) | 9/29 | 31% |
| **Nhận báo đổi phòng muộn hoặc sau khi đã báo** (C4) | 19/29 | 66% |
| **Hai nguồn ghi hai phòng khác nhau** (C4) | 14/29 | 48% |
| Không biết buổi đã chuyển online (C4) | 8/29 | 28% |
| Đến nhầm phòng (C4) | 9/29 | 31% |
| Tên bị lệch danh sách (C4) | 5/29 | 17% |
| Gặp ≥1 tình huống ở C4 | 26/29 | 90% |
| Lần gần nhất mất **≥15 phút** mới chắc chắn phòng (C3) | 12/29 | 41% |
| Lần gần nhất mất hơn 30 phút (C3) | 6/29 | 21% |
| Có ≥1 hậu quả về buổi học hoặc điểm danh: đến muộn / lỡ một phần buổi / ảnh hưởng điểm danh, điểm (C6) | 24/29 | 83% |
| Có ≥1 hậu quả: đến muộn / lỡ một phần buổi / ảnh hưởng điểm danh, điểm / phải nhờ người khác (C6) | 25/29 | 86% |
| Đến muộn (C6) | 15/29 | 52% |
| Ảnh hưởng điểm danh hoặc điểm (C6) | 12/29 | 41% |
| Dùng ≥2 kênh mới biết phòng cuối cùng (C2) | 16/29 | 55% |
| Không chắc phòng thì hỏi trợ giảng / coach (L1) | 14/29 | 48% |

**Nhánh người vận hành gồm 3 người:**
- Coach 1 (L3B): 1–4 buổi phải đối chiếu / gửi thông báo trong 4 tuần; lần gần nhất mất 10–30 phút; dùng bảng lịch ban đào tạo + bảng đội lab coach + hỏi trực tiếp người phụ trách; thông báo từng sai và **đã có người bị ảnh hưởng**.
- Coach 2 (L3A): 0 buổi; dưới 10 phút; dùng bảng đội lab coach + form đổi ca; thông báo từng sai nhưng **tự sửa kịp**; luôn muốn tự xem lại thông báo "buổi chuyển online" và "phòng chưa được xác nhận".
- Key Coach / Day Lead (L3B, R28) báo 1–4 buổi phải đối chiếu hoặc gửi thông báo trong 4 tuần, lần gần nhất mất 30–60 phút. Người này từng tự sửa thông báo trước khi ai bị ảnh hưởng và muốn duyệt lại thông báo phòng chưa xác nhận.

## 3. Trích dẫn nguyên văn (câu C5, giữ nguyên chính tả, bỏ thông tin nhận diện)

1. "Vào được phòng theo lịch được 30 phút mới thấy email thông báo đổi phòng và mất thêm 15 phút di chuyển" — phiếu R10, học viên L3A
2. "Mình nhận được lịch đổi phòng khi mình đã vào phòng học gốc rồi, mình mất thêm 15p để chuyển phòng học" — phiếu R23, học viên L3A
3. "khi đi học mình bị đổi lớp và thời gian học, xong lớp đó cũng không đủ chỗ để ngồi, mất rất lâu mới biết chính xác phòng học khiến thời gian làm lab bị ngắn đi" — phiếu R12, học viên L3A
4. "Phòng học đã có lớp học trước dẫn đến việc bị thay đổi phòng học, mất 30 phút và các học viên, giảng viên bị ảnh hưởng" — phiếu R11, học viên L3A
5. "lần gần nhất là bi trùng phòng học với lớp khác. Hậu quả phải chờ 30p mới được vào phong" — phiếu R04, học viên L3A
6. "chùng phòng học và phải chuyển phòng khác" — phiếu R15, học viên L3A

Mã phiếu R01–R29 tương ứng với thứ tự phản hồi trong `results.csv`, tính từ dòng sau tiêu đề.

## 4. Các nguồn có khớp nhau không

Chỉ có một nguồn thật (khảo sát) → **chưa có nguồn thứ hai kiểm lại** (rubric R1, tiêu chí 3).
Đối chiếu tham khảo với data **giả lập** của BTC (không tính là bằng chứng): data có 20/113 buổi còn "chờ xác nhận" lúc xuất bảng và 16/29 buổi lab đợt 2 lệch giữa hai bảng — cùng chiều với 14/29 (48%) người trả lời gặp "hai nguồn ghi hai phòng khác nhau". **Lệch:** 3 phiếu (R04, R11, R15) kể bị **trùng phòng với lớp khác**, nhưng data giả lập không có ca trùng nào.

## 5. Kết luận

Giả thuyết (`evidence/hypothesis.md`): **phải đổi.**
- **Phía nhận lịch:** 19/29 nhận báo đổi phòng muộn, 14/29 gặp hai nguồn ghi hai phòng khác nhau và 25/29 gặp ít nhất một hậu quả ở C6. Học viên chiếm 26/29 phiếu.
- **Phía soạn thông báo:** có 2 Lab Coach và 1 Key Coach / Day Lead. Người thuộc vai Key Coach / Day Lead duy nhất ở L3B và báo mất 30–60 phút ở lần gần nhất. Mẫu còn nhỏ để ước lượng thời gian đối chiếu điển hình của Key Coach / Trợ giảng L3A. Mức 20–30 phút/buổi trong giả thuyết là *(tự ước tính)*.
- **Điều vẫn chưa biết:** thông báo đến muộn là do người gửi chậm (đối chiếu lâu) hay do trường chốt phòng muộn — khảo sát không tách được hai nguyên nhân này.

## 6. Giới hạn

- **Đúng người dùng:** 26/29 là học viên nhận thông báo. Nhánh vận hành có 3 người, gồm 1 Key Coach / Day Lead ở L3B.
- **Ngoài nhóm:** Nhóm đã xác nhận 23 phiếu đợt đầu đều từ người ngoài nhóm. Tình trạng này của 6 phiếu bổ sung đang chờ xác nhận. Cột C8 ghi kênh nhận form.
- Mẫu tự chọn qua nhóm Zalo và bạn bè, tập trung ở L3A (25/29). Các tỷ lệ mô tả mẫu khảo sát.
- Hai phiếu vừa chọn tình huống ở C4 vừa chọn "Không gặp". Bảng tính theo lựa chọn tình huống. Khi loại hai phiếu này, 24/27 người gặp ít nhất một tình huống ở C4.
- Không hỏi lớp học cụ thể / ngày → không ghép được với lịch.
- Câu trả lời thu lúc 2:45–3:57 ngày 27/11/2026; 6 phiếu cuối (R24–R29) nhận sau bản tổng hợp đầu (n = 23) — mọi phiếu đều được giữ, không loại phiếu nào.
