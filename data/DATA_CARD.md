# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · `data/schedule_data.json` ( phần `sessions` & `staff_aliases` — Trích rút từ `data/training-ops/`)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn dữ liệu nền cho 2 công cụ `get_schedule` và `check_conflicts` trong `codebase/tools.py`; dùng để kiểm thử các ca đối chiếu lịch, bắt lệch giữa 2 bảng và lịch sử đổi phòng sát giờ. |
| **Từ đâu** | Trích rút và chuẩn hóa cấu trúc từ bộ dữ liệu giả lập BTC cấp (`data/training-ops/teaching-schedule.xlsx` — bản xuất `21:00 27/04/2027` và `data/training-ops/lab-coach-schedule.xlsx`). Không commit nguyên file `.xlsx` gốc của BTC. |
| **Xử lý những bước gì** | 1. Chọn các bản ghi đại diện cho tình huống vận hành (đã xác nhận, lệch trạng thái `dk`/`chờ xác nhận`, đổi phòng, đổi giờ/chuyển online, trùng phòng/trùng coach, nghỉ lễ, thiếu trên bảng chính).<br>2. Trích mã ô gốc (`K9-GD1/F18`, `K9-GD1/F27`...), lịch sử chỉnh sửa (`EDIT-...`) và bảng ánh xạ tên gõ lệch (`staff_aliases`: `Labcoach AY`, `Lab Coach  J`, `Lecturer C.`, `GV E`, `Support  D`). |
| **Số dòng / số đoạn** | 14 bản ghi lịch (`sessions`, gồm cả ngày nghỉ và buổi chưa có trên bảng chính), 6 cặp ánh xạ tên nhân sự (`staff_aliases`), 11 mục lịch sử chỉnh sửa (`edit_history`). |
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

**Data `synthetic` (nhóm tự sinh):** Sinh cố định theo quy tắc chia 6 nhóm/lớp L3 (mỗi phòng lab ghép 2 nhóm ~45–48 học viên để khớp với sức chứa phòng 40–50 chỗ trong sheet `Lịch lab 2604-0805`). Ghi nhận kiểm tay của **Bùi Mạnh Linh** và **Nguyễn Mạnh Quyền** bao gồm 15 dòng nhóm và 10 bản ghi buổi học. Data tự dựng phục vụ chạy thử công cụ và benchmark.

## Dataset 3 · Câu thử mang nhãn `nguoi_dung` hoặc `data_that` trong `eval/benchmark.csv`

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Làm đầu vào (`input`) để kiểm thử các tình huống đối chiếu lịch. |
| **Từ đâu** | Cột `source` ghi lời kể của trợ giảng hoặc tình huống từ kênh lớp và dữ liệu lịch. Cần đối chiếu từng nhãn với biên bản hoặc thông báo gốc đã ẩn danh, nhất là `B16`, hiện ghi nguồn là dữ liệu lịch. |
| **Xử lý những bước gì** | Ẩn danh thông tin cá nhân và ánh xạ ngày/mã buổi sang `schedule_data.json` để chạy thử. |
| **Số dòng / số đoạn** | 8/20 câu (40%) theo nhãn trong CSV. `nguoi_dung` gồm `B01`, `B02`, `B04`, `B12`. `data_that` gồm `B03`, `B05`, `B14`, `B16`. |
| **Phiên bản / ngày lấy** | v1.0 · Ngày 27/11/2026. |
| **Nhãn** | `nguoi_dung` (4) và `data_that` (4) theo CSV. Nguồn gốc của từng câu đang chờ đối chiếu. |
| **Giới hạn** | Mã ngày/phòng cụ thể trong câu hỏi được ánh xạ sang lịch Khoá 9 (`22/04`–`08/05/2027`) để khớp với kho dữ liệu giả lập của bản chạy thử. |
