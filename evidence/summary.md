# Tổng hợp bằng chứng pain

> Guide bước 1.2 · rubric R1. Số dưới đây chạy lại được bằng `python evidence/survey/count.py`.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data | ☐ (không làm — data `training-ops` là giả lập, không tính) | — |
| Phỏng vấn | ☐ (không làm) | — |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **n = 23** — *xem giới hạn ở mục 6* | `evidence/survey/questions.md` · `results.csv` · `count.py` |

## 2. Số chính (khảo sát, N = 23: 21 học viên, 2 lab coach; 20 L3A, 3 L3B)

| Đếm gì (4 tuần qua, trừ khi ghi khác) | x / N | % |
|---|---|---|
| Biết ≥1 buổi có phòng **đổi hoặc chỉ chốt trong 24 giờ** trước giờ học (C1) | 21/23 | 91% |
| … trong đó ≥3 buổi | 6/23 | 26% |
| **Nhận báo đổi phòng muộn hoặc sau khi đã báo** (C4) | 16/23 | 70% |
| **Hai nguồn ghi hai phòng khác nhau** (C4) | 11/23 | 48% |
| Không biết buổi đã chuyển online (C4) | 8/23 | 35% |
| Đến nhầm phòng (C4) | 7/23 | 30% |
| Tên bị lệch danh sách (C4) | 4/23 | 17% |
| Gặp ≥1 tình huống ở C4 | 20/23 | 87% |
| Lần gần nhất mất **≥15 phút** mới chắc chắn phòng (C3) | 12/23 | 52% |
| … mất hơn 30 phút | 6/23 | 26% |
| Có ≥1 hậu quả: đến muộn / lỡ một phần buổi / ảnh hưởng điểm danh, điểm / phải nhờ người khác (C6) | 19/23 | 83% |
| Đến muộn (C6) | 12/23 | 52% |
| Ảnh hưởng điểm danh hoặc điểm (C6) | 10/23 | 43% |
| Phải dùng ≥2 kênh mới biết phòng cuối cùng (C2) | 14/23 | 61% |
| Không chắc phòng thì hỏi trợ giảng / coach (L1) | 14/23 | 61% |

**Nhánh người vận hành (lab coach), n = 2 — không ghi %:**
- Coach 1 (L3B): 1–4 buổi phải đối chiếu / gửi thông báo trong 4 tuần; lần gần nhất mất 10–30 phút; dùng bảng lịch ban đào tạo + bảng đội lab coach + hỏi trực tiếp người phụ trách; thông báo từng sai và **đã có người bị ảnh hưởng**.
- Coach 2 (L3A): 0 buổi; dưới 10 phút; dùng bảng đội lab coach + form đổi ca; thông báo từng sai nhưng **tự sửa kịp**; luôn muốn tự xem lại thông báo "buổi chuyển online" và "phòng chưa được xác nhận".

## 3. Trích dẫn nguyên văn (câu C5, giữ nguyên chính tả, bỏ thông tin nhận diện)

1. "Vào được phòng theo lịch được 30 phút mới thấy email thông báo đổi phòng và mất thêm 15 phút di chuyển" — phiếu R10, học viên L3A
2. "Mình nhận được lịch đổi phòng khi mình đã vào phòng học gốc rồi, mình mất thêm 15p để chuyển phòng học" — phiếu R23, học viên L3A
3. "khi đi học mình bị đổi lớp và thời gian học, xong lớp đó cũng không đủ chỗ để ngồi, mất rất lâu mới biết chính xác phòng học khiến thời gian làm lab bị ngắn đi" — phiếu R12, học viên L3A
4. "Phòng học đã có lớp học trước dẫn đến việc bị thay đổi phòng học, mất 30 phút và các học viên, giảng viên bị ảnh hưởng" — phiếu R11, học viên L3A
5. "lần gần nhất là bi trùng phòng học với lớp khác. Hậu quả phải chờ 30p mới được vào phong" — phiếu R04, học viên L3A
6. "chùng phòng học và phải chuyển phòng khác" — phiếu R15, học viên L3A

(Mã phiếu R01–R23 = thứ tự dòng trong `results.csv`.)

## 4. Các nguồn có khớp nhau không

Chỉ có một nguồn thật (khảo sát) → **chưa có nguồn thứ hai kiểm lại** (rubric R1, tiêu chí 3).
Đối chiếu tham khảo với data **giả lập** của BTC (không tính là bằng chứng): data có 20/113 buổi còn "chờ xác nhận" lúc xuất bảng và 16/29 buổi lab đợt 2 lệch giữa hai bảng — cùng chiều với 48% người trả lời gặp "hai nguồn ghi hai phòng khác nhau". **Lệch:** 3 phiếu (R04, R11, R15) kể bị **trùng phòng với lớp khác**, nhưng data giả lập không có ca trùng nào.

## 5. Kết luận

Giả thuyết (`evidence/hypothesis.md`): **phải đổi.**
- **Đúng ở phía học viên nhận lịch:** phòng đổi / chốt sát giờ là chuyện thường gặp (21/23), thông báo đến muộn (16/23), hai nguồn lệch nhau (11/23), và có hậu quả cụ thể (19/23 — đến muộn, lỡ buổi, ảnh hưởng điểm danh).
- **Chưa kiểm được ở phía key coach / trợ giảng** (người dùng chính trong lát cắt): chỉ 2 lab coach trả lời; 1/2 kể mất 10–30 phút và từng gửi sai có người bị ảnh hưởng. Con số "20–30 phút / buổi" trong giả thuyết vẫn là *(tự ước tính)*.
- **Điều vẫn chưa biết:** thông báo đến muộn là do người gửi chậm (đối chiếu lâu) hay do trường chốt phòng muộn — khảo sát không tách được hai nguyên nhân này.

## 6. Giới hạn

- **Đúng người dùng:** 21/23 là học viên — người *nhận* thông báo, chịu hậu quả; người *soạn* thông báo (key coach) chỉ n = 2.
- **Ngoài nhóm:** 6/23 phiếu nhận form qua "Bạn bè trong nhóm làm sản phẩm" (bạn bè của thành viên). Nhóm xác nhận (27/11/2026): **không thành viên nào tự điền form** → N = 23 đều là người ngoài nhóm.
- Mẫu tự chọn qua nhóm Zalo / bạn bè, lệch về L3A (20/23) → % không đại diện toàn khoá.
- 2 phiếu vừa chọn tình huống ở C4 vừa chọn "Không gặp" (mâu thuẫn) — vẫn tính theo lựa chọn tình huống; nếu loại 2 phiếu này thì "gặp ≥1 tình huống" là 18/21.
- Không hỏi lớp học cụ thể / ngày → không ghép được với lịch.
