# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · `data/schedule_data.json` ( phần `sessions` & `staff_aliases` — Trích rút từ `data/training-ops/`)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn dữ liệu nền cho 2 công cụ `get_schedule` và `check_conflicts` trong `codebase/tools.py`; dùng để kiểm thử các ca đối chiếu lịch, bắt lệch giữa 2 bảng và lịch sử đổi phòng sát giờ. |
| **Từ đâu** | Trích rút và chuẩn hóa cấu trúc từ bộ dữ liệu giả lập BTC cấp (`data/training-ops/teaching-schedule.xlsx` — bản xuất `21:00 27/04/2027` và `data/training-ops/lab-coach-schedule.xlsx`). Không commit nguyên file `.xlsx` gốc của BTC. |
| **Xử lý những bước gì** | 1. Chọn lọc 10 buổi học đại diện cho đủ 5 kiểu tình huống vận hành (đã xác nhận khớp, lệch trạng thái `dk`/`chờ xác nhận`, đổi phòng sau khi đã báo, đổi giờ/chuyển online, trùng phòng/trùng coach).<br>2. Trích mã ô gốc (`K9-GD1/F18`, `K9-GD1/F27`...), lịch sử chỉnh sửa (`EDIT-...`) và bảng ánh xạ tên gõ lệch (`staff_aliases`: `Labcoach AY`, `Lab Coach  J`, `Lecturer C.`, `GV E`, `Support  D`). |
| **Số dòng / số đoạn** | 10 bản ghi buổi học (`sessions`), 6 cặp ánh xạ tên nhân sự (`staff_aliases`), 9 bản ghi lịch sử chỉnh sửa (`edit_history`). |
| **Phiên bản / ngày lấy** | v1.0 · Trích xuất ngày 27/11/2026 từ bản giả lập Khoá 9 (15/04–08/05/2027). |
| **Nhãn** | `synthetic` (dữ liệu vận hành giả lập từ bộ đề BTC — **không dùng làm bằng chứng pain**). |
| **Giới hạn** | Chỉ bao phủ các buổi tiêu biểu của đợt 22/04–08/05/2027 của lớp L3A, L3B, L2A, L2B; chưa chứa toàn bộ 111 buổi của cả giai đoạn 1. |

## Dataset 2 · `data/schedule_data.json` ( phần `groups` — Danh sách nhóm học viên theo lớp)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn cho công cụ `get_schedule` và `check_conflicts` để chia nhóm học viên vào từng phòng lab và kiểm tra cảnh báo vượt sức chứa phòng (`capacity_warnings`). |
| **Từ đâu** | Nhóm tự dựng (`synthetic`) để bổ sung phần danh sách nhóm học viên không có sẵn trong hai file Excel của bộ đề. |
| **Xử lý những bước gì** | Khởi tạo cố định 6 nhóm cho lớp L3A (`L3A-N1`..`L3A-N6`, sĩ số 22–24 HV/nhóm, tổng 138 HV), 6 nhóm cho L3B (`L3B-N1`..`L3B-N6`, tổng 136 HV), cùng các cụm nhóm L2A, L2B. |
| **Số dòng / số đoạn** | 15 cụm/nhóm học viên thuộc 4 lớp (`L3A`, `L3B`, `L2A`, `L2B`). |
| **Phiên bản / ngày lấy** | v1.0 · Tạo ngày 27/11/2026. |
| **Nhãn** | `synthetic` |
| **Giới hạn** | Sĩ số từng nhóm là con số giả định đều nhau (~22–24 HV/nhóm), thực tế tại lớp có thể dao động theo tỷ lệ đi học từng buổi. |

**Data `synthetic` (nhóm tự sinh):** Sinh cố định theo quy tắc chia 6 nhóm/lớp L3 (mỗi phòng lab ghép 2 nhóm ~45–48 học viên để khớp với sức chứa phòng 40–50 chỗ trong sheet `Lịch lab 2604-0805`). Người kiểm: **Bùi Mạnh Linh** và **Nguyễn Mạnh Quyền** đã kiểm tay toàn bộ 15 dòng nhóm và 10 buổi học. Data tự dựng chỉ phục vụ chạy thử tool và benchmark, **không phải bằng chứng pain**.

## Dataset 3 · Câu hỏi & tình huống thực tế trong `eval/benchmark.csv`

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Làm đầu vào (`input`) cho các câu thử có nhãn nguồn `nguoi_dung` và `data_that` trong `eval/benchmark.csv` (7/20 câu = 35% ≥ 1/3 theo quy định R4). |
| **Từ đâu** | Ghi nhận từ lời kể tình huống thực tế khi phỏng vấn Trợ giảng / Key Coach L3A (`P1`, `P2`, `P3`) và mẫu câu hỏi đổi phòng/giờ thực tế trên kênh lớp L3A (đã ẩn danh và ánh xạ mã buổi sang lịch Khoá 9 để chạy qua tool). |
| **Xử lý những bước gì** | Xoá toàn bộ tên thật, SĐT, email cá nhân; giữ nguyên cấu trúc câu hỏi tự nhiên của học viên/trợ giảng và ánh xạ ngày/mã buổi sang không gian dữ liệu `schedule_data.json`. |
| **Số dòng / số đoạn** | 7 câu thử thực tế (`B01`, `B02`, `B03`, `B04`, `B12`, `B15`, `B17`) trên tổng số 20 câu thử trong `eval/benchmark.csv`. |
| **Phiên bản / ngày lấy** | v1.0 · Ngày 27/11/2026. |
| **Nhãn** | **thật** (cấu trúc câu hỏi & tình huống vận hành từ người dùng thật, đã ẩn danh). |
| **Giới hạn** | Mã ngày/phòng cụ thể trong câu hỏi được ánh xạ sang lịch Khoá 9 (`22/04`–`08/05/2027`) để khớp với kho dữ liệu giả lập của bản chạy thử. |
