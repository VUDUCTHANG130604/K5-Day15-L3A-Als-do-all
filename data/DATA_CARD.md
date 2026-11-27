# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4. Chấm ở rubric R4. Không commit nguyên file data BTC: bản gốc để ở `data-btc/` (đã có trong `.gitignore`).
> **Mọi dữ liệu dưới đây là giả lập hoặc tự dựng — không phải bằng chứng pain.**

## Dataset 1 · Lịch Khoá 9 — `data/schedule_data.json` (phần `sessions`, `edit_history`, `staff_aliases`)

| | |
|---|---|
| Dùng để làm gì | Nguồn của 3 công cụ `get_schedule`, `check_conflicts`, `draft_notice` (`codebase/tools.py`) và đáp án (`expected`) của `eval/benchmark.csv` |
| Từ đâu | Bộ **giả lập** BTC cấp, `data/training-ops/` trong repo đề: `teaching-schedule.xlsx` (bản xuất **21:00 27/04/2027**) và `lab-coach-schedule.xlsx`. Người, email, ngày là giả; mã phòng và chủ đề giữ theo khoá thật (theo README của bộ data) |
| Xử lý những bước gì | Script `data/build_schedule.py` (chỉ thư viện chuẩn). Chạy lại: chép 2 file xlsx vào `data-btc/` rồi `python data/build_schedule.py`.<br>1. Sheet `Khoá 9 (GĐ1)`: tách mỗi ô chữ nhiều dòng → lớp, mã buổi, giờ, chủ đề, trạng thái phòng (`CONFIRMED` / `PENDING` / `ONLINE` / `UNCLEAR` / `NO_CLASS`), phòng chính thức, phòng dự kiến, phòng thêm, giảng viên. Hai ô LEC song song (cột D, E) gộp thành một buổi. Ô LEC không có dòng `Phòng:` → lấy phòng theo tiêu đề cột (H209 / H210), đúng quy ước trong README bộ data; nếu dòng giảng viên ghi phòng khác tiêu đề → gắn `UNCLEAR`, không đoán (ô E19).<br>2. Sheet `Lịch sử chỉnh sửa`: 44 dòng, phân loại `ROOM_CONFIRMED` / `ROOM_CHANGED_AFTER_CONFIRM` / `TIME_CHANGED` / `LECTURER_CHANGED` / `EXTRA_ROOM_CHANGED`, nối vào buổi theo địa chỉ ô.<br>3. Sheet `Lịch lab 1504-2404`, `Lịch lab 2604-0805`: gom các dòng coach theo (ngày, lớp, mã buổi) → phòng ghi ở bảng phụ (`dk:` / `chờ xác nhận` / phòng), key coach, danh sách lab coach. Đợt 1 không có cột phòng.<br>4. Sheet `Nhan_su`: bảng tên gõ lệch → tên khớp chuẩn.<br>Không ẩn danh thêm (bộ data đã dùng nhãn `Lecturer A`, `Lab Coach B`…). Không giữ email |
| Số dòng | 113 buổi (20 chờ xác nhận, 1 không rõ phòng, 2 đổi phòng sau khi xác nhận, 1 đổi giờ, 2 đổi giảng viên) · 44 lần sửa · 69 nhóm dòng bảng lab coach (1 dòng "Khai giảng toàn khoá" không nối với buổi nào) · 7 cặp tên gõ lệch |
| Mã trích dẫn | `[K9-GD1/<ô>]` = ô trong sheet `Khoá 9 (GĐ1)` · `[LSCS/<dòng>]` = dòng trong `Lịch sử chỉnh sửa` · `[LAB1/<dòng>]`, `[LAB2/<dòng>]` = dòng đầu nhóm trong sheet lịch lab đợt 1 / đợt 2. Mở xlsx là kiểm lại được |
| Phiên bản / ngày lấy | Sinh 27/11/2026 từ bộ đề phát ngày 27/11/2026 |
| Nhãn | `synthetic` (giả lập của BTC) |
| Giới hạn | Một ảnh chụp tại 21:00 27/04/2027 — không có thay đổi sau thời điểm đó. "Hôm nay" của bản chạy thử cố định là 27/04/2027. Không đọc màu nền, link, ô gộp ngoài các trường trên; không đọc sheet `Lịch lớp K9 (bản chép)`, `Đổi buổi (form)`, `Workload`. Cột "Sức chứa phòng" của bảng lab coach ghi một số cho cả buổi nhiều phòng, nghĩa không rõ → chỉ hiển thị, **không** dùng để kiểm vượt sức chứa. Trong toàn bộ data **không có** ca trùng phòng hay trùng coach giữa hai buổi chồng giờ (code vẫn kiểm) |

## Dataset 2 · Danh sách nhóm học viên — `data/schedule_data.json` (phần `groups`)

| | |
|---|---|
| Dùng để làm gì | Đề xuất chia nhóm vào phòng cho buổi LAB đã chốt (`check_conflicts` → `group_allocation`) |
| Từ đâu | **Nhóm tự dựng** — bộ đề không có danh sách nhóm |
| Cách sinh | `build_groups()` trong `data/build_schedule.py`, `random.Random(42)`: L3A, L3B mỗi lớp 12 nhóm; L2A, L2B mỗi lớp 6 nhóm; sĩ số mỗi nhóm 26–31. Quy mô lấy theo tiêu đề bảng phân công (L3 ~350 HV/lớp, L2 ~160 HV/lớp) |
| Số dòng | 36 nhóm |
| Nhãn | `synthetic` |
| Giới hạn | Số nhóm và sĩ số là giả định. Chia nhóm là đề xuất cơ học (khối liền nhau, đều theo số phòng), key coach phải chỉnh |

## Dataset 3 · Bộ câu thử — `eval/benchmark.csv`

| | |
|---|---|
| Từ đâu | Nhóm tự viết (`tu_viet`, 27 câu) và 1 câu dựa trên danh sách nhóm sinh có seed (`sinh_seed`). Mỗi `expected` trỏ về ô / dòng cụ thể trong xlsx (ghi ở cột `source`) |
| Số dòng | 28 câu: `thuong` 9 · `kho` 14 · `tu_choi` 5 |
| Giới hạn | **Chưa có câu nào từ lời người dùng thật hoặc data thật** (0/28; rubric R4 cần ≥ 1/3 ở CP3). Câu thêm từ khảo sát / kênh công khai sau này sẽ được **thêm** vào bộ, không sửa câu cũ |
