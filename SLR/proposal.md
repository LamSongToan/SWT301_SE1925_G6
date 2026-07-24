# Đề xuất Nghiên cứu: Đánh giá LLM-as-Evaluator cho Reproducibility của Bug Report

**Nhóm:** G6_SE1925

**Thành viên:** Lâm Song Toàn (SE200458), Nguyễn Thành Lộc (SE203692), Nguyễn Hồng Quân (SE203653), Tống Gia Huy (SE160995), Trần Thái Dương (SE193500)

**Mã đề tài:** RT-SWT-004

**Ngày nộp:** 2026-06-19

**Phiên bản:** 1.0

**Trạng thái:** Đang chờ phê duyệt

---

## 1. Thông tin Tổng quan

Nghiên cứu này khảo sát khả năng sử dụng mô hình ngôn ngữ lớn (LLM) như một bộ đánh giá tự động (*LLM-as-Evaluator*) để chấm điểm mức độ tái hiện được (*reproducibility*) của bug report — và đo lường mức độ đồng thuận giữa LLM với chú thích thủ công của developer thông qua hệ số Cohen's Kappa.

Dataset sử dụng là 139 bug report từ **Mojira Minecraft Issue Tracker**, vốn đã có sẵn hai chú thích độc lập của người dùng. Mô hình được chọn là **GPT-4o mini** (snapshot cố định `gpt-4o-mini-2024-07-18`) với nhiệt độ sinh văn bản bằng 0 để đảm bảo tính tái lập. Tiêu chí thành công là đạt Cohen's Kappa ≥ 0.70 giữa đánh giá của LLM và chú thích thủ công.

Nghiên cứu lấp đầy **GAP-M** (Metric Gap) — khoảng trống về phép đo agreement giữa LLM-evaluated reproducibility và developer judgment — mà chưa có paper nào trong 13 nghiên cứu được khảo sát giải quyết.

---

## 2. Phát biểu Vấn đề Nghiên cứu

### 2.1 Bối cảnh & Tầm quan trọng

