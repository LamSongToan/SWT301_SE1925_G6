# Results Directory Overview / Tổng quan thư mục Results

## English

### Purpose — English

The `Results` directory stores all experiment outputs for the Bug Report Quality Assessment with LLM project.

It contains:

- official Pilot results for Raw and Improved reports;
- Full Development results;
- Full Pilot Validation results;
- final protected Holdout results;
- Raw-versus-Improved comparison files;
- the SHA-256 record of the frozen configuration used before Holdout evaluation.

The final research conclusion must be based on the protected Holdout results, not on Development or Pilot Validation metrics.

### Directory classification — English

| Directory or file | Phase | Purpose |
| --- | --- | --- |
| `Results/Raw` | Official Pilot | Stores the final Raw Pilot outputs for 26 cases. |
| `Results/Improved` | Official Pilot | Stores the final Improved Pilot outputs for 26 cases. |
| `Results/comparison_raw_vs_improved_pilot.csv` | Official Pilot comparison | Compares Raw and Improved Pilot metrics. |
| `Results/Full/Development` | Full Development | Stores the 75-case Development outputs used for prompt and rule calibration. |
| `Results/Full/Pilot_Validation` | Full Pilot Validation | Stores the candidate Full configuration results on the 26 Pilot cases. |
| `Results/Full/Holdout` | Full Holdout | Stores the final protected evaluation results for 38 cases. |
| `Results/Full/frozen_configuration_sha256.csv` | Frozen configuration record | Stores SHA-256 hashes for the configuration frozen before the Holdout run. |

### Common result files — English

Each Raw or Improved experiment directory may contain the following file types:

| File pattern | Description |
| --- | --- |
| `*_api_log_*.csv` | API execution log, including case status, prediction, token usage, and technical metadata. |
| `*_llm_output_*.csv` | Structured LLM predictions and complete evaluation output for each case. |
| `mismatch_analysis_*.csv` | Cases where the LLM Steps to Reproduce label differs from Ground Truth. |
| `summary_*.csv` | Aggregate metrics, confusion matrix, token usage, cost, and threshold status. |
| `comparison_raw_vs_improved_*.csv` | Side-by-side comparison between Raw and Improved metrics for the same phase. |
| `README.md` | Phase-specific documentation for the directory. |

### Official Pilot results — English

#### `Results/Raw` — English

This directory stores the official Raw Pilot result produced with:

- model: `gpt-4o-mini-2024-07-18`;
- seed: `210`;
- prompt: `Prompts_Raw_Final_V10_PilotCandidate`;
- cases: `26`.

| Metric | Value |
| --- | ---: |
| Accuracy | `0.9615` |
| Cohen's Kappa | `0.9202` |
| Mismatches | `1` |
| Threshold `0.70` | Passed |

#### `Results/Improved` — English

This directory stores the official Improved Pilot result produced with:

- model: `gpt-4o-mini-2024-07-18`;
- seed: `210`;
- prompt: `Prompts_Improved_Final_V18_PilotCandidate`;
- cases: `26`.

| Metric | Value |
| --- | ---: |
| Accuracy | `1.0000` |
| Cohen's Kappa | `1.0000` |
| Mismatches | `0` |
| Threshold `0.70` | Passed |

The official Pilot comparison is stored in:

`Results/comparison_raw_vs_improved_pilot.csv`

### Full Development results — English

The `Results/Full/Development` directory stores the final candidate Full results on 75 Development cases.

Development was used for prompt refinement, Full-only rule calibration, and mismatch analysis.

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.9467` | `0.8678` | `4` | Passed |
| Improved V20 | `0.9200` | `0.8085` | `6` | Passed |

The comparison file is:

`Results/Full/Development/comparison_raw_vs_improved_development.csv`

Development results are supporting calibration results and are not the final generalization result.

### Full Pilot Validation results — English

The `Results/Full/Pilot_Validation` directory stores the candidate Full configuration results on the same 26 Pilot cases.

Pilot Validation does not overwrite the official Pilot outputs. It verifies that the Full configuration still preserves acceptable agreement on the Pilot cases.

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.9231` | `0.8375` | `2` | Passed |
| Improved V20 | `0.9615` | `0.9065` | `1` | Passed |

The comparison file is:

`Results/Full/Pilot_Validation/comparison_raw_vs_improved_pilot_validation.csv`

Pilot Validation was required before the protected Holdout evaluation.

### Final protected Holdout results — English

The `Results/Full/Holdout` directory stores the final evaluation on 38 protected cases.

The Full configuration was frozen before this phase. Holdout cases were not used for prompt tuning or rule development.

| Version | Accuracy | Cohen's Kappa | Mismatches | Threshold |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.6842` | `0.2349` | `12` | Not passed |
| Improved V20 | `0.6842` | `0.0988` | `12` | Not passed |

The comparison file is:

`Results/Full/Holdout/comparison_raw_vs_improved_holdout.csv`

Final interpretation:

- neither Raw nor Improved reached the predefined Cohen's Kappa threshold of `0.70`;
- the Improved configuration showed a strong prediction bias toward the `Executable` class;
- the high Development and Pilot Validation performance did not generalize to the protected Holdout set;
- the Holdout metrics are the official final research results.

### Frozen configuration record — English

The file `Results/Full/frozen_configuration_sha256.csv` records SHA-256 hashes for the files frozen before Holdout evaluation.

It is retained to demonstrate that the final Holdout run used the same fixed model, prompts, metric logic, and experiment configuration that had already passed Development and Pilot Validation.

### Result flow — English

The experiment result flow is:

1. Run and retain the official Raw and Improved Pilot results.
2. Develop and calibrate the candidate Full configuration on Development.
3. validate the candidate Full configuration on Pilot Validation.
4. freeze the configuration and record SHA-256 hashes.
5. run the protected Holdout exactly once.
6. use Holdout metrics as the final answer to the research question.

### Important rules — English

- Do not overwrite the official Pilot results in `Results/Raw` or `Results/Improved`.
- Do not use Pilot Validation output as a replacement for official Pilot output.
- Do not use Holdout mismatches to tune prompts or rules.
- Do not rerun the same Holdout set to improve the reported metrics.
- Keep all summary, mismatch, API log, LLM output, comparison, and frozen-hash files for reproducibility.
- Use the protected Holdout results for the final research conclusion.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Results` lưu toàn bộ kết quả thí nghiệm của dự án Bug Report Quality Assessment with LLM.

Thư mục bao gồm:

- kết quả Pilot chính thức cho Raw và Improved;
- kết quả Full Development;
- kết quả Full Pilot Validation;
- kết quả Holdout được bảo vệ cuối cùng;
- các file so sánh Raw và Improved;
- file SHA-256 của cấu hình đã được đóng băng trước khi chạy Holdout.

Kết luận nghiên cứu cuối phải dựa trên kết quả Holdout được bảo vệ, không dựa trên Development hoặc Pilot Validation.

### Phân loại thư mục — Tiếng Việt

| Thư mục hoặc file | Giai đoạn | Mục đích |
| --- | --- | --- |
| `Results/Raw` | Pilot chính thức | Lưu kết quả Pilot Raw cuối cho 26 case. |
| `Results/Improved` | Pilot chính thức | Lưu kết quả Pilot Improved cuối cho 26 case. |
| `Results/comparison_raw_vs_improved_pilot.csv` | So sánh Pilot chính thức | So sánh chỉ số Pilot giữa Raw và Improved. |
| `Results/Full/Development` | Full Development | Lưu kết quả 75 case Development dùng để hiệu chỉnh prompt và rule. |
| `Results/Full/Pilot_Validation` | Full Pilot Validation | Lưu kết quả cấu hình Full candidate trên 26 case Pilot. |
| `Results/Full/Holdout` | Full Holdout | Lưu kết quả đánh giá cuối được bảo vệ cho 38 case. |
| `Results/Full/frozen_configuration_sha256.csv` | Bản ghi cấu hình đóng băng | Lưu SHA-256 của cấu hình được đóng băng trước khi chạy Holdout. |

### Các loại file kết quả chung — Tiếng Việt

Mỗi thư mục thí nghiệm Raw hoặc Improved có thể chứa các loại file sau:

| Mẫu tên file | Mô tả |
| --- | --- |
| `*_api_log_*.csv` | Nhật ký gọi API, gồm trạng thái case, dự đoán, token và metadata kỹ thuật. |
| `*_llm_output_*.csv` | Dự đoán LLM có cấu trúc và toàn bộ kết quả đánh giá của từng case. |
| `mismatch_analysis_*.csv` | Các case có nhãn Steps to Reproduce của LLM khác Ground Truth. |
| `summary_*.csv` | Chỉ số tổng hợp, confusion matrix, token, chi phí và trạng thái ngưỡng. |
| `comparison_raw_vs_improved_*.csv` | So sánh Raw và Improved trong cùng một giai đoạn. |
| `README.md` | Tài liệu mô tả riêng cho từng thư mục giai đoạn. |

### Kết quả Pilot chính thức — Tiếng Việt

#### `Results/Raw` — Tiếng Việt

Thư mục này lưu kết quả Pilot Raw chính thức với:

- mô hình: `gpt-4o-mini-2024-07-18`;
- seed: `210`;
- prompt: `Prompts_Raw_Final_V10_PilotCandidate`;
- số case: `26`.

| Chỉ số | Giá trị |
| --- | ---: |
| Accuracy | `0.9615` |
| Cohen's Kappa | `0.9202` |
| Mismatch | `1` |
| Ngưỡng `0.70` | Đạt |

#### `Results/Improved` — Tiếng Việt

Thư mục này lưu kết quả Pilot Improved chính thức với:

- mô hình: `gpt-4o-mini-2024-07-18`;
- seed: `210`;
- prompt: `Prompts_Improved_Final_V18_PilotCandidate`;
- số case: `26`.

| Chỉ số | Giá trị |
| --- | ---: |
| Accuracy | `1.0000` |
| Cohen's Kappa | `1.0000` |
| Mismatch | `0` |
| Ngưỡng `0.70` | Đạt |

File so sánh Pilot chính thức được lưu tại:

`Results/comparison_raw_vs_improved_pilot.csv`

### Kết quả Full Development — Tiếng Việt

Thư mục `Results/Full/Development` lưu kết quả cấu hình Full candidate trên 75 case Development.

Development được dùng để điều chỉnh prompt, hiệu chỉnh Full-only rule và phân tích mismatch.

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.9467` | `0.8678` | `4` | Đạt |
| Improved V20 | `0.9200` | `0.8085` | `6` | Đạt |

