# GAP Analysis — Bug Report Quality Assessment with LLM

**RQ:** "Đối với bug reports trên GitHub/Jira (P), LLM đánh giá chất lượng báo cáo lỗi tự động theo tiêu chí reproducibility (I) so với developer manual review (C) có đạt Cohen's Kappa ≥0.70 không (O)?"

---

## Bước 1 — Kiểm tra evidence table

| Gate | Kết quả | Pass? |
|---|---|---|
| P1: Số paper ≥ 5 | 10 paper | ✅ |
| P2: Cột Tool/LLM ≥ 90% điền | 10/10 (100%) | ✅ |
| P3: Cột Kết quả ≥ 50% có số | 9/10 (90%) — chỉ #5 là N/A | ✅ |
| P4: Cột Hạn chế ≥ 50% điền | 10/10 (100%) | ✅ |
| P5: Cột Metric tên cụ thể | 10/10 đều có tên metric cụ thể (F1, BLEU, Pass@k, Reproduction rate, Spearman...) | ✅ |

---

# Bước 2 - Phân tích GAP
## Bước 2A — GAP-M

| Loại | Câu hỏi | Trả lời |
|---|---|---|
| GAP-M | Khía cạnh nào chưa đo? | No published paper measures inter-rater agreement (Cohen's Kappa) between LLM ratings and developer manual review on bug report 
reproducibility in GitHub/Jira contexts |

---

## Bước 2B — Kiểm tra phản chứng

### GAP-M: "Không paper nào dùng Cohen's Kappa để đo agreement giữa LLM-output và developer manual review"

| Paper | Vai trò LLM trong paper | Đã làm đúng như GAP mô tả không? | Ghi chú |
|---|---|---|---|
| #1 Multi-model framework, 2023 | BERT/RF/NB/SVM/LR/KNN/DT — classifier dự đoán 6 thuộc tính ISO 25010 | Không | κ=0.776 là agreement 2 người, không phải reproducibility, không có κ LLM-vs-developer. |
| #2 Issue Discussions OSS, 2024 | Không có LLM | Không | Không đo κ, không có LLM. |
| #3 Automated Analysis Bug Descriptions | DeMIBuD/Euler — heuristic detect missing EB/S2R | Không | Đo bằng Precision/Recall (85.9–93.2%), không phải κ; không phải LLM theo nghĩa hiện đại; domain là 9 hệ thống không xác định rõ GitHub/Jira. |
| #4 BugScribe (Android), 2026 | GPT-4/GPT-4o/Claude — **generator** sinh bug report | Không | κ=0.98 là giữa 2 annotator NGƯỜI đánh giá ground truth; domain Android, không phải GitHub/Jira; LLM không đóng vai evaluator. |
| #5 Root-Cause Subclassification, 2026 | Gemini/GPT-5.4/Opus — **Judge-LLM** cho root-cause/fix | Không | Judge-LLM success rate đo cho root-cause subclassification và fix generation, KHÔNG phải reproducibility; domain là GitHub (Brave) nhưng tiêu chí khác hẳn. |
| #6 Bug-AutoQ, 2021 MSR | Không có LLM | Không | κ=0.60 chỉ là baseline con người-vs-con người (xem 2A-bis) — không có LLM evaluator để so. |
| #7 CrowdTest, 2026 | Không có LLM | Không | α=0.609, p=0.092 đo reproducibility nhưng giữa người-với-người trên platform crowdsourced, không phải GitHub/Jira, không có LLM. |
| #8 Hallucinations LLM Summaries | Llama/Mistral/BERT-family — detect hallucination trong **summary** do LLM sinh | Không | κ=0.85 là ground-truth giữa người; phần LLM đo bằng F1/Macro-F1 (không phải κ) cho hallucination trong summary, không phải reproducibility của report gốc. |
| #9 Solution-Related Content | GPT-4/Llama-3 — classifier nội dung giải pháp | Không | κ=0.89 giữa 7 người; chủ đề không liên quan reproducibility. |
| #10 FeedAIde, 2026 | MLLM sinh follow-up question | Không | Domain là app feedback (không GitHub/Jira); κ=0.906 là agreement giữa 2 evaluator người, không phải MLLM-vs-developer. |
| #11 ImproBR, 2026 EASE | GPT-4o mini — **generator** cải thiện report | Không | κ=0.663–0.801 là baseline con người-vs-con người (xem 2A-bis); LLM ở đây sửa report, không đánh giá report. |
| #12 SLR, 2025 | Tổng hợp nhiều LLM qua các paper khác | Không | Đây là review, không phải thực nghiệm trực tiếp. |
| #13 Performance/Accuracy Bugs, 2022 | Không có LLM | Không | κ≥0.7 là baseline con người trên GitHub (xem 2A-bis), nhưng tiêu chí là bug type, không phải reproducibility; không có LLM. |

**Kết luận:** Không paper nào trong 13 paper dùng LLM làm **đánh giá chất lượng báo cáo lỗi tự động theo tiêu chí reproducibility** trên bug report GitHub/Jira rồi đo κ với developer manual review. Hai paper gần nhất về domain + criterion (#6 GitHub, #11 Jira) đều chỉ cung cấp baseline **con người-vs-con người**

---

### 2C. Đánh giá khả thi (Feasibility) trước khi chốt GAP

| Tiêu chí | Câu hỏi tự hỏi | Đánh giá | Căn cứ (ô cụ thể trong evidence table) |
|---|---|---|---|
| Dataset | Dataset có public, tải được ngay không? | ✅ An toàn | Paper #11 dùng "Mojira Minecraft bug tracker (24,998 bug reports, 139 manually evaluated)" — đúng là Jira instance, public, có sẵn subset đã đánh giá tay. Paper #6/#13 dùng GitHub issues public — cũng khớp domain P. |
| Tool/API | LLM/tool có free tier cho sinh viên không? | ⚠️ Cần xử lý | Paper #11 và #4 dùng GPT-4o mini — API trả phí nhưng chi phí thấp (per-token); cần ngân sách nhỏ (<$5 cho mẫu vài chục report) để chạy LLM-as-evaluator, chưa có free tier đủ lớn cho việc này. |
| Compute | Cần loại phần cứng gì để chạy? | ✅ An toàn | Tất cả paper liên quan (#4, #6, #11) chỉ chạy API/text-pipeline, không cần GPU training; tính Cohen's Kappa là phép tính CPU nhẹ (sklearn/statsmodels). |
| Ground truth | Cần tạo dữ liệu nhãn thủ công không? | ⚠️ Cần xử lý | Cần ≥2 người đóng vai "developer" đánh giá độc lập một mẫu bug report theo tiêu chí reproducibility để có κ Control. Quy mô tham khảo: paper #6 dùng "400 manually annotated, 2 annotators"; paper #11 dùng "139 manually evaluated, 2 annotators" — một mẫu nhỏ hơn (30–50 report) với 2–3 thành viên nhóm là khả thi trong vài giờ. |
| Skills | Nhóm có thể implement pipeline này không? | ✅ An toàn | Tính Cohen's Kappa là hàm thư viện chuẩn (`sklearn.metrics.cohen_kappa_score`); kỹ thuật LLM-as-judge đã được dùng phổ biến trong paper #4, #5 (Judge-LLM success rate) — không cần kỹ thuật research-level mới. |
| Thời gian | Experiment hoàn thành trong số tuần còn lại? | ❓ Không đánh giá được | Không có dữ liệu về deadline/số tuần còn lại của nhóm trong evidence-table.md hoặc RBL2 — theo quy tắc "không có nguồn → không hợp lệ", mục này cần nhóm tự xác nhận trực tiếp trước khi chốt GAP-M làm primary. |

**Tổng kết khả thi:** 4/6 tiêu chí ở mức ✅ An toàn, 2/6 ở mức ⚠️ Cần xử lý (ngân sách API nhỏ + vài giờ annotation tay), 1 tiêu chí (Thời gian) cần nhóm tự xác nhận. Không có ❌ Blocker nào được phát hiện dựa trên các nguồn trong evidence table → **GAP-M khả thi để triển khai thành thực nghiệm**, miễn nhóm xác nhận đủ thời gian.

---