# Pilot Validation Results / Kết quả Pilot Validation

## English

### Purpose — English

This directory stores the Raw and Improved Pilot Validation results for the 26 Pilot cases.

Pilot Validation reuses the Pilot input data but evaluates it with the candidate Full prompts and Full-only consistency rules. It verifies that the Full configuration still preserves acceptable agreement on the original Pilot cases without overwriting the official Pilot results in `Results/Raw` and `Results/Improved`.

### Experiment configuration — English

| Item | Value |
| --- | --- |
| Model | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Cases | `26` |
| Cohen's Kappa threshold | `0.70` |
| Raw prompt version | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Improved prompt version | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `pilot_validation_api_log_raw.csv` | API execution log for Raw Pilot Validation. |
| `pilot_validation_llm_output_raw.csv` | Raw Pilot Validation predictions for 26 Pilot cases. |
| `mismatch_analysis_pilot_validation_raw.csv` | Raw Pilot Validation disagreements with Pilot Ground Truth. |
| `summary_pilot_validation_raw.csv` | Raw Pilot Validation metrics, confusion matrix, token usage, and cost. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `pilot_validation_api_log_improved.csv` | API execution log for Improved Pilot Validation. |
| `pilot_validation_llm_output_improved.csv` | Improved Pilot Validation predictions for 26 Pilot cases. |
| `mismatch_analysis_pilot_validation_improved.csv` | Improved Pilot Validation disagreements with Pilot Ground Truth. |
| `summary_pilot_validation_improved.csv` | Improved Pilot Validation metrics, confusion matrix, token usage, and cost. |

#### Comparison file — English

| File | Description |
| --- | --- |
| `comparison_raw_vs_improved_pilot_validation.csv` | Comparison of Raw and Improved Pilot Validation performance. |

### Final Pilot Validation metrics — English

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.9231` | `0.8375` | `2` | Passed |
| Improved | `0.9615` | `0.9065` | `1` | Passed |

### Relationship to frozen configuration — English

The file `Results/Full/frozen_configuration_sha256.csv` is stored one level above this directory. It records SHA-256 hashes for the frozen configuration used before the final Holdout evaluation.

### Usage rules — English

- This directory belongs to the Full Pilot Validation phase.
- Pilot Validation uses Pilot cases with the candidate Full configuration.
- It must not replace or overwrite the official Pilot results.
- Passing Pilot Validation was required before the protected Holdout run.
- Pilot Validation metrics are supporting validation results, not the final research conclusion.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục này lưu kết quả Raw và Improved của Pilot Validation trên 26 case Pilot.

Pilot Validation sử dụng lại dữ liệu đầu vào Pilot nhưng đánh giá bằng prompt Full candidate và các consistency rule chỉ dành cho Full. Mục đích là kiểm tra cấu hình Full vẫn giữ mức đồng thuận chấp nhận được trên các case Pilot ban đầu mà không ghi đè kết quả Pilot chính thức trong `Results/Raw` và `Results/Improved`.

### Cấu hình thí nghiệm — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Mô hình | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Số case | `26` |
| Ngưỡng Cohen's Kappa | `0.70` |
| Phiên bản prompt Raw | `Prompts_Raw_Final_V11_DevelopmentTuned` |
| Phiên bản prompt Improved | `Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20` |

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `pilot_validation_api_log_raw.csv` | Nhật ký gọi API của Raw Pilot Validation. |
| `pilot_validation_llm_output_raw.csv` | Dự đoán Raw Pilot Validation cho 26 case Pilot. |
| `mismatch_analysis_pilot_validation_raw.csv` | Các bất đồng giữa Raw Pilot Validation và Pilot Ground Truth. |
| `summary_pilot_validation_raw.csv` | Chỉ số Raw Pilot Validation, confusion matrix, token và chi phí. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `pilot_validation_api_log_improved.csv` | Nhật ký gọi API của Improved Pilot Validation. |
| `pilot_validation_llm_output_improved.csv` | Dự đoán Improved Pilot Validation cho 26 case Pilot. |
| `mismatch_analysis_pilot_validation_improved.csv` | Các bất đồng giữa Improved Pilot Validation và Pilot Ground Truth. |
| `summary_pilot_validation_improved.csv` | Chỉ số Improved Pilot Validation, confusion matrix, token và chi phí. |

#### File so sánh — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `comparison_raw_vs_improved_pilot_validation.csv` | So sánh kết quả Pilot Validation giữa Raw và Improved. |

### Chỉ số Pilot Validation cuối — Tiếng Việt

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw | `0.9231` | `0.8375` | `2` | Đạt |
| Improved | `0.9615` | `0.9065` | `1` | Đạt |

### Quan hệ với cấu hình đóng băng — Tiếng Việt

File `Results/Full/frozen_configuration_sha256.csv` được lưu ở thư mục cấp trên. File này ghi SHA-256 của cấu hình đã đóng băng trước khi đánh giá Holdout cuối.

### Quy tắc sử dụng — Tiếng Việt

- Thư mục này thuộc giai đoạn Full Pilot Validation.
- Pilot Validation sử dụng case Pilot với cấu hình Full candidate.
- Không được thay thế hoặc ghi đè kết quả Pilot chính thức.
- Pilot Validation phải đạt trước khi chạy Holdout được bảo vệ.
- Chỉ số Pilot Validation là kết quả xác nhận hỗ trợ, không phải kết luận nghiên cứu cuối.
