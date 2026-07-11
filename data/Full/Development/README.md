# Development Dataset / Bộ dữ liệu Development

## English

### Purpose — English

The `Data/Full/Development` directory stores 75 non-Pilot cases used to develop
and calibrate the Full experiment configuration.

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `development_sample_raw.csv` | Raw Development sample containing 75 cases. |
| `development_ground_truth_raw.csv` | Raw Development Ground Truth containing 75 cases. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `development_sample_improved.csv` | Improved Development sample containing 75 cases. |
| `development_ground_truth_improved.csv` | Improved Development Ground Truth containing 75 cases. |

### Split properties — English

| Item | Value |
| --- | --- |
| Split seed | `210` |
| Number of cases | `75` |
| Pilot overlap | `0` |
| Holdout overlap | `0` |
| Raw–Improved issue-key alignment | Required |

### Allowed usage — English

Development data may be used for:

- prompt refinement;
- Full-only consistency-rule calibration;
- mismatch analysis;
- Development metric calculation;
- comparison between Raw and Improved performance.

### Important rules — English

- Development is the only Full subset allowed for tuning.
- Changes derived from Development must be validated on Pilot Validation before
  Holdout.
- Development metrics are not the final research result.
- Do not move cases between Development and Holdout after the split is frozen.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Full/Development` lưu 75 case không thuộc Pilot, được dùng để phát
triển và hiệu chỉnh cấu hình thí nghiệm Full.

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `development_sample_raw.csv` | Mẫu Raw Development gồm 75 case. |
| `development_ground_truth_raw.csv` | Ground Truth Raw Development gồm 75 case. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `development_sample_improved.csv` | Mẫu Improved Development gồm 75 case. |
| `development_ground_truth_improved.csv` | Ground Truth Improved Development gồm 75 case. |

### Thuộc tính phép chia — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Seed phép chia | `210` |
| Số case | `75` |
| Trùng Pilot | `0` |
| Trùng Holdout | `0` |
| Khớp issue key Raw–Improved | Bắt buộc |

### Mục đích được phép — Tiếng Việt

Có thể sử dụng dữ liệu Development để:

- chỉnh prompt;
- hiệu chỉnh consistency rule chỉ dành cho Full;
- phân tích mismatch;
- tính metric Development;
- so sánh hiệu suất Raw và Improved.

### Quy tắc quan trọng — Tiếng Việt

- Development là tập Full duy nhất được phép dùng để tuning.
- Thay đổi dựa trên Development phải được kiểm tra bằng Pilot Validation trước
  khi chạy Holdout.
- Chỉ số Development không phải kết quả nghiên cứu cuối.
- Không chuyển case giữa Development và Holdout sau khi phép chia đã đóng băng.