File so sánh được lưu tại:

`Results/Full/Development/comparison_raw_vs_improved_development.csv`

Kết quả Development chỉ là kết quả hiệu chỉnh hỗ trợ, không phải kết quả tổng quát hóa cuối.

### Kết quả Full Pilot Validation — Tiếng Việt

Thư mục `Results/Full/Pilot_Validation` lưu kết quả cấu hình Full candidate trên cùng 26 case Pilot.

Pilot Validation không ghi đè kết quả Pilot chính thức. Giai đoạn này kiểm tra cấu hình Full vẫn giữ mức đồng thuận chấp nhận được trên các case Pilot.

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.9231` | `0.8375` | `2` | Đạt |
| Improved V20 | `0.9615` | `0.9065` | `1` | Đạt |

File so sánh được lưu tại:

`Results/Full/Pilot_Validation/comparison_raw_vs_improved_pilot_validation.csv`

Pilot Validation phải đạt trước khi thực hiện đánh giá Holdout được bảo vệ.

### Kết quả Holdout được bảo vệ cuối — Tiếng Việt

Thư mục `Results/Full/Holdout` lưu kết quả đánh giá cuối trên 38 case được bảo vệ.

Cấu hình Full đã được đóng băng trước giai đoạn này. Case Holdout không được dùng để chỉnh prompt hoặc phát triển rule.

| Phiên bản | Accuracy | Cohen's Kappa | Mismatch | Trạng thái ngưỡng |
| --- | ---: | ---: | ---: | --- |
| Raw V11 | `0.6842` | `0.2349` | `12` | Không đạt |
| Improved V20 | `0.6842` | `0.0988` | `12` | Không đạt |

File so sánh được lưu tại:

`Results/Full/Holdout/comparison_raw_vs_improved_holdout.csv`

Diễn giải cuối:

- cả Raw và Improved đều không đạt ngưỡng Cohen's Kappa `0.70`;
- cấu hình Improved có thiên lệch dự đoán mạnh về nhãn `Executable`;
- kết quả cao trên Development và Pilot Validation không tổng quát hóa sang Holdout được bảo vệ;
- chỉ số Holdout là kết quả nghiên cứu chính thức cuối cùng.

### Bản ghi cấu hình đóng băng — Tiếng Việt

File `Results/Full/frozen_configuration_sha256.csv` ghi SHA-256 của các file cấu hình đã được đóng băng trước khi đánh giá Holdout.

File này được giữ để chứng minh lần chạy Holdout cuối sử dụng cùng model, prompt, metric logic và cấu hình thí nghiệm đã vượt qua Development cùng Pilot Validation.

### Luồng kết quả — Tiếng Việt

Quy trình tạo kết quả diễn ra theo thứ tự:

1. Chạy và giữ kết quả Pilot Raw cùng Improved chính thức.
2. Phát triển và hiệu chỉnh cấu hình Full trên Development.
3. Xác nhận cấu hình Full candidate trên Pilot Validation.
4. Đóng băng cấu hình và ghi SHA-256.
5. Chạy Holdout được bảo vệ đúng một lần.
6. Dùng chỉ số Holdout làm câu trả lời cuối cho Research Question.

### Quy tắc quan trọng — Tiếng Việt

- Không ghi đè kết quả Pilot chính thức trong `Results/Raw` hoặc `Results/Improved`.
- Không dùng output Pilot Validation để thay thế output Pilot chính thức.
- Không dùng mismatch Holdout để chỉnh prompt hoặc rule.
- Không chạy lại cùng tập Holdout nhằm cải thiện chỉ số đã báo cáo.
- Giữ toàn bộ summary, mismatch, API log, LLM output, comparison và frozen hash để bảo đảm khả năng tái lập.
- Dùng kết quả Holdout được bảo vệ cho kết luận nghiên cứu cuối.
