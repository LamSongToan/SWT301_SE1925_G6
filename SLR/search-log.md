# Search Log – Bug Report Quality Assessment with LLM

**Ngày thực hiện:** 2026-06-15

---

## Chuỗi tìm kiếm (Query Strings)

### String A
**Query nguyên văn:**

```
bug report completeness Cohen's kappa inter-rater Jira GitHub
```

**Database:** Google Scholar
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-15 23:30
**Số kết quả:** 79 papers

---

### String B
**Query nguyên văn:**

```text
("bug report" OR "defect report" OR "issue report") AND ("inter-rater agreement" OR "inter-rater reliability" OR "Cohen's Kappa" OR "human evaluation" OR "manual evaluation") AND ("automated" OR "LLM" OR "machine learning" OR "NLP")
```

**Database:** Google Scholar
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-15 23:50
**Số kết quả:** 74 papers

---

### String C
**Query nguyên văn:**

```text
"inter-rater" "bug report" GitHub Jira kappa
```

**Database:** Google Scholar
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-15 23:50
**Số kết quả:** 72 papers

---

### String D
**Query nguyên văn:**

```text
"Cohen's kappa" "bug report" GitHub Jira
```

**Database:** Google Scholar
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-16 00:10
**Số kết quả:** 7 papers

---

### String E
**Query nguyên văn:**

```text
"Cohen's kappa" "bug report" reproducibility
```

**Database:** Google Scholar
**Bộ lọc:** 2018-2026
**Ngày search:** 2026-06-15 23:50
**Số kết quả:** 17 papers

---

## Tổng hợp trước dedup

| Database               | String   | Kết quả |
| ---------------------- | -------- | ------- |
| Google Scholar         | String A | 79      |
| Google Scholar         | String B | 74      |
| Google Scholar         | String C | 72      |
| Google Scholar         | String D | 7       |
| Google Scholar         | String E | 17      |
| **Tổng trước dedup**   |          | 249     |
| **Sau dedup**          |          | 197     |
| Số bị loại (trùng lặp) |          | 52      |

---

## Phần S — Cross-reference Search (Snowballing)

> Snowballing không có query string — không điền vào mục này như các String A/B/C/D.

**Phương pháp:** Backward snowballing — đọc reference list của các paper đã pass V2 screening
**Thực hiện:** Sau khi có `03_final_included.csv`, đọc reference list của từng paper included
**Công cụ:** CrossRef (crossref.org) để lookup metadata từ DOI; Google Scholar để check full-text
**Ngày thực hiện:** 2026-06-02
**Paper included đã scan:** 1 papers
**Paper mới phát hiện:** 6 paper

> **Lưu ý:** Snowballing chỉ làm SAU khi hoàn thành tất cả database search. Paper tìm được qua snowballing được thêm vào `01_all_records.csv` và đi qua screening V1 → V2 bình thường.

---

## Ghi chú

- Thực hiện dedup bằng: Excel
- Snowballing: [số] paper mới tìm được, [số] pass V2