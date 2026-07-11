# Protected Holdout Dataset / Bộ dữ liệu Holdout được bảo vệ

## English

### Purpose — English

The `Data/Full/Holdout` directory stores 38 protected cases used only for the
final generalization evaluation.

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `holdout_sample_raw.csv` | Raw Holdout sample containing 38 cases. |
| `holdout_ground_truth_raw.csv` | Raw Holdout Ground Truth containing 38 cases. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `holdout_sample_improved.csv` | Improved Holdout sample containing 38 cases. |
| `holdout_ground_truth_improved.csv` | Improved Holdout Ground Truth containing 38 cases. |

### Split properties — English

| Item | Value |
| --- | --- |
| Split seed | `210` |
| Number of cases | `38` |
| Pilot overlap | `0` |
| Development overlap | `0` |
| Evaluation role | Final protected evaluation |

### Protection rules — English

- Do not use Holdout cases for prompt tuning.
- Do not add rules based on Holdout mismatches.
- Do not run case-level API tests on Holdout.
- Do not use partial Holdout runs.
- Do not rerun the same Holdout to improve metrics.
- Holdout Ground Truth is used only during final metric computation.

### Final-evaluation meaning — English

The Holdout metrics are the official final research results. Whether the
predefined Cohen's Kappa threshold is passed or not, the reported Holdout result
must be retained without post-hoc tuning on these cases.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Full/Holdout` lưu 38 case được bảo vệ, chỉ dùng cho đánh giá khả
năng tổng quát hóa cuối cùng.

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `holdout_sample_raw.csv` | Mẫu Raw Holdout gồm 38 case. |
| `holdout_ground_truth_raw.csv` | Ground Truth Raw Holdout gồm 38 case. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `holdout_sample_improved.csv` | Mẫu Improved Holdout gồm 38 case. |
| `holdout_ground_truth_improved.csv` | Ground Truth Improved Holdout gồm 38 case. |

### Thuộc tính phép chia — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Seed phép chia | `210` |
| Số case | `38` |
| Trùng Pilot | `0` |
| Trùng Development | `0` |
| Vai trò đánh giá | Đánh giá cuối được bảo vệ |

### Quy tắc bảo vệ — Tiếng Việt

- Không dùng case Holdout để chỉnh prompt.
- Không thêm rule dựa trên mismatch Holdout.
- Không chạy API test từng case trên Holdout.
- Không chạy một phần Holdout.
- Không chạy lại cùng Holdout để cải thiện metric.
- Holdout Ground Truth chỉ được dùng khi tính metric cuối.

### Ý nghĩa đánh giá cuối — Tiếng Việt

Chỉ số Holdout là kết quả nghiên cứu chính thức cuối cùng. Dù có đạt ngưỡng
Cohen's Kappa đã xác định trước hay không, kết quả Holdout phải được giữ nguyên
và không được tuning hậu nghiệm trên các case này.
