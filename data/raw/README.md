# Raw Source and Pilot Dataset / Dữ liệu nguồn và Pilot Raw

## English

### Purpose — English

The `Data/Raw` directory stores original Raw Mojira source reports and the
official Raw Pilot dataset.

### Directory contents — English

| File or directory | Phase | Description |
| --- | --- | --- |
| `RAW` | Full source | Original Raw JSON reports used to generate `Data/Full/All/Raw/full_sample_raw.csv`. |
| `pilot_sample_raw.csv` | Official Pilot | Raw Pilot sample containing 26 cases. |
| `pilot_ground_truth_raw.csv` | Official Pilot | Final Ground Truth for the 26 Raw Pilot cases. |
| `pilot_annotation_raw_author1.csv` | Pilot annotation | Raw Pilot annotations from Author 1. |
| `pilot_annotation_raw_author2.csv` | Pilot annotation | Raw Pilot annotations from Author 2. |
| `kappa_scores_raw.csv` | Pilot annotation | Inter-annotator agreement results for Raw Pilot. |
| `README.md` | Documentation | Documentation for this directory. |

### Role in the experiment — English

This directory supports two separate roles:

1. source JSON data for Full Raw sample generation;
2. official Raw Pilot input and Ground Truth.

The Pilot files are also reused as input for Full Pilot Validation, while its
results are written to `Results/Full/Pilot_Validation/Raw`.

### Important rules — English

- Do not delete `RAW`; it is required to regenerate the Full Raw sample.
- Do not overwrite official Pilot files with Pilot Validation output.
- Keep annotation and Kappa files as evidence of the manual labeling process.
- Full Development and Holdout data belong under `Data/Full`, not here.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Raw` lưu báo cáo Mojira Raw gốc và bộ dữ liệu Pilot Raw chính thức.

### Nội dung thư mục — Tiếng Việt

| File hoặc thư mục | Giai đoạn | Mô tả |
| --- | --- | --- |
| `RAW` | Nguồn Full | Báo cáo Raw JSON gốc dùng để tạo `Data/Full/All/Raw/full_sample_raw.csv`. |
| `pilot_sample_raw.csv` | Pilot chính thức | Mẫu Pilot Raw gồm 26 case. |
| `pilot_ground_truth_raw.csv` | Pilot chính thức | Ground Truth cuối cho 26 case Pilot Raw. |
| `pilot_annotation_raw_author1.csv` | Gán nhãn Pilot | Kết quả gán nhãn Pilot Raw của Author 1. |
| `pilot_annotation_raw_author2.csv` | Gán nhãn Pilot | Kết quả gán nhãn Pilot Raw của Author 2. |
| `kappa_scores_raw.csv` | Gán nhãn Pilot | Kết quả đồng thuận giữa hai người gán nhãn cho Pilot Raw. |
| `README.md` | Tài liệu | Tài liệu mô tả thư mục này. |

### Vai trò trong thí nghiệm — Tiếng Việt

Thư mục này có hai vai trò riêng:

1. lưu JSON nguồn để tạo Full Raw sample;
2. lưu input và Ground Truth Pilot Raw chính thức.

Các file Pilot cũng được sử dụng lại làm input cho Full Pilot Validation, trong
khi kết quả được ghi vào `Results/Full/Pilot_Validation/Raw`.

### Quy tắc quan trọng — Tiếng Việt

- Không xóa `RAW` vì cần thiết để tạo lại Full Raw sample.
- Không ghi đè file Pilot chính thức bằng output Pilot Validation.
- Giữ file annotation và Kappa làm bằng chứng của quy trình gán nhãn thủ công.
- Dữ liệu Full Development và Holdout phải nằm trong `Data/Full`, không nằm ở đây.
