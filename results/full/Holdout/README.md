# Holdout Results / Kết quả Holdout

## English

### Purpose — English

This directory stores the final Raw and Improved results for the protected 38-case Holdout subset.

The Holdout subset was evaluated only after the Full configuration had been frozen using Development and Pilot Validation. These results represent the final generalization evaluation and the official answer to the predefined Cohen's Kappa threshold criterion.

### Experiment configuration — English

| Item | Value |
| --- | --- |
| Model | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Cases | `38` |
| Cohen's Kappa threshold | `0.70` |
| Raw prompt version | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Improved prompt version | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `holdout_api_log_raw.csv` | API execution log for the final Raw Holdout run. |
| `holdout_llm_output_raw.csv` | Final LLM predictions for 38 Raw Holdout cases. |
| `mismatch_analysis_holdout_raw.csv` | Raw Holdout label disagreements, retained for reporting and discussion only. |
| `summary_holdout_raw.csv` | Final Raw Holdout metrics, confusion matrix, token usage, and cost. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `holdout_api_log_improved.csv` | API execution log for the final Improved Holdout run. |
| `holdout_llm_output_improved.csv` | Final LLM predictions for 38 Improved Holdout cases. |
| `mismatch_analysis_holdout_improved.csv` | Improved Holdout label disagreements, retained for reporting and discussion only. |
| `summary_holdout_improved.csv` | Final Improved Holdout metrics, confusion matrix, token usage, and cost. |

#### Comparison file — English

| File | Description |
| --- | --- |
| `comparison_raw_vs_improved_holdout.csv` | Final comparison of Raw and Improved Holdout performance. |

### Final Holdout metrics — English

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.6842` | `0.2349` | `12` | Not passed |
| Improved | `0.6842` | `0.0988` | `12` | Not passed |

### Final interpretation — English

Neither Raw nor Improved reached the predefined Cohen's Kappa threshold of `0.70` on the protected Holdout set. The Improved configuration predicted the `Executable` class for almost all Holdout cases, which produced a strong class bias and low chance-corrected agreement.

### Usage rules — English

- This directory belongs to the final Full Holdout phase.
- Holdout mismatches may be analyzed only for reporting, discussion, threats to validity, and future work.
- Holdout cases must not be used to tune prompts or rules.
- The experiment must not be rerun on the same Holdout set to improve the reported metrics.
- These metrics are the final protected evaluation results.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục này lưu kết quả Raw và Improved cuối cùng của tập Holdout được bảo vệ gồm 38 case.

Tập Holdout chỉ được đánh giá sau khi cấu hình Full đã được đóng băng bằng Development và Pilot Validation. Kết quả trong thư mục này là đánh giá khả năng tổng quát hóa cuối và là cơ sở chính thức để trả lời tiêu chí ngưỡng Cohen's Kappa đã xác định trước.

### Cấu hình thí nghiệm — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Mô hình | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Số case | `38` |
| Ngưỡng Cohen's Kappa | `0.70` |
| Phiên bản prompt Raw | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Phiên bản prompt Improved | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `holdout_api_log_raw.csv` | Nhật ký gọi API của lần chạy Raw Holdout cuối. |
| `holdout_llm_output_raw.csv` | Dự đoán LLM cuối cho 38 case Raw Holdout. |
| `mismatch_analysis_holdout_raw.csv` | Các bất đồng nhãn Raw Holdout, chỉ giữ để báo cáo và thảo luận. |
| `summary_holdout_raw.csv` | Chỉ số Raw Holdout cuối, confusion matrix, token và chi phí. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `holdout_api_log_improved.csv` | Nhật ký gọi API của lần chạy Improved Holdout cuối. |
| `holdout_llm_output_improved.csv` | Dự đoán LLM cuối cho 38 case Improved Holdout. |
| `mismatch_analysis_holdout_improved.csv` | Các bất đồng nhãn Improved Holdout, chỉ giữ để báo cáo và thảo luận. |
| `summary_holdout_improved.csv` | Chỉ số Improved Holdout cuối, confusion matrix, token và chi phí. |

#### File so sánh — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `comparison_raw_vs_improved_holdout.csv` | So sánh kết quả Holdout cuối giữa Raw và Improved. |

### Chỉ số Holdout cuối — Tiếng Việt

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.6842` | `0.2349` | `12` | Không đạt |
| Improved | `0.6842` | `0.0988` | `12` | Không đạt |

### Diễn giải cuối — Tiếng Việt

Cả Raw và Improved đều không đạt ngưỡng Cohen's Kappa `0.70` trên tập Holdout được bảo vệ. Cấu hình Improved dự đoán nhãn `Executable` cho gần như toàn bộ case Holdout, dẫn đến thiên lệch lớp mạnh và mức đồng thuận sau khi hiệu chỉnh theo xác suất rất thấp.

### Quy tắc sử dụng — Tiếng Việt

- Thư mục này thuộc giai đoạn Full Holdout cuối.
- Chỉ được phân tích mismatch Holdout để viết báo cáo, thảo luận, threats to validity và future work.
- Không được dùng case Holdout để chỉnh prompt hoặc rule.
- Không được chạy lại cùng tập Holdout nhằm cải thiện chỉ số đã báo cáo.
- Các chỉ số trong thư mục này là kết quả đánh giá được bảo vệ cuối cùng.