Bug report là đầu vào cốt lõi trong quy trình phát triển phần mềm: chỉ khi developer có thể tái hiện (*reproduce*) được lỗi, họ mới có thể chẩn đoán và sửa chữa. Tuy nhiên, nghiên cứu từ ImproBR (Ramos et al. '26) cho thấy chưa đến 8% bug report trên Jira đạt tiêu chí đầy đủ để reproduce ngay lần đầu — chi phí xử lý thủ công từng report gây ra nút thắt cổ chai nghiêm trọng trong vòng đời phần mềm. Với quy mô hàng chục nghìn report trên các project lớn như TensorFlow hay Django, việc tự động hóa bước đánh giá reproducibility mang ý nghĩa thực tiễn rõ ràng cho cả nhà phát triển lẫn cộng đồng OSS.

### 2.2 Hiện trạng Nghiên cứu

BugScribe (Chen et al. '26) là công trình gần nhất sử dụng GPT-4o và Claude Opus để sinh tự động bug report từ ứng dụng Android, đạt F1 = 89.56 và κ = 0.98 giữa hai người chú thích — nhưng vai trò LLM ở đây là *generator*, không phải *evaluator*. ImproBR (Ramos et al. '26, EASE) dùng GPT-4o mini để cải thiện độ đầy đủ của bug report trên Jira (Minecraft), ghi nhận κ = 0.663–0.801 trong đánh giá baseline con người — gần domain nhất với nghiên cứu này, nhưng LLM chỉ đóng vai trò sửa report, không đánh giá reproducibility. Bug-AutoQ (Fazzini et al. '21, MSR) tự động gợi ý câu hỏi follow-up cho bug report thiếu thông tin trên GitHub (25.000 issues, κ = 0.60 baseline), xác lập floor cho inter-rater agreement trong domain. Automated Root-Cause Subclassification (Hu et al. '26) dùng Gemini và GPT làm Judge-LLM để phân loại và đề xuất fix cho invalid bug report — cho thấy LLM-as-Judge là hướng tiếp cận khả thi, nhưng tiêu chí đánh giá là root-cause, không phải reproducibility.

### 2.3 Khoảng trống Nghiên cứu (GAP)

Không có paper nào trong 13 nghiên cứu được khảo sát sử dụng LLM để đánh giá chất lượng bug report theo tiêu chí reproducibility trên GitHub/Jira, rồi đo mức độ đồng thuận với developer manual review bằng Cohen's Kappa. Các paper gần nhất về domain và tiêu chí chỉ cung cấp baseline κ giữa người và người — không có thành phần LLM-as-evaluator. Đây là **GAP-M** (Metric Gap): khoảng trống về phép đo agreement giữa LLM-evaluated reproducibility và developer judgment, được xác nhận qua phản chứng đầy đủ 13/13 paper.

### 2.4 Động lực Nghiên cứu

Nếu không giải quyết GAP này, các nhóm phát triển sẽ tiếp tục đầu tư nguồn lực con người đáng kể vào việc sàng lọc thủ công hàng nghìn bug report mỗi tháng, trong khi không có cơ sở thực nghiệm nào để biết LLM có thể đảm nhận bước này đáng tin cậy hay không. Xác lập được ngưỡng Cohen's Kappa giữa LLM và developer sẽ tạo ra tiền lệ đo lường có thể tái sử dụng cho bất kỳ dự án OSS nào muốn tích hợp LLM vào quy trình triage bug.

---

## 3. Các Nghiên cứu Liên quan

### 3.1 Tổng quan

| # | Paper | Công cụ/LLM | Dataset (quy mô) | Metric | Kết quả tốt nhất | Hạn chế chính |
|---|---|---|---|---|---|---|
| 1 | Multi-model framework (2023, ESE) | BERT, RF, NB, SVM, LR, KNN, DT | Jira/Bugzilla (5.400 report, 2 annotator) | Cohen's Kappa (κ), F1 | κ = 0.776; F1 = 0.98 | Giới hạn 6 OSS project; class mất cân bằng |
| 4 | BugScribe (2026, ACM) | GPT-4, GPT-4o, GPT-4o-mini, Claude Opus | Android apps (58 report, 2 annotator) | F1, κ, Krippendorff's α | F1 = 89.56; κ = 0.98 | LLM non-determinism; ground truth chủ quan |
| 5 | Root-Cause Subclassification (2026) | Gemini 3.1, GPT-5.4, Opus 4.6 | GitHub/Brave (1.404 report, 302 được chú thích) | Weighted F1, Judge-LLM success rate | F1 = 0.66; Judge success = 68.9% | Single repo; rủi ro data leakage |
| 6 | Bug-AutoQ (2021, MSR) | GloVe, LSTM, Deep NN | GitHub (25.000 issues, 400 được chú thích) | MRR, P@n, κ | MRR = 0.677; κ = 0.60 | Tập chú thích nhỏ; heuristic-based |
| 7 | CrowdTest (2026, JSCP) | N/A | Crowdsourced platform (54 người tham gia, 30 report) | Krippendorff's α, p-value | α = 0.609; p = 0.092 | Mẫu nhỏ; evaluator không chuyên |
| 8 | Hallucinations LLM Summaries (N/A) | Llama-3.2, Mistral-7B, BERT family | Mozilla Bugzilla (10.304 report, 3 annotator) | κ, Macro-F1 | κ = 0.85; Macro-F1 = 0.891 | Taxonomy chưa bao quát edge cases |
| 9 | Solution-Related Content (N/A) | GPT-4, Llama-3, BERT, RoBERTa | Mozilla/Chromium/GnuCash (376 issues, 7 annotator) | F1, κ | F1 = 0.737; κ = 0.89 | Phân tích comment độc lập mất context |
| 10 | FeedAIde (2026, MOBILESoft) | MLLM (Multimodal LLM) | App feedback (2 evaluator) | κ | κ = 0.906 (bug report) | Token consumption cao; rủi ro privacy |
| 11 | ImproBR (2026, EASE) | GPT-4o mini, DistilBERT | Mojira Minecraft (24.998 report, 139 được đánh giá) | κ, TF-IDF, Semantic similarity | κ = 0.663–0.801; Semantic = 77.7% | Single domain; phụ thuộc BEE tool |
| 13 | Performance/Accuracy Bugs (2022, EASE) | PyGithub | GitHub DL frameworks (664 sampled, toàn bộ tác giả) | κ | κ ≥ 0.70 (tất cả trường hợp) | Phân loại thủ công có thể có lỗi |

*10 paper liên quan nhất được liệt kê ở trên; xem đầy đủ 13 paper tại `evidence-table-merged.md`.*

### 3.2 Phân tích Mẫu

**Mẫu 1 — LLM chủ yếu đóng vai trò generator, không phải evaluator.** Các paper sử dụng LLM (GPT-4o, Claude, Gemini) hầu hết để *tạo ra* hoặc *cải thiện* bug report thay vì đánh giá chất lượng của chúng — thể hiện qua BugScribe (#4), ImproBR (#11), và FeedAIde (#10). Khoảng trống LLM-as-evaluator vẫn chưa được lấp đầy.

**Mẫu 2 — Cohen's Kappa được dùng phổ biến nhưng không gắn với LLM.** Các paper sử dụng κ (#1, #4, #6, #8, #9, #10, #11, #13) đều đo agreement giữa người và người như một bước xác nhận ground truth, không phải giữa LLM-output và developer judgment — chính xác là khoảng trống GAP-M của nghiên cứu này.

**Mẫu 3 — Baseline κ trên GitHub/Jira hội tụ quanh 0.60–0.80.** Paper #6 (GitHub, κ = 0.60), Paper #11 (Jira, κ = 0.663–0.801), Paper #13 (GitHub, κ ≥ 0.70) cung cấp dải tham chiếu thực nghiệm vững chắc, là căn cứ trực tiếp để đặt ngưỡng κ ≥ 0.70 trong RQ1.

**Mẫu 4 — Domain đơn lẻ là hạn chế phổ biến.** Hầu hết paper (#5, #7, #11) chỉ dùng một repository hoặc một nền tảng, hạn chế external validity — đây là lý do nghiên cứu này sử dụng dataset Mojira đại diện cho nhiều loại bug kỹ thuật khác nhau.

### 3.3 Ánh xạ Khoảng trống

| Khoảng trống | Loại | Bằng chứng | Trạng thái |
|---|---|---|---|
| Không paper nào đo κ giữa LLM-evaluated reproducibility và developer manual review | GAP-M | 13/13 paper không thực hiện — xem bảng phản chứng `gap-analysis.md` Bước 2B | Đã xác nhận |
| Thiếu dataset gán nhãn theo tiêu chí reproducibility có sẵn cho GitHub (không phải Android/Minecraft) | GAP-D | 0/13 paper cung cấp dataset GitHub gán nhãn theo reproducibility rubric | Chưa đánh giá |
| Thiếu rubric chuẩn hóa 5 điểm cho reproducibility của GitHub issues | GAP-T | Chỉ CrowdTest (#7) và ImproBR (#11) dùng rubric ordinal, nhưng trên domain crowdsourced/Jira | Đã xác nhận – Hoãn xử lý |

---

## 4. Câu hỏi Nghiên cứu

### Câu hỏi chính (RQ)

Đối với các bug report trên **Mojira Minecraft Issue Tracker** (P), khi LLM được sử dụng như một bộ đánh giá tự động để chấm mức độ reproducibility của bug report (I), so với đánh giá thủ công của developer đã có sẵn trong dataset (C), liệu mức độ đồng thuận giữa hai phương pháp có đạt mức đáng kể (**Cohen's Kappa ≥ 0.70**) (O) hay không?

### Câu hỏi phụ (SQ)

**SQ1 — Mức độ đồng thuận tổng thể**
Mức độ đồng thuận giữa đánh giá reproducibility của LLM và chú thích thủ công của người trên tập Mojira là bao nhiêu, đo bằng Cohen's Kappa?

**SQ2 — Mức độ đồng thuận theo từng chiều**
Mức độ đồng thuận giữa LLM và người thay đổi như thế nào qua các chiều reproducibility khác nhau (Steps to Reproduce, Observed Behavior, Expected Behavior)?

**SQ3 — Phân tích bất đồng**
Những đặc điểm nào của bug report dẫn đến sự bất đồng có hệ thống giữa đánh giá của LLM và chú thích thủ công?

---

## 5. Giao thức Thực nghiệm

### 5.1 Tổng quan Pipeline

Nghiên cứu đánh giá mức độ mà một bộ đánh giá reproducibility dựa trên LLM có thể đồng thuận với chú thích thủ công sẵn có trong dataset Mojira Minecraft Issue Tracker. Mục tiêu là đo lường agreement giữa đánh giá tự động và đánh giá thủ công về reproducibility của bug report, với ngưỡng benchmark là Cohen's κ ≥ 0.70.

Thực nghiệm gồm hai giai đoạn: **Giai đoạn 0 — Kiểm tra thử** (pilot validation, dùng để hiệu chỉnh hệ thống) và **Giai đoạn 1 — Đánh giá đầy đủ** trên toàn bộ 139 report của dataset Mojira.

---

#### Giai đoạn 0 — Kiểm tra thử (Hiệu chỉnh hệ thống)


Giai đoạn này đảm bảo thiết lập LLM hoạt động ổn định và scoring logic được áp dụng nhất quán trước khi chạy thực nghiệm chính thức.
 
- Lấy mẫu một tập con **10–15 bug report Mojira từ dataset ImproBR, không trùng với tập 139 report dùng trong đánh giá chính**.
- Mỗi report đã có sẵn hai chú thích độc lập (từ dataset gốc) và các nhãn chú thích có cấu trúc.
- Tính Cohen's Kappa giữa hai người chú thích trên tập pilot bằng cách áp dụng **scoring function chuẩn** → xác nhận κ_pilot_human.
  - Nếu **κ_pilot_human < 0.60**: chú thích trong tập pilot không đủ nhất quán → cân nhắc loại trừ tập pilot từ dataset gốc hoặc rà soát lại cách tổng hợp nhãn. **Chỉ tiếp tục nếu κ_pilot_human ≥ 0.60**.
- LLM (GPT-4o mini) đánh giá độc lập cùng tập pilot, áp dụng zero-shot prompt (mặc định), và ghi lại output dạng JSON.
- Tính **κ_pilot_LLM** giữa output của LLM (sau scoring function) và điểm tổng hợp của người trên tập pilot.
- Áp dụng cơ chế cổng kiểm soát (*gating*):
  - Nếu **κ_pilot_LLM < 0.50**: prompt zero-shot chưa phù hợp → chuyển từ zero-shot sang few-shot (k=3) cho toàn bộ 139 report đánh giá chính.
  - Nếu **κ_pilot_LLM ≥ 0.50**: tiếp tục toàn bộ 139 report với zero-shot.
- Chỉ tiến hành Giai đoạn 1 khi điều kiện gating được thỏa mãn.

---

#### Giai đoạn 1 — Đánh giá đầy đủ (139 bug report Mojira)

Thực nghiệm chính được thực hiện trên toàn bộ 139 bug report Mojira đã được tuyển chọn.

Dataset bao gồm các trường cấu trúc sau cho mỗi report:

- **Nội dung thô:** summary, description, status, versions, components, labels
- **Các phần trích xuất có cấu trúc:** Steps to Reproduce, Observed Behavior, Expected Behavior, Environment (nếu có)
- **Chú thích:** hai chú thích độc lập (Author 1 và Author 2) từ dataset gốc

Quy trình xử lý:

1. Tổng hợp hai chú thích của người thành một điểm tham chiếu duy nhất (trung bình hoặc majority vote, áp dụng nhất quán cho toàn bộ 139 report).
2. LLM (GPT-4o mini, temperature = 0, structured JSON output) đánh giá độc lập từng report và gán điểm reproducibility (1–5) theo cùng rubric.
3. Tính **κ_control** (agreement giữa hai người chú thích) để đặt giới hạn trên về độ tin cậy của ground truth.
4. Tính **κ_LLM** giữa output LLM và điểm tổng hợp của người — đây là kết quả chính của nghiên cứu.

---

#### Đánh giá Câu hỏi Nghiên cứu

**RQ1 / SQ1 — Mức độ đồng thuận tổng thể**

Phép đo chính là Cohen's Kappa (κ) giữa dự đoán của LLM và điểm tổng hợp của người, kèm bootstrap 95% confidence interval để ước lượng độ bền của kết quả.

**SQ2 — Mức độ đồng thuận theo từng chiều**

Reproducibility được phân tách thành ba chiều theo cấu trúc của report Mojira: Steps to Reproduce, Observed Behavior, Expected Behavior. Agreement được tính riêng cho từng chiều.

**SQ3 — Phân tích bất đồng**

Các trường hợp bất đồng giữa LLM và người được phân tích theo các đặc điểm lặp lại:
- Steps to Reproduce bị thiếu, không đầy đủ, hoặc mơ hồ
- Kỳ vọng ngầm định vs. kỳ vọng tường minh trong mô tả lỗi
- Thông tin môi trường/phiên bản không rõ ràng hoặc mâu thuẫn
- Mô tả không có cấu trúc hoặc không phân đoạn rõ ràng

---

#### Phân tích Thống kê

- **Wilcoxon signed-rank test** (hai phía, α = 0.05) để phát hiện sai lệch có hệ thống giữa phân phối điểm của LLM và của người.
- **Nhị phân hóa điểm** để kiểm tra bổ sung (sanity check):
  - Điểm ≥ 4 → Reproducible
  - Tính: Accuracy, Precision, Recall

---

### 5.2 Dataset

Dataset gồm 139 bug report từ Mojira Minecraft Issue Tracker được sử dụng để đánh giá reproducibility. **Mỗi report đã có sẵn hai chú thích độc lập từ dataset gốc (ImproBR, Ramos et al. 2026).**
 
| Dataset | Tracker | Phạm vi | Nguồn chú thích |
|---|---|---|---|
| Mojira Minecraft Issue Tracker | Mojang Jira / Mojira | 139 bug report | ImproBR paper (2 human annotators mỗi issue) |
 
#### Đặc điểm Dữ liệu
 
Mỗi bug report bao gồm:
 
**Trường thô:** Issue key (ví dụ: MC-xxxxx), Summary, Description, Metadata (status, versions, components, labels)
 
**Trường chú thích có cấu trúc:** Hai chú thích độc lập (từ ImproBR dataset) với các nhãn:
- S2R Label (Steps to Reproduce category)
- S2R Irrep Category (irreproducibility type, if applicable)
- OB Category (Observed Behavior presence)
- OB Label (Observed Behavior quality/sufficiency)
- EB Category (Expected Behavior presence)
- EB Label (Expected Behavior quality/accuracy)
#### Tiêu chí Đưa vào
 
- Được gán nhãn là bug-related trong Mojira
- Có đủ nội dung văn bản (≥ 50 từ trong description)
- Có trạng thái giải quyết hợp lệ (loại trừ: wontfix, duplicate, invalid)
- Được tạo trước năm 2024
- Có thông tin reproduction có thể sử dụng (dạng có cấu trúc hoặc bán cấu trúc)
- **Có hai chú thích độc lập sẵn có từ dataset ImproBR**
#### Chiến lược Lấy mẫu
 
Dataset được xác định trước và cố định ở N = 139 report từ ImproBR paper. Không thực hiện lấy mẫu bổ sung hoặc chú thích mới.
 
**Lưu ý quan trọng:**
- Mỗi report **đã được chú thích sẵn bởi hai người** trong bài báo gốc — chúng tôi **không thu thập chú thích mới** trong nghiên cứu này.
- Chú thích này được coi là **ground truth cố định** và không bị sửa đổi hay xác nhận lại.
- Random seed cố định (`random_state = 42`) được dùng nếu cần chia tập con trong nội bộ để đảm bảo tính tái lập.

---

### 5.3 Cấu hình LLM / Công cụ

**Mô hình:** GPT-4o mini — `gpt-4o-mini-2024-07-18`
*(snapshot ID cố định — bắt buộc để đảm bảo tính tái lập; tránh cập nhật mô hình ngầm giữa các lần chạy; xem §7.1)*

**Siêu tham số:**
- temperature = 0 (sinh văn bản xác định)
- top_p = 1 (giữ mặc định vì temperature = 0 đã đảm bảo tính xác định)
- max_tokens = 300 (đủ cho JSON output có cấu trúc `{score, reasoning}` với lý giải ngắn gọn)

---

#### Biểu diễn Đầu vào

Mỗi bug report được cung cấp cho mô hình dưới dạng chuỗi văn bản có cấu trúc, bao gồm:

- Metadata thô (summary, description, status, versions, components, labels)
- Các phần có cấu trúc đã trích xuất: Steps to Reproduce, Observed Behavior, Expected Behavior, Environment (nếu có)

---

#### Chiến lược Prompting

**Zero-shot prompting** được dùng mặc định cho toàn bộ 139 report.
 
**Fallback strategy:** Nếu κ_pilot_LLM (§5.1) dưới 0.50, hệ thống chuyển sang **few-shot k=3** cho toàn bộ 139 report đánh giá chính:
 
- k=3 gồm ba ví dụ: một cho mỗi mức điểm tiêu biểu (score = 1, 3, và 5)
- Các ví dụ được **lựa chọn thủ công từ bài báo ImproBR hoặc công khai từ Mojira**, **ngoài cả tập pilot lẫn tập 139 report đánh giá chính** để tránh data leakage
- **Lưu ý:** Chiến lược này là phương sách dự phòng dựa trên giả định rằng few-shot có thể cải thiện alignment. Tuy nhiên, không có bằng chứng thực nghiệm nào trước đó cho thấy few-shot tốt hơn zero-shot trên task reproducibility assessment — đây là một quyết định heuristic của nhóm.
- Các phiên bản prompt được khóa cứng trong suốt thực nghiệm để tránh HARKing (Hypothesizing After Results are Known)
**Template Prompt — Zero-shot (Mặc định)**
 
```
You are a software engineer evaluating bug report reproducibility.
Your task is to assign a score from 1 to 5:
 
1 = Not reproducible (missing reproduction steps and context)
2 = Weak reproducibility (partial description, major missing details)
3 = Partially reproducible (some steps exist but incomplete)
4 = Mostly reproducible (minor missing details)
5 = Fully reproducible (clear steps, environment, expected/actual behavior)
 
Now evaluate:
 
"""
{issue_text}
"""
 
Return JSON: {"score": <1-5>, "reasoning": "<1-2 sentences>"}
```
 
**Template Prompt — Few-shot (Fallback, k=3)**
 
```
You are a software engineer evaluating bug report reproducibility.
Your task is to assign a score from 1 to 5:
 
1 = Not reproducible (missing reproduction steps and context)
2 = Weak reproducibility (partial description, major missing details)
3 = Partially reproducible (some steps exist but incomplete)
4 = Mostly reproducible (minor missing details)
5 = Fully reproducible (clear steps, environment, expected/actual behavior)
 
Examples:
 
Example 1 (score=1):
"""
{few_shot_example_low}
"""
→ {"score": 1, "reasoning": "Missing reproduction steps and environment information."}
 
Example 2 (score=3):
"""
{few_shot_example_mid}
"""
→ {"score": 3, "reasoning": "Partial steps provided but key details such as environment or version are missing."}
 
Example 3 (score=5):
"""
{few_shot_example_high}
"""
→ {"score": 5, "reasoning": "Complete reproduction steps with environment and expected/actual behavior clearly specified."}
 
Now evaluate:
 
"""
{issue_text}
"""
 
Return JSON: {"score": <1-5>, "reasoning": "<1-2 sentences>"}
```
---

#### Tài liệu tham chiếu Tiêu chí Chất lượng

Chú thích của người tuân theo rubric được định nghĩa tại:

> `RQ1/manual_evaluation/evaluation_metrics.yaml`

File này định nghĩa hướng dẫn đánh giá chính thức mà người chú thích sử dụng. LLM xấp xỉ các tiêu chí này thông qua prompt có cấu trúc và đầu vào phân đoạn theo từng section.

---

#### **Hàm Scoring Xác định (Deterministic Scoring Function)**
 
Ground truth scores (1–5) được tạo từ chú thích người bằng cách áp dụng một hàm scoring **xác định** (deterministic function) trên các nhãn chú thích có cấu trúc. Cùng hàm này được áp dụng trên output của LLM để đảm bảo so sánh công bằng.
 
**Hàm scoring:**
 
```python
def score_row(s2r, irr, ob, obl, eb, ebl):
    """
    Chuyển đổi nhãn chú thích → điểm reproducibility 1–5
    
    Inputs:
      s2r (str): S2R Label ("executable" hoặc phạm trù khác)
      irr (str): S2R Irrep Category (nếu s2r không "executable")
      ob (str): OB Category ("present" / "absent" / etc)
      obl (str): OB Label ("sufficient" / "insufficient" / etc)
      eb (str): EB Category ("present" / "absent" / etc)
      ebl (str): EB Label ("accurate" / "inaccurate" / etc)
    
    Output: score ∈ {1, 2, 3, 4, 5}
    """
    s2r = str(s2r).strip().lower()
    irr = str(irr).strip().lower()
    ob = str(ob).strip().lower()
    obl = str(obl).strip().lower()
    eb = str(eb).strip().lower()
    ebl = str(ebl).strip().lower()
 
    # Mức 5: Steps executable + OB đầy đủ + EB chính xác
    if s2r == 'executable':
        if ob == 'present' and obl == 'sufficient' and eb == 'present' and ebl == 'accurate':
            return 5
        return 4  # Executable nhưng OB/EB không đầy đủ → 4
 
    # Mức 1: Thông tin sai hoặc bị mất
    if irr == 'wrong information':
        return 1
 
    # Mức 3: Cả OB và EB có, nhưng có thể không đầy đủ
    if ob == 'present' and eb == 'present':
        return 3
 
    # Mức 2: Chỉ OB hoặc EB có
    if ob == 'present' or eb == 'present':
        return 2
 
    # Mặc định: Không có thông tin reproduction
    return 1
```
 
**Ứng dụng:**
- Hàm này được áp dụng trên các nhãn chú thích của người (từ dataset ImproBR) → ground truth scores
- Hàm **tương tự** được áp dụng trên output được trích xuất từ LLM (s2r_label, s2r_failure_type, observed_behavior_presence, observed_behavior_quality, expected_behavior_presence, expected_behavior_quality) → LLM scores
- Cả hai scores sau đó được so sánh bằng Cohen's κ
**Lợi ích:** Đảm bảo rằng sự khác biệt giữa người và LLM không phải do lựa chọn hàm scoring, mà thực sự do LLM diễn giải nội dung report khác với người.
---

#### Căn cứ Thiết kế

Cấu hình này được thiết kế để đảm bảo:
- **Tính tái lập:** snapshot mô hình cố định và giải mã xác định
- **Tính so sánh được:** cùng rubric chấm điểm cho cả người và LLM
- **Tính ổn định:** fallback từ zero-shot sang few-shot chỉ theo điều kiện pilot đã định trước
- **Output ít biến động:** JSON có cấu trúc giảm thiểu mơ hồ trong quá trình phân tích

---

### 5.4 Đo lường

| Metric | Công cụ + phiên bản | Nguồn ground truth | Thiết lập agreement |
|---|---|---|---|
| Cohen's Kappa (κ) | Python `scikit-learn` (phiên bản ghi nhận tại runtime qua `pip show scikit-learn` trong quá trình thiết lập môi trường) | Chú thích người từ dataset Mojira (2 annotators độc lập từ ImproBR paper, không thu thập lại trong nghiên cứu này) | κ_control được tham chiếu từ bài báo gốc (ImproBR: κ = 0.663–0.801) để xác nhận độ tin cậy của ground truth |
 
**Lưu ý:**
- Ground truth được lấy **trực tiếp từ chú thích có sẵn trong dataset ImproBR**; không thu thập thêm nhãn mới trong nghiên cứu này.
- Hai chú thích độc lập mỗi report được tổng hợp bằng cách áp dụng **cùng một scoring function xác định** (xem §5.3) để chuyển đổi nhãn thể loại → điểm ordinal 1–5, tạo ra ground truth score duy nhất.
- Cohen's Kappa là metric agreement chính cho phép đo chính: agreement người–LLM (đánh giá tại §6).
- Toàn bộ tính toán metric được thực hiện trên tập đánh giá đầy đủ 139 report.

---

### 5.5 Baseline

Nghiên cứu này được đặt vấn đề như một **bài toán đánh giá khả năng (capability assessment)** — mục tiêu là xác định liệu LLM có thể đảm nhận vai trò bộ đánh giá reproducibility một cách đáng tin cậy hay không.
 
Thay vì so sánh với một hệ thống ML baseline cạnh tranh (ví dụ: classifier rule-based), chúng tôi sử dụng:
- **Agreement giữa người và người (κ_control = 0.663–0.801)** làm giới hạn trên về độ nhất quán của chú thích người
- **Cohen's Kappa ≥ 0.70** làm tiêu chí thành công để chỉ ra LLM đạt *substantial agreement* với chú thích người
**Ngưỡng κ ≥ 0.70** được lựa chọn dựa trên:
1. Phạm vi κ_control từ paper #11 (ImproBR): 0.663–0.801
2. Tiêu chuẩn chung trong tài liệu (Landis & Koch, 1977): κ ≥ 0.70 = "substantial agreement"
3. Các paper liên quan (#13, #6) cũng đặt ngưỡng ở 0.60–0.70
Đánh giá do đó tập trung vào **khả năng tuyệt đối của LLM** (absolute capability) thay vì hiệu suất tương đối so với mô hình khác (relative performance).
---

## 6. Kế hoạch Đánh giá

Kế hoạch đánh giá xem xét mức độ mà bộ chấm điểm reproducibility dựa trên LLM đồng thuận với chú thích người trên tập bug report Mojira Minecraft, tập trung vào cả agreement tổng thể lẫn đặc trưng của các trường hợp lỗi.

---

### 6.1 Agreement Tổng thể (RQ1 / SQ1)

Phép đo chính đánh giá mức độ đồng thuận giữa dự đoán của LLM và chú thích tổng hợp của người.

- **Metric:** Cohen's Kappa (κ)
- **Đầu vào:** điểm reproducibility của LLM (1–5) và điểm tổng hợp của người (từ hai annotator trong dataset)
- **Hỗ trợ thống kê:** bootstrap 95% confidence interval cho κ
- **Tiêu chí thành công:** κ ≥ 0.70 biểu thị agreement đáng kể (*substantial agreement*)

Phép đo này trực tiếp trả lời câu hỏi liệu LLM có thể xấp xỉ đánh giá reproducibility ở mức người trên tập bug report Mojira hay không.

---

### 6.2 Đánh giá theo Từng Chiều (SQ2)


Để hiểu các phần nào của bug report đóng góp nhiều nhất vào agreement tổng thể, reproducibility được phân tách thành ba chiều có cấu trúc:
 
- **Steps to Reproduce (S2R)**
- **Observed Behavior (OB)**
- **Expected Behavior (EB)**
#### Phương pháp Tính κ theo Chiều
 
Thay vì tính κ trực tiếp trên điểm tổng hợp 1–5, chúng tôi tạo điểm phụ cho mỗi chiều bằng cách **rescoring** chỉ trên các trường liên quan:
 
**S2R Score (1–3):**
- 3 = "executable" (cần thiết để tái hiện)
- 2 = "executable" nhưng có thêm thông tin sai → downgrade
- 1 = irreproducible hoặc missing steps
**OB Score (1–3):**
- 3 = "present" + "sufficient"
- 2 = "present" nhưng "insufficient"
- 1 = "absent"
**EB Score (1–3):**
- 3 = "present" + "accurate"
- 2 = "present" nhưng "inaccurate"
- 1 = "absent"
Với mỗi chiều:
- Áp dụng hàm rescoring chuẩn trên cả human annotations và LLM outputs
- Tính Cohen's Kappa riêng cho S2R, OB, EB
- So sánh κ_S2R, κ_OB, κ_EB để xác định chiều nào LLM dự đoán tốt nhất
**Giải thích:** Phương pháp này cho phép chúng tôi xác định nếu LLM có khó khăn với một chiều cụ thể (ví dụ: EB luôn bị đánh giá thấp) hay là vấn đề tổng quát.
 

---

### 6.3 Phân tích Bất đồng (SQ3)

Để điều tra sự khác biệt có hệ thống giữa đánh giá LLM và người, các trường hợp bất đồng được phân tích trên toàn bộ 139 bug report Mojira, kết hợp phân tích định lượng và định tính.

**Phân tích định lượng:**
- Phân phối chênh lệch điểm (LLM so với người)
- Tần suất bất đồng theo từng mức điểm (1–5)
- Tỷ lệ bất đồng theo từng chiều

**Phân tích định tính:**
- Steps to Reproduce bị thiếu hoặc không đầy đủ
- Kỳ vọng ngầm định vs. tường minh trong mô tả lỗi
- Thông tin môi trường/phiên bản không nhất quán hoặc không rõ ràng
- Mô tả không có cấu trúc hoặc không phân đoạn rõ ràng

Bước này nhằm đặc trưng hóa các mẫu lỗi lặp lại của LLM trong đánh giá reproducibility.

---

### 6.4 Giới hạn Tham chiếu của Agreement Người (κ_control)

Để đặt kết quả LLM vào ngữ cảnh, agreement từ bước chú thích gốc của dataset được tham chiếu: Cohen's κ = 0.663–0.801 (Paper #11 (Jira, κ = 0.663–0.801), n=139). Giá trị này thiết lập đường cơ sở cho độ tin cậy của nhãn trong dataset, với κ ≥ 0.60 theo tiêu chí của chính RQ gốc.

- **Metric:** Cohen's Kappa (κ_control)
- **Mục đích:**
  - Xác lập giới hạn tin cậy của chú thích người
  - Cung cấp tham chiếu để diễn giải agreement người–LLM

---

### 6.5 Tổng hợp Mục tiêu Đánh giá

| Câu hỏi | Tiêu chí |
|---|---|
| RQ1 / SQ1 | Agreement tổng thể κ ≥ 0.70 (tiêu chí thành công chính) |
| SQ2 | Sự khác biệt agreement theo từng chiều của bug report |
| SQ3 | Xác định các mẫu bất đồng có hệ thống |
| κ_control | Baseline độ tin cậy chú thích người |

---

## 7. Các Mối Đe dọa đến Giá trị Nghiên cứu

Phần này thảo luận các mối đe dọa tiềm năng đến giá trị của thiết kế thực nghiệm và cách chúng được giảm thiểu trong bối cảnh đánh giá LLM-based reproducibility trên tập Mojira.

---

### 7.1 Giá trị Nội tại (Internal Validity)

Mối đe dọa chính là **sự không ổn định của mô hình giữa các lần chạy hoặc phiên bản**. Để giảm thiểu:
- Sử dụng snapshot mô hình cố định (`gpt-4o-mini-2024-07-18`) thay vì alias
- Temperature = 0 để đảm bảo output xác định
- Sử dụng một template prompt duy nhất nhất quán cho toàn bộ 139 report
- Không chỉnh sửa prompt trong suốt quá trình thực nghiệm

Mối đe dọa khác là **sai lệch từ thiết kế prompt**, có thể ảnh hưởng đến hành vi chấm điểm của LLM. Được giảm thiểu một phần thông qua:
- Rubric ordinal được định nghĩa rõ ràng (thang 1–5)
- Chiến lược fallback có kiểm soát (zero-shot → few-shot chỉ theo điều kiện pilot đã định)

---

### 7.2 Giá trị Cấu trúc (Construct Validity)

Giá trị cấu trúc liên quan đến việc đánh giá có thực sự đo "reproducibility" hay không.

Các mối đe dọa tiềm năng:
- Sự không khớp giữa cách người và LLM diễn giải reproducibility
- Phụ thuộc vào trích xuất có cấu trúc (Steps to Reproduce, Expected/Observed Behavior), có thể gây sai lệch trừu tượng hóa
- Điểm ordinal (1–5) có thể không nắm bắt được các sắc thái tinh tế trong chất lượng bug report

Chiến lược giảm thiểu:
- Căn chỉnh với hướng dẫn chú thích người sẵn có trong dataset (`evaluation_metrics.yaml`)
- Sử dụng cùng cấu trúc rubric cho cả người và LLM
- Đánh giá theo từng chiều (SQ2) để giảm thiểu sự trừu tượng hóa từ điểm tổng hợp duy nhất

---

### 7.3 Giá trị Ngoại tại (External Validity)

Nghiên cứu bị giới hạn trong:
- Bug report Mojira Minecraft
- Domain phần mềm nguồn mở (bối cảnh phát triển game)

Điều này có thể hạn chế khả năng tổng quát hóa sang:
- Hệ thống bug tracking doanh nghiệp
- Domain phần mềm không phải Minecraft hay không phải game
- Issue tracker công nghiệp với tiêu chuẩn báo cáo khác nhau

Tuy nhiên, dataset trải rộng nhiều loại bug kỹ thuật khác nhau và có thể so sánh với các nghiên cứu trước về phân tích bug report OSS.

---

### 7.4 Giá trị Kết luận (Conclusion Validity)

Các mối đe dọa phát sinh từ lựa chọn suy luận thống kê:
- Cohen's Kappa có thể nhạy cảm với class imbalance trong điểm ordinal
- Bootstrap confidence interval có thể biến động tùy thuộc vào phương sai resampling
- Wilcoxon signed-rank test giả định phân phối đối xứng của sai khác cặp

Chiến lược giảm thiểu:
- Sử dụng bootstrap confidence interval cho κ thay vì giả định tiệm cận
- Chọn Wilcoxon test phi tham số thay vì t-test do tính chất ordinal của dữ liệu
- Báo cáo effect size (rank-biserial correlation) cùng với p-value

---

### 7.5 Độ Tin cậy và Tính Tái lập

Để đảm bảo tính tái lập của kết quả:
- Toàn bộ thực nghiệm dùng dataset cố định (139 bug report Mojira)
- Phiên bản mô hình được pin tường minh
- Template prompt được cố định và quản lý phiên bản
- Tính ngẫu nhiên trong lấy mẫu được loại bỏ (không resampling động trong quá trình đánh giá)
- Phân tích thống kê dùng các thư viện chuẩn (`scikit-learn`, `scipy`, `pingouin`)

---

## 8. Timeline & Tài nguyên

### 8.0 Phân công Vai trò và Trách nhiệm

Thực nghiệm được thực hiện bởi nhóm 5 thành viên. **Quan trọng:** Chú thích người dùng làm ground truth **đã có sẵn trong dataset ImproBR** và không được thu thập hay xác nhận lại trong nghiên cứu này. Vai trò của mỗi thành viên tập trung vào chuẩn bị pipeline, chạy LLM, và phân tích thống kê.
 
| Vai trò | Thành viên | Trách nhiệm |
|---|---|---|
| PL (Project Lead) | Nguyễn Hồng Quân (SE203653) | Điều phối tổng thể, kiểm tra tính nhất quán phương pháp, nộp bài cuối |
| DG (Data) | Nguyễn Thành Lộc (SE203692) | Chuẩn bị dataset Mojira (139 issue từ ImproBR), triển khai pipeline tiền xử lý, xác minh scoring logic (§5.3) |
| LR (LLM Runner) | Tống Gia Huy (SE160995) | Pipeline suy luận LLM (thiết lập GPT-4o mini), triển khai prompt, thực thi batch, ghi log output và theo dõi chi phí |
| MS (Stats) | Trần Thái Dương (SE193500) | Phân tích thống kê: Cohen's Kappa, Wilcoxon signed-rank test, bootstrap confidence interval, tính effect size, và per-dimension κ rescoring (§6.2) |
| RW (Writer) | Lâm Song Toàn (SE200458) | Viết tài liệu: phần giới thiệu, các mối đe dọa giá trị (§7), kết luận và tạo hình minh họa |
 
**Lưu ý về Nguồn Chú thích:**
- Ground truth annotations **đã có sẵn trong dataset ImproBR** từ hai annotators độc lập (không phải từ thành viên nhóm LR hay RW).
- Các chú thích này được coi là **ground truth cố định** và không bị sửa đổi, xác nhận lại, hoặc chú thích lại trong nghiên cứu này.
- Mọi xử lý (scoring function, tổng hợp) chỉ được áp dụng nhất quán trên các nhãn sẵn có.
- **Không có thành viên nào thực hiện gán nhãn thủ công bổ sung.**

---

### 8.1 Kiểm kê Tài nguyên

| Tài nguyên | Trạng thái | Phụ trách | Ghi chú |
|---|---|---|---|
| Dataset (Mojira Minecraft Issue Tracker – 139 bug report) | ✅ | DG | Dữ liệu issue công khai từ Mojira. Mỗi report có các trường có cấu trúc và **chú thích người sẵn có (2 annotator mỗi issue)** dùng làm ground truth. |
| LLM API (GPT-4o mini) | ⚠️ | LR | Chi phí API dựa trên token tiêu thụ. Ước tính < $5 cho toàn bộ 139 report theo cấu hình prompt hiện tại. |
| Tính toán | ✅ | LR | Không cần GPU. Toàn bộ pipeline chạy qua API call + phân tích thống kê cục bộ (scikit-learn / scipy) trên CPU hoặc Colab miễn phí. |
| Chú thích ground truth | ✅ | Dataset Mojira sẵn có | Chú thích người sẵn có trong dataset (Author 1 & Author 2 mỗi issue). **Không được tạo mới trong nghiên cứu này** — được sử dụng trực tiếp hoặc sau tổng hợp nhất quán (trung bình/majority vote) để đánh giá. |

---

### 8.2 Ước tính Chi phí

| Hạng mục | Khối lượng | Đơn giá (ước tính) | Tổng |
|---|---|---|---|
| GPT-4o mini — input tokens | ~139 report × ~800 token | ~$0.15 / 1M token | ~$0.017 |
| GPT-4o mini — output tokens | ~139 report × ~150 token | ~$0.60 / 1M token | ~$0.012 |
| Pilot + retry overhead (few-shot fallback, logging, re-run) | ~2× buffer đánh giá | — | ~$0.05 |
| **Tổng ước tính** | | | **< $0.10** |

---

### 8.3 Timeline (Tuần 5–10)

> Tuần 5–6: Chuẩn bị đề xuất · Tuần 7–8: Thực thi thực nghiệm (xem §5–6) · Tuần 9–10: Viết và thuyết trình (xem RBL-5)
> Hạn nộp đề xuất: **2026-06-26**

| Tuần | Hoạt động | Phụ trách | Checkpoint |
|---|---|---|---|
| 5 | Viết đề xuất §2–§7 | DG + RW + PL | Draft `proposal.md` (các mục §2–§7) |
| 5 | Chuẩn bị dataset (Mojira 139 report) | DG | `data/processed/` + README |
| 5 | Thiết lập API + test pipeline suy luận | LR | `test_api.py` + ghi log chi phí |
| 5 | Draft script thống kê (Kappa, Wilcoxon) | MS | Draft `compute_metrics.py` |
| 6 | Hoàn thiện đề xuất §8 + nộp | PL | `proposal.md v1.0` đã nộp |
| 6 | Checkpoint phê duyệt giám sát viên | PL | Đã phê duyệt / Cần chỉnh sửa |
| 7 | Thực nghiệm pilot (10–15 report) | LR | `pilot_llm_output.csv` |
| 7 | Phân tích pilot (κ, kiểm tra phương sai) | MS | `pilot_analysis.ipynb` |
| 7 | Họp review pilot | PL | Quyết định: tiếp tục / điều chỉnh |
| 8 | Suy luận LLM đầy đủ (139 report) | LR | `full_llm_output.csv` |
| 8 | Đánh giá thống kê (κ, Wilcoxon, CI) | MS | `full_analysis.ipynb` |
| 8 | Ghi chép sử dụng ground truth | DG | Đã xác minh tính nhất quán dataset |
| 8 | Tạo hình minh họa | RW | `figures/` |
| 9–10 | Viết + thuyết trình | Tất cả | Bài báo cuối + slides |

---

### 8.4 Kế hoạch Dự phòng

**Nếu đề xuất không được phê duyệt vào Tuần 6:**
Thu hẹp phạm vi chỉ còn SQ1 và thông báo cho giám sát viên để điều chỉnh.

**Nếu gặp giới hạn tốc độ API:**
Xử lý theo batch với độ trễ giữa các lần gọi; không thay đổi phương pháp.

**Nếu một phần issue Mojira không thể truy cập:**
Chỉ thay thế các mẫu bị thiếu trong hệ sinh thái Mojira (không thay thế từ issue tracker khác). Lấy mẫu lại trong Mojira để duy trì tính nhất quán.

**Nếu pilot phát hiện vấn đề phương pháp (Tuần 7):**
Nộp đề xuất sửa đổi trong vòng 24 giờ (xem §8.6).

**Nếu xảy ra chậm trễ từ thành viên:**
PL phân phối lại khối lượng công việc sau ngưỡng chậm trễ 48 giờ.

---

### 8.5 Checkpoint Theo Vai trò

| Vai trò | Tuần 5 | Tuần 6 | Tuần 7 | Tuần 8 |
|---|---|---|---|---|
| PL | Review draft §2–§7 | Nộp đề xuất | Họp quyết định pilot | Kiểm tra tính nhất quán §5–§6 |
| DG | Chuẩn bị dataset Mojira | Xác nhận tài nguyên | Hỗ trợ điều phối pilot | Hỗ trợ xác minh full run |
| LR | Test pipeline API | Xác nhận chi phí & thiết lập | Chạy pilot + output LLM | Chạy suy luận đầy đủ |
| MS | Draft triển khai metric | Hoàn thiện kế hoạch thống kê | Phân tích pilot | Kiểm định thống kê đầy đủ |
| RW | Draft §7 | Proofread đề xuất | Hỗ trợ báo cáo pilot | Hình minh họa + viết cuối |

---

### 8.6 Quy trình Sửa đổi

Nếu pilot (Tuần 7) phát hiện vấn đề phương pháp (ví dụ: metric agreement không ổn định, giả định thống kê không hợp lệ, hoặc ràng buộc dataset), nhóm nộp:

`proposal-amendment-v1.1.md`

trong vòng 24 giờ cho giám sát viên, bao gồm:
- Vấn đề được xác định
- Sửa đổi đề xuất (trước → sau)
- Căn cứ (phương pháp / thống kê)
- Các mục bị ảnh hưởng (chủ yếu §5–§6)

---

**Ràng buộc quan trọng:**
- ❌ Không cho phép sửa đổi dựa trên kết quả kém một mình
- ❌ Không thay đổi metric sau khi đã quan sát kết quả thực nghiệm đầy đủ (ngăn chặn HARKing)



---

## 9. Addendum v1.1 — Dual-Dataset Design (Raw + Improved)

*(This addendum is written in English and extends the proposal above. It records
a scope change agreed after the initial draft; the core protocol, model
configuration, scoring function, and statistical methods are unchanged.)*

### 9.1 Scope change

All reports and annotations come from the **ImproBR replication package**
(Akyol et al., 2026, arXiv:2604.26142). That package contains **two forms** of
each of the 139 Mojira Minecraft issues:

- **Raw** — the original bug report as submitted to Mojira.
- **Improved** — the same report after the ImproBR LLM pipeline rewrote it to be
  more complete (clarifying or adding Steps to Reproduce, Observed Behavior,
  Expected Behavior, and Environment).

Whereas the original proposal treated only the Raw form as the study dataset and
the Improved form as supplementary, **this addendum treats the Raw and Improved
forms as two co-equal datasets.** We run the identical evaluation pipeline
(same model, prompt design, deterministic scoring function, and statistics) on
each form and report both.

### 9.2 Updated research question

For each form (Raw and Improved) of the Mojira bug reports (P), when GPT-4o mini
is used as an automated reproducibility evaluator (I), compared against the
existing two-annotator human labels (C), how strong is the agreement measured by
Cohen's Kappa (O)? The **primary comparison** is between the two forms: does the
LLM stay as close to human judgment on the AI-improved reports as on the
original ones?

- **SQ1 (per form):** overall composite kappa on Raw and on Improved.
- **SQ2 (per form):** per-dimension kappa (S2R, OB, EB) on each form.
- **SQ3 (comparison):** how and why agreement differs between the two forms,
  including any systematic bias introduced by the AI rewriting.

### 9.3 Success criterion (revised)

We report kappa_Raw and kappa_Improved side by side, each compared
**independently** against the pre-registered threshold kappa >= 0.70. The study
does not require both to pass; the scientific contribution is the **comparison**
of the two, not a single pass/fail verdict. The human-human control
kappa_control is likewise computed per form as the reliability ceiling for that
form.

### 9.4 Both datasets follow the same two-phase pipeline

Each form runs its own Pilot (26 reports) -> Full (139 reports) sequence with the
same gating rules from Section 5.1. The full-phase prompt is held identical to
the pilot prompt for each form (Raw: the V10 pilot prompt; Improved: the V18
pilot prompt), consistent with the fixed-prompt design and the anti-HARKing
constraints in Section 8.6.

### 9.5 Results summary (full phase, N = 139 per form)

| Measure | Raw | Improved |
|---|---|---|
| Composite kappa (LLM vs. human) | 0.578 | 0.335 |
| 95% bootstrap CI | [0.471, 0.684] | [0.226, 0.441] |
| Accuracy | 71.9% | 62.6% |
| kappa_control (human-human) | 0.674 | 0.556 |
| S2R kappa | 0.693 | 0.654 |
| EB kappa | 0.556 | 0.161 |
| OB kappa | 0.289 | 0.130 |
| Wilcoxon p (bias) | 0.452 (none) | <10^-6 (optimistic) |
| Binary >=4 accuracy | 87.1% | 86.3% |
| Meets kappa >= 0.70? | No | No |

**Key finding:** the LLM's agreement with humans is moderate and unbiased on Raw
reports, but drops to only fair agreement with a strong optimistic bias on
Improved reports — it rates the AI-polished text as reproducible far more often
than the human annotators do (111/139 vs. 94/139 at score >= 4). Full analysis,
figures, and the qualitative disagreement discussion are in `paper/`.
