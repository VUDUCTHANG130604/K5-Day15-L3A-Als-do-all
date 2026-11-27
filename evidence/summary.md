# Tổng hợp bằng chứng pain

> Guide bước 1.2 · rubric R1. Số dưới đây chạy lại được bằng `python evidence/survey/count.py`.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data | ☐ (không làm — data `training-ops` là giả lập, không tính) | — |
| Phỏng vấn | ☐ (không làm) | — |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **n = 29** — *xem giới hạn ở mục 6* | `evidence/survey/questions.md` · `results.csv` · `count.py` |

## 2. Số chính (khảo sát, N = 29: 26 học viên, 2 lab coach, 1 key coach / Day Lead; 25 L3A, 4 L3B)

| Đếm gì (4 tuần qua, trừ khi ghi khác) | x / N | % |
|---|---|---|
| Biết ≥1 buổi có phòng **đổi hoặc chỉ chốt trong 24 giờ** trước giờ học (C1) | 27/29 | 93% |
| … trong đó ≥3 buổi | 9/29 | 31% |
| **Nhận báo đổi phòng muộn hoặc sau khi đã báo** (C4) | 19/29 | 66% |
| **Hai nguồn ghi hai phòng khác nhau** (C4) | 14/29 | 48% |
| Đến nhầm phòng (C4) | 9/29 | 31% |
| Không biết buổi đã chuyển online (C4) | 8/29 | 28% |
| Tên bị lệch danh sách (C4) | 5/29 | 17% |
| Gặp ≥1 tình huống ở C4 | 26/29 | 90% |
| Lần gần nhất mất **≥15 phút** mới chắc chắn phòng (C3) | 12/29 | 41% |
| … mất hơn 30 phút | 6/29 | 21% |
| Có ≥1 hậu quả: đến muộn / lỡ một phần buổi / ảnh hưởng điểm danh, điểm / phải nhờ người khác (C6) | 25/29 | 86% |
| Đến muộn (C6) | 15/29 | 52% |
| Ảnh hưởng điểm danh hoặc điểm (C6) | 12/29 | 41% |
| Phải dùng ≥2 kênh mới biết phòng cuối cùng (C2) | 16/29 | 55% |
| Không chắc phòng thì hỏi trợ giảng / coach (L1) | 14/29 | 48% |

**Nhánh người vận hành (người soạn / gửi thông báo), n = 3 — không ghi %:**

| | Vai | Số buổi phải đối chiếu / gửi (4 tuần) | Lần gần nhất mất | Nguồn dùng để đối chiếu | Thông báo từng sai / thiếu? | Luôn muốn tự xem lại |
|---|---|---|---|---|---|---|
| R03 | Lab coach, L3B | 1–4 | 10–30 phút | Bảng lịch ban đào tạo, bảng đội lab coach, hỏi trực tiếp người phụ trách | Có, **đã có người bị ảnh hưởng** | Không loại nào |
| R05 | Lab coach, L3A | 0 | Dưới 10 phút | Bảng đội lab coach, form đổi ca | Có, tự sửa kịp | Buổi chuyển online, phòng chưa xác nhận |
| R28 | Key coach / Day Lead, L3B | 1–4 | **30–60 phút** | Link danh sách nhóm | Có, tự sửa kịp | Phòng chưa xác nhận |

→ **3/3** người vận hành có thông báo từng bị sai hoặc thiếu trong 4 tuần qua; **2/3** mất ≥10 phút mỗi lần; **2/3** muốn tự xem lại thông báo khi phòng chưa xác nhận.

## 3. Trích dẫn nguyên văn (câu C5, giữ nguyên chính tả, bỏ thông tin nhận diện)

