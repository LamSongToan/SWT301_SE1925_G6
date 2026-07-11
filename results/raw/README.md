# Official Raw Pilot Results / Kết quả Pilot Raw chính thức

## English

### Purpose — English

This directory stores the official Raw Pilot experiment results for 26 cases.

These results were produced with the frozen Raw Pilot configuration and are independent from Full Development, Pilot Validation, and Holdout results.

### Experiment configuration — English

| Item | Value |
| --- | --- |
| Phase | Official Pilot |
| Dataset version | Raw |
| Model | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Cases | `26` |
| Prompt version | `Prompts_Raw_Final_V10_PilotCandidate` |
| Cohen's Kappa threshold | `0.70` |

### Directory contents — English

| File | Description |
| --- | --- |
| `pilot_api_log_raw.csv` | API execution log for the official Raw Pilot run. |
| `pilot_llm_output_raw.csv` | LLM predictions and structured output for 26 Raw Pilot cases. |
| `mismatch_analysis_raw.csv` | Raw Pilot disagreements with Pilot Ground Truth. |
| `summary_raw.csv` | Official Raw Pilot metrics, confusion matrix, token usage, and cost. |
| `README.md` | Documentation for this result directory. |

The cross-version Pilot comparison is stored at:

`Results/comparison_raw_vs_improved_pilot.csv`

### Official Raw Pilot metrics — English

| Metric | Value |
| --- | ---: |
| Accuracy | `0.9615` |
| Cohen's Kappa | `0.9202` |
| Correct | `25` |
| Mismatches | `1` |
| Total cost | `$0.01290600` |

### Usage rules — English

- This directory belongs to the official Raw Pilot phase.
- These files must not be overwritten by Pilot Validation or Full runs.
- The official Pilot result is retained as calibration evidence.
- The final research conclusion must still be based on the protected Holdout results.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục này lưu kết quả thí nghiệm Pilot Raw chính thức cho 26 case.

Kết quả được tạo bằng cấu hình Pilot Raw đã đóng băng và độc lập với Full Development, Pilot Validation và Holdout.

### Cấu hình thí nghiệm — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Giai đoạn | Pilot chính thức |
| Phiên bản dữ liệu | Raw |
| Mô hình | `gpt-4o-mini-2024-07-18` |
| Seed | `210` |
| Số case | `26` |
| Phiên bản prompt | `Prompts_Raw_Final_V10_PilotCandidate` |
| Ngưỡng Cohen's Kappa | `0.70` |

### Nội dung thư mục — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `pilot_api_log_raw.csv` | Nhật ký gọi API của lần chạy Pilot Raw chính thức. |
| `pilot_llm_output_raw.csv` | Dự đoán LLM và output có cấu trúc cho 26 case Pilot Raw. |
| `mismatch_analysis_raw.csv` | Các bất đồng giữa Pilot Raw và Pilot Ground Truth. |
| `summary_raw.csv` | Chỉ số Pilot Raw chính thức, confusion matrix, token và chi phí. |
| `README.md` | Tài liệu mô tả thư mục kết quả này. |

File so sánh Pilot giữa Raw và Improved được lưu tại:

`Results/comparison_raw_vs_improved_pilot.csv`

### Chỉ số Pilot Raw chính thức — Tiếng Việt

| Chỉ số | Giá trị |
| --- | ---: |
| Accuracy | `0.9615` |
| Cohen's Kappa | `0.9202` |
| Số case đúng | `25` |
| Mismatch | `1` |
| Tổng chi phí | `$0.01290600` |

### Quy tắc sử dụng — Tiếng Việt

- Thư mục này thuộc giai đoạn Pilot Raw chính thức.
- Không được để Pilot Validation hoặc Full run ghi đè các file này.
- Kết quả Pilot chính thức được giữ làm bằng chứng hiệu chỉnh ban đầu.
- Kết luận nghiên cứu cuối vẫn phải dựa trên kết quả Holdout được bảo vệ.
