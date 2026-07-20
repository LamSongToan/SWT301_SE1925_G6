# IE Criteria — Bug Report Quality Assessment with LLM

**RQ:** "Đối với bug reports trên GitHub/Jira (P), LLM đánh giá chất lượng báo cáo lỗi tự động theo tiêu chí reproducibility (I) so với developer manual review (C) có đạt Cohen's Kappa ≥0.70 không (O)?"
**PICO:** P=Đối với bug reports trên GitHub/Jira | I=LLM đánh giá chất lượng báo cáo lỗi tự động theo tiêu chí reproducibility | C=so với developer manual review | O=có đạt Cohen's Kappa ≥0.70 không

---

## Inclusion Criteria (IC) — paper PHẢI có đủ tất cả

| Mã | Tiêu chí |
|----|----------|
| **IC-L** | Viết bằng tiếng Anh |
| **IC-Y** | Xuất bản từ 2020 đến nay — Lý do: LLM thế hệ GPT-3+ được ứng dụng rộng rãi cho NLP tasks từ 2020 |
| **IC-T** | Đăng trên conference hoặc journal có peer-review — không phải blog, thesis, hay báo cáo kỹ thuật nội bộ không có phản biện |
| **IC-P** | Về task: Đánh giá chất lượng bug report dựa trên tiêu chí reproducibility / clarity / completeness / severity |
| **IC-I** | Dùng kỹ thuật: Dùng LLM (GPT, Claude, Llama, v.v.) hoặc deep learning model để tự động đánh giá/phân loại bug reports |
| **IC-E** | Có ít nhất 1 con số kết quả định lượng trong Table hoặc Figure của paper gốc |

## Exclusion Criteria (EC) — loại nếu BẤT KỲ điều kiện nào đúng

| Mã | Tiêu chí |
|----|----------|
| **EC-D** | Trùng lặp với paper đã có trong danh sách|
| **EC-A** | Không truy cập được full-text|
| **EC-S** | Dưới 4 trang (extended abstract, poster, short paper) |
| **EC-N** | Không có thực nghiệm (position paper, vision paper, tutorial) |
| **EC-O** | Không về topic: task không phải bug report quality assessment |