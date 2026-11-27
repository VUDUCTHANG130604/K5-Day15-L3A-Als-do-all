"""Đếm kết quả khảo sát lịch / phòng — chạy lại: python evidence/survey/count.py
Đầu vào: evidence/survey/results.csv (export Google Form, không có tên / email / SĐT).
Câu nhiều lựa chọn: mỗi người tính 1 lần cho mỗi lựa chọn đã tick. Mẫu số ghi rõ ở từng dòng.
"""
import csv
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

rows = list(csv.reader(open(os.path.join(HERE, "results.csv"), encoding="utf-8-sig")))
head, data = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
col = {h.split(".")[0].strip(): i for i, h in enumerate(head)}   # "1", "O1", ..., "C8"


def g(r, k):
    return r[col[k]].strip()


def multi(r, k):
    return [x.strip() for x in g(r, k).split(",") if x.strip()]


def pct(x, n):
    return "%d/%d (%.0f%%)" % (x, n, 100.0 * x / n) if n else "0/0"


N = len(data)
print("Tổng số câu trả lời: %d" % N)
print("Vai trò:", dict(Counter(g(r, "1") for r in data)))
print("Lớp:", dict(Counter(g(r, "C7") for r in data)))
print("Nhận form qua:", dict(Counter(g(r, "C8") for r in data)))

print("\n== C1. Số buổi phòng đổi / chỉ chốt trong 24h trước giờ học (4 tuần qua), N=%d" % N)
c1 = Counter(g(r, "C1") for r in data)
for k, v in c1.most_common():
    print("  %-8s %s" % (k, pct(v, N)))
print("  ≥1 buổi:", pct(sum(v for k, v in c1.items() if k != "0"), N))

print("\n== C3. Lần gần nhất, từ lúc cần biết phòng đến lúc chắc chắn, N=%d" % N)
c3 = Counter(g(r, "C3") for r in data)
for k, v in c3.most_common():
    print("  %-14s %s" % (k, pct(v, N)))
print("  ≥15 phút:", pct(c3["15–30 phút"] + c3["Hơn 30 phút"], N))

print("\n== C4. Tình huống gặp trong 4 tuần qua (nhiều lựa chọn), N=%d" % N)
c4 = Counter(x for r in data for x in set(multi(r, "C4")))
for k, v in c4.most_common():
    print("  %-50s %s" % (k, pct(v, N)))
gap = [r for r in data if [x for x in multi(r, "C4") if x != "Không gặp"]]
print("  Gặp ≥1 tình huống (bỏ người chỉ chọn 'Không gặp'):", pct(len(gap), N))
mau = [r for r in data if any(x != "Không gặp" for x in multi(r, "C4")) and "Không gặp" in multi(r, "C4")]
print("  Câu trả lời mâu thuẫn (vừa chọn tình huống vừa chọn 'Không gặp'):", len(mau))

print("\n== C6. Hậu quả từng gặp (nhiều lựa chọn), N=%d" % N)
c6 = Counter(x for r in data for x in set(multi(r, "C6")))
for k, v in c6.most_common():
    print("  %-40s %s" % (k, pct(v, N)))
hq = [r for r in data if any(x in ("Đến muộn", "Lỡ một phần buổi", "Ảnh hưởng điểm danh hoặc điểm", "Phải nhờ người khác xử lý")
                             for x in multi(r, "C6"))]
print("  Có ≥1 hậu quả cụ thể (đến muộn / lỡ buổi / ảnh hưởng điểm danh / phải nhờ người khác):", pct(len(hq), N))

print("\n== C2. Biết phòng cuối cùng qua đâu (nhiều lựa chọn), N=%d" % N)
c2 = Counter(x for r in data for x in set(multi(r, "C2")))
for k, v in c2.most_common():
    print("  %-25s %s" % (k, pct(v, N)))
nhieu = [r for r in data if len(multi(r, "C2")) >= 2]
print("  Dùng ≥2 nguồn để biết phòng:", pct(len(nhieu), N))

print("\n== L1. Lần gần nhất không chắc phòng đã làm gì (nhiều lựa chọn), N=%d" % N)
l1 = Counter(x for r in data for x in set(multi(r, "L1")))
for k, v in l1.most_common():
    print("  %-30s %s" % (k, pct(v, N)))

print("\n== L2. Hai nguồn ghi khác nhau thì tin nguồn nào, N=%d" % N)
for k, v in Counter(g(r, "L2") for r in data).most_common():
    print("  %-25s %s" % (k, pct(v, N)))

coach = [r for r in data if g(r, "1") != "Học viên"]
print("\n== Nhánh người vận hành (O1–O6), n=%d — n nhỏ, không ghi %%" % len(coach))
for r in coach:
    print("  %s: O1=%s · O2=%s · O3=%s · O5=%s · O6=%s" % (g(r, "1"), g(r, "O1"), g(r, "O2"), g(r, "O3"), g(r, "O5"), g(r, "O6")))

print("\n== C5. Kể lần gần nhất (nguyên văn, không sửa chữ)")
for i, r in enumerate(data, 1):
    t = g(r, "C5")
    if t and t != "Không gặp":
        print("  R%02d (%s, %s): %s" % (i, g(r, "1"), g(r, "C7"), t))
