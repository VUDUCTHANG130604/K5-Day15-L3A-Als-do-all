## A5 · Vận hành đào tạo: lịch, phòng, phân công

**Hiện trạng.**
- **Khoá thiếu cơ sở vật chất, phòng học không cố định.** Lớp L3 hơn 700 học viên, chia L3A và L3B. Mỗi buổi giảng ghép hai phòng song song, thêm phòng phụ; mỗi buổi lab rải 3–6 phòng ở nhiều khu.
- **Nhiều phòng chỉ chốt sát ngày học**, có khi ngay trong ngày, và vẫn có thể đổi.
- **Phân công nằm ở nhiều bảng tính.** Ban đào tạo gom form đăng ký của giảng viên vào một bảng lịch chung, mỗi ô là chữ tự do. Đội lab coach giữ bảng riêng, đổi ca qua form và nhóm Zalo. Học viên nhận lịch qua email, tra nhóm trong một link danh sách.

**Định hướng ý tưởng.** Sắp xếp lịch và đưa lịch tới đúng người khi phòng chốt sát ngày và thông tin nằm ở nhiều nơi. Người dùng: ban đào tạo · key coach / Day Lead (chia coach theo phòng) · lab coach, giảng viên · học viên nhận lịch. Chạy thử trên [data/training-ops/](../data/training-ops/README.md) *(giả lập)*.

**Lát cắt gợi ý.** *Một key coach · tối trước buổi lab · AI đối chiếu phòng vừa xác nhận với lịch lab và danh sách nhóm, soạn thông báo phòng cho từng nhóm · key coach duyệt rồi gửi.*

**Tình huống khó.** Phòng chưa xác nhận · hai bảng ghi hai phòng khác nhau · phòng đổi sau khi đã báo · buổi chuyển sang online · tên người gõ lệch danh sách chuẩn.

**Công cụ gợi ý.** `get_schedule(date, class)` · `check_conflicts(plan) → chỗ trùng phòng, trùng người`: chạy bằng code, không phải AI · `draft_notice(class, changes)`: **không tự gửi**.