1. "Vào được phòng theo lịch được 30 phút mới thấy email thông báo đổi phòng và mất thêm 15 phút di chuyển" — phiếu R10, học viên L3A
2. "Mình nhận được lịch đổi phòng khi mình đã vào phòng học gốc rồi, mình mất thêm 15p để chuyển phòng học" — phiếu R23, học viên L3A
3. "khi đi học mình bị đổi lớp và thời gian học, xong lớp đó cũng không đủ chỗ để ngồi, mất rất lâu mới biết chính xác phòng học khiến thời gian làm lab bị ngắn đi" — phiếu R12, học viên L3A
4. "Phòng học đã có lớp học trước dẫn đến việc bị thay đổi phòng học, mất 30 phút và các học viên, giảng viên bị ảnh hưởng" — phiếu R11, học viên L3A
5. "lần gần nhất là bi trùng phòng học với lớp khác. Hậu quả phải chờ 30p mới được vào phong" — phiếu R04, học viên L3A
6. "chùng phòng học và phải chuyển phòng khác" — phiếu R15, học viên L3A

(Mã phiếu R01–R29 = thứ tự dòng trong `results.csv`. R25 "Khá lâu và cần thời gia" và R28 "bạn tôi" quá ngắn, không dùng làm trích dẫn.)

## 4. Các nguồn có khớp nhau không

Chỉ có một nguồn thật (khảo sát) → **chưa có nguồn thứ hai kiểm lại** (rubric R1, tiêu chí 3).
Đối chiếu tham khảo với data **giả lập** của BTC (không tính là bằng chứng): data có 20/113 buổi còn "chờ xác nhận" lúc xuất bảng và 16/29 buổi lab đợt 2 lệch giữa hai bảng — cùng chiều với 14/29 (48%) người trả lời gặp "hai nguồn ghi hai phòng khác nhau". **Lệch:** 3 phiếu (R04, R11, R15) kể bị **trùng phòng với lớp khác**, nhưng data giả lập không có ca trùng nào.

## 5. Kết luận

Giả thuyết (`evidence/hypothesis.md`): **đúng một phần, phải đổi cách nói.**
- **Rõ ở phía học viên nhận lịch:** phòng đổi / chốt sát giờ là chuyện thường gặp (27/29), thông báo đến muộn (19/29), hai nguồn lệch nhau (14/29), có hậu quả cụ thể (25/29 — đến muộn, lỡ buổi, ảnh hưởng điểm danh).
- **Có tín hiệu ở phía người soạn thông báo nhưng n quá nhỏ (3):** cả 3 từng gửi thông báo sai / thiếu; key coach duy nhất mất 30–60 phút lần gần nhất, lab coach 10–30 phút và dưới 10 phút. Giả thuyết "20–30 phút / buổi" nằm trong khoảng này nhưng **chưa đủ để kết luận**.
- **Điều vẫn chưa biết:** thông báo đến muộn là do người gửi chậm (đối chiếu lâu) hay do trường chốt phòng muộn — khảo sát không tách được.

## 6. Giới hạn

- **Đúng người dùng:** 26/29 là học viên — người *nhận* thông báo, chịu hậu quả; người *soạn* thông báo chỉ n = 3 (1 key coach, 2 lab coach).
- **Ngoài nhóm:** 10/29 phiếu nhận form qua "Bạn bè trong nhóm làm sản phẩm" (bạn bè của thành viên). Nhóm xác nhận (27/11/2026): **không thành viên nào tự điền form** → N = 29 đều là người ngoài nhóm.
- Mẫu tự chọn qua nhóm Zalo / bạn bè, lệch về L3A (25/29) → % không đại diện toàn khoá.
- 2 phiếu vừa chọn tình huống ở C4 vừa chọn "Không gặp" (mâu thuẫn) — vẫn tính theo lựa chọn tình huống; nếu loại 2 phiếu này thì "gặp ≥1 tình huống" là 24/27.
- Không hỏi lớp học cụ thể / ngày → không ghép được với lịch.
- Câu trả lời thu lúc 2:45–3:57 ngày 27/11/2026; 6 phiếu cuối (R24–R29) nhận sau bản tổng hợp đầu (n = 23) — mọi phiếu đều được giữ, không loại phiếu nào.
