# Official Improved Pilot Results / Kết quả Pilot Improved chính thức

## English

### Purpose — English

This directory stores the official Improved Pilot experiment results for 26 cases.

These results were produced with the frozen Improved Pilot configuration and are independent from Full Development, Pilot Validation, and Holdout results.

### Experiment configuration — English

| Item | Value |
| --- | --- |
| Phase | Official Pilot |
| Dataset version | Improved |
| Model | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Cases | `26` |
| Prompt version | `Prompts_Improved_Final_V18_PilotCandidate` |
| Cohen's Kappa threshold | `0.70` |

### Directory contents — English

| File | Description |
| --- | --- |
| `pilot_api_log_improved.csv` | API execution log for the official Improved Pilot run. |
| `pilot_llm_output_improved.csv` | LLM predictions and structured output for 26 Improved Pilot cases. |
| `mismatch_analysis_improved.csv` | Improved Pilot disagreements with Pilot Ground Truth. |
| `summary_improved.csv` | Official Improved Pilot metrics, confusion matrix, token usage, and cost. |
| `README.md` | Documentation for this result directory. |

The cross-version Pilot comparison is stored at:

`Results/comparison_raw_vs_improved_pilot.csv`

### Official Improved Pilot metrics — English

| Metric | Value |
| --- | ---: |
| Accuracy | `1.0000` |
| Cohen's Kappa | `1.0000` |
| Correct | `26` |
| Mismatches | `0` |
| Total cost | `$0.02291595` |

### Usage rules — English

- This directory belongs to the official Improved Pilot phase.
- These files must not be overwritten by Pilot Validation or Full runs.
- The official Pilot result is retained as calibration evidence.
- The final research conclusion must still be based on the protected Holdout results.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục này lưu kết quả thí nghiệm Pilot Improved chính thức cho 26 case.

Kết quả được tạo bằng cấu hình Pilot Improved đã đóng băng và độc lập với Full Development, Pilot Validation và Holdout.

### Cấu hình thí nghiệm — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Giai đoạn | Pilot chính thức |
| Phiên bản dữ liệu | Improved |
| Mô hình | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Số case | `26` |
| Phiên bản prompt | `Prompts_Improved_Final_V18_PilotCandidate` |
| Ngưỡng Cohen's Kappa | `0.70` |

### Nội dung thư mục — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `pilot_api_log_improved.csv` | Nhật ký gọi API của lần chạy Pilot Improved chính thức. |
| `pilot_llm_output_improved.csv` | Dự đoán LLM và output có cấu trúc cho 26 case Pilot Improved. |
| `mismatch_analysis_improved.csv` | Các bất đồng giữa Pilot Improved và Pilot Ground Truth. |
| `summary_improved.csv` | Chỉ số Pilot Improved chính thức, confusion matrix, token và chi phí. |
| `README.md` | Tài liệu mô tả thư mục kết quả này. |

File so sánh Pilot giữa Raw và Improved được lưu tại:

`Results/comparison_raw_vs_improved_pilot.csv`

### Chỉ số Pilot Improved chính thức — Tiếng Việt

| Chỉ số | Giá trị |
| --- | ---: |
| Accuracy | `1.0000` |
| Cohen's Kappa | `1.0000` |
| Số case đúng | `26` |
| Mismatch | `0` |
| Tổng chi phí | `$0.02291595` |

### Quy tắc sử dụng — Tiếng Việt

- Thư mục này thuộc giai đoạn Pilot Improved chính thức.
- Không được để Pilot Validation hoặc Full run ghi đè các file này.
- Kết quả Pilot chính thức được giữ làm bằng chứng hiệu chỉnh ban đầu.
- Kết luận nghiên cứu cuối vẫn phải dựa trên kết quả Holdout được bảo vệ.
