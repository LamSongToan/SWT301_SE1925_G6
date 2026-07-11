# Development Results / Kết quả Development

## English

### Purpose — English

This directory stores the Raw and Improved results for the 75-case Development subset.

The Development subset was used to develop, calibrate, and verify the Full prompts and Full-only consistency rules before Pilot Validation and Holdout evaluation. Its metrics are not the final research conclusion.

### Experiment configuration — English

| Item | Value |
| --- | --- |
| Model | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Cases | `75` |
| Cohen's Kappa threshold | `0.70` |
| Raw prompt version | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Improved prompt version | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `development_api_log_raw.csv` | API execution log for the Raw Development run. |
| `development_llm_output_raw.csv` | LLM predictions and structured evaluation output for 75 Raw Development cases. |
| `mismatch_analysis_development_raw.csv` | Raw Development cases where the LLM label differs from Ground Truth. |
| `summary_development_raw.csv` | Final Raw Development metrics, confusion matrix, token usage, and cost. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `development_api_log_improved.csv` | API execution log for the Improved Development run. |
| `development_llm_output_improved.csv` | LLM predictions and structured evaluation output for 75 Improved Development cases. |
| `mismatch_analysis_development_improved.csv` | Improved Development cases where the LLM label differs from Ground Truth. |
| `summary_development_improved.csv` | Final Improved Development metrics, confusion matrix, token usage, and cost. |

#### Comparison file — English

| File | Description |
| --- | --- |
| `comparison_raw_vs_improved_development.csv` | Direct comparison of the final Raw and Improved Development metrics. |

### Final Development metrics — English

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.9467` | `0.8678` | `4` | Passed |
| Improved | `0.9200` | `0.8085` | `6` | Passed |

### Usage rules — English

- This directory belongs to the Full Development phase.
- Development results may be used for prompt refinement, rule calibration, and mismatch analysis.
- Development metrics must not be reported as the final generalization result.
- The final research conclusion must be based on the protected Holdout results.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục này lưu kết quả Raw và Improved của tập Development gồm 75 case.

Tập Development được dùng để phát triển, hiệu chỉnh và kiểm tra các prompt Full cùng các consistency rule chỉ dành cho Full trước khi thực hiện Pilot Validation và Holdout. Các chỉ số trong thư mục này không phải kết luận cuối của nghiên cứu.

### Cấu hình thí nghiệm — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Mô hình | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Số case | `75` |
| Ngưỡng Cohen's Kappa | `0.70` |
| Phiên bản prompt Raw | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Phiên bản prompt Improved | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `development_api_log_raw.csv` | Nhật ký gọi API của lần chạy Raw Development. |
| `development_llm_output_raw.csv` | Dự đoán LLM và kết quả đánh giá có cấu trúc cho 75 case Raw Development. |
| `mismatch_analysis_development_raw.csv` | Các case Raw Development có nhãn LLM khác Ground Truth. |
| `summary_development_raw.csv` | Chỉ số Raw Development cuối, confusion matrix, token và chi phí. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `development_api_log_improved.csv` | Nhật ký gọi API của lần chạy Improved Development. |
| `development_llm_output_improved.csv` | Dự đoán LLM và kết quả đánh giá có cấu trúc cho 75 case Improved Development. |
| `mismatch_analysis_development_improved.csv` | Các case Improved Development có nhãn LLM khác Ground Truth. |
| `summary_development_improved.csv` | Chỉ số Improved Development cuối, confusion matrix, token và chi phí. |

#### File so sánh — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `comparison_raw_vs_improved_development.csv` | So sánh trực tiếp chỉ số Development cuối giữa Raw và Improved. |

### Chỉ số Development cuối — Tiếng Việt

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.9467` | `0.8678` | `4` | Đạt |
| Improved | `0.9200` | `0.8085` | `6` | Đạt |

### Quy tắc sử dụng — Tiếng Việt

- Thư mục này thuộc giai đoạn Full Development.
- Có thể dùng kết quả Development để chỉnh prompt, hiệu chỉnh rule và phân tích mismatch.
- Không được dùng chỉ số Development làm kết quả tổng quát hóa cuối.
- Kết luận nghiên cứu cuối phải dựa trên kết quả Holdout được bảo vệ.
