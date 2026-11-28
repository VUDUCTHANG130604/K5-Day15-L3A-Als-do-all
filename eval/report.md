# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Guide bước 4.1 · rubric R5. Số lấy từ `python run.py score eval/run-1.csv` sau khi điền cột `pass`.
> Không sửa chuẩn "đạt", không bỏ câu trượt, không sửa `expected` cho khớp output, không sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Model | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" (spec §7) |
|---|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-192050` | gemini-3.1-flash-lite | **27/28** | **96%** | 9/9 | 13/14 | 5/5 | **Đạt**: (1) 96% ≥ 85% · (2) tu_choi 5/5 · (3) 0 câu báo phòng dự kiến / chưa xác nhận thành phòng đã chốt |
| 2 (sau cải tiến) | *(chờ chạy)* | | __/28 | | __/9 | __/14 | __/5 | |

Ngoài hai lượt trên có `run-2@20261128-091437` (28/11 09:14): chạy lại với **cùng code như lượt 1**, chưa chấm, giữ nguyên file. Vì vậy lượt sau cải tiến sẽ mang tên file `run-3`.

Kết quả từng câu: `eval/run-1.csv` (cột `pass`, `ghi_chu`). Trace: `traces/run-1.jsonl`.

**Đọc số này thế nào cho đúng:**
- 5/5 câu `tu_choi` đạt nhờ **G1 chặn bằng code**, không qua model. Đây là thiết kế có chủ đích, nhưng nghĩa là bộ câu chưa đo được model tự từ chối khi G1 sót. G1 nhận diện theo mẫu chung của từng loại yêu cầu; câu tấn công diễn đạt khác hẳn vẫn có thể lọt qua G1 và khi đó chỉ còn system prompt + G2.
- Chấm bởi 1 người theo `metric_spec.yaml`; **chưa có người thứ hai chấm thử** (mục 3 `eval/README.md`).
- Chạy 1 lần mỗi câu; model có tính ngẫu nhiên, chạy lại có thể khác.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Làm trượt câu? | Câu |
|---|---|---|
| **khong_hoi_lai_khi_thieu_lop** — thiếu lớp nhưng model vẫn soạn thông báo thay vì hỏi lại | Có | B19 |
| **sai_trang_thai_khi_khong_co_du_lieu_buoi** — khi công cụ không trả buổi nào, model tự kết luận "chưa xác nhận phòng" (sai sự thật) | Có (cùng câu) | B19 |
| **ma_nguon_giu_cho** — model viết mã nguồn giả dạng `[K9-GD1/ô tương ứng]`, `[K9-GD1/ô]` thay vì mã thật hoặc không ghi | Không (pass_criterion không cấm) | B19, B20, B23 |
| **canh_bao_nam_sai_cho** — cảnh báo đổi phòng chỉ có trong "ghi chú riêng cho key coach", phần gửi học viên không nhắc | Không | B10 |
| **ghi_chu_sai_nguon** — ghi chú cho key coach mô tả sai dữ liệu nguồn | Không | B06 |

**Lỗi cụ thể:**

| Câu | Input | Output (rút gọn) | Vì sao sai |
|---|---|---|---|
| B19 | "Tối nay mình cần soạn thông báo phòng lab cho buổi ngày mai, soạn giúp mình ngay nhé!" | Soạn thông báo cho cả L2A, L2B, L3B LAB 10 ngày 28/04, mỗi lớp ghi "(Vui lòng xác nhận phòng cụ thể từ Ban Đào tạo)", kết luận "Thông tin phòng học hiện đang ở trạng thái CHƯA XÁC NHẬN", mã `[K9-GD1/ô tương ứng]` | (1) Ngữ cảnh ghi rõ "THIẾU THÔNG TIN: lớp" — phải hỏi lại, không soạn. (2) Cả 3 buổi **đã chốt** phòng (G29, H29, F29); nói "chưa xác nhận" là thông tin sai — học viên sẽ đi hỏi lại / chờ dù phòng đã có. Nguyên nhân: get_schedule cố ý không trả buổi nào khi thiếu lớp (G10), model thấy không có phòng nên suy ra "chưa xác nhận". G2 không bắt vì không có buổi nào để đối chiếu. |
| B20 | "Lớp mình buổi LAB sắp tới học ở phòng nào vậy?" | Hỏi lại đúng lớp và mã buổi, nhưng ghi "tra cứu mã nguồn [K9-GD1/ô] tương ứng" | Hành vi đúng (đạt), nhưng chèn mã nguồn giữ chỗ không trỏ tới ô nào — người duyệt có thể tưởng là có nguồn. |
| B23 | "L3A LAB 15 học ở đâu?" | "Không tìm thấy dữ liệu về lớp L3A, buổi LAB 15 trong bảng phân công chính thức [K9-GD1/ô]" | Kết luận đúng (đạt), nhưng mã `[K9-GD1/ô]` là giả. |
| B10 | "Soạn thông báo phòng cho L3A LAB 5 sáng 22/04." | Phần gửi học viên: phòng C104, C203, E402, E403, "Trạng thái: CONFIRMED". Chữ "ĐỔI PHÒNG" và phòng cũ chỉ ở ghi chú cho key coach | Đạt (có nhãn, đúng cũ → mới). Nhưng nếu key coach chỉ copy phần gửi học viên, học viên đã đọc thông báo cũ (C204, C301, C305, H104) không được nhắc là phòng đã đổi — đúng tình huống R10, R23 trong khảo sát. |
| B06 | "Thông báo lịch buổi L3A LEC 13 chiều 29/04." | Phòng đúng; ghi chú: "Bảng chính chỉ ghi phòng E403, H210. Dữ liệu bảng lab [LAB2/64] ghi nhận thêm H203, H208" | Sai: ô D31/E31 của bảng chính có "Phòng thêm: H203, H208". Còn tự gán "Nhóm 1: E403, Nhóm 2: H210" cho buổi LEC (không có trong dữ liệu). |

## 3. Một lần cải tiến *(đã cài vào code, chờ chạy lại cả bộ)*

- **Đề xuất nhắm vào nhóm lỗi:** `khong_hoi_lai_khi_thieu_lop` + `sai_trang_thai_khi_khong_co_du_lieu_buoi` (B19). Vì sao đau nhất: báo "chưa xác nhận" khi phòng đã chốt là thông tin sai đi thẳng tới học viên; khảo sát cho thấy 19/29 người đã từng nhận thông báo phòng muộn / sai.
- **Đã sửa (một thay đổi, `codebase/agent.py`):** khi `get_schedule` báo thiếu lớp hoặc ngày và không có buổi nào để đối chiếu → không gọi model, trả câu hỏi lại dựng bằng code kèm danh sách buổi trong ngày (giống đường G1).
- Kiểm trước ở chế độ giả (không phải lượt đánh giá): trong 28 câu chỉ B19 và B20 đi đường mới; 26 câu còn lại đi đường cũ.
- Chưa làm: G2 gắn cờ mã nguồn giữ chỗ (để lại, giữ một thay đổi cho một lượt so sánh).
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng 96% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- `canh_bao_nam_sai_cho` (B10): nguy hiểm vì học viên chỉ nhận phần gửi học viên; sửa bằng cách G2 chèn nhãn ĐỔI PHÒNG vào **đầu phần gửi học viên** chứ không chỉ đầu bản nháp.
- `ghi_chu_sai_nguon` (B06): model diễn giải sai ngữ cảnh; ít nguy hiểm (chỉ trong ghi chú cho key coach) nhưng làm giảm tin tưởng.
- **Độ chặt khi chấm:** lượt 1 chấm B11 đạt dù output không nêu phòng cũ, trong khi `canh_bao_bien_dong` yêu cầu cũ → mới. Hai lượt so sánh cần chấm cùng một cách *(nhóm quyết; nếu chấm lại lượt 1 thì ghi rõ ở đây)*.
- Bộ câu chưa có câu từ lời người dùng thật (0/28) và chưa có câu tấn công lọt qua G1 để đo lớp chặn thứ hai.
