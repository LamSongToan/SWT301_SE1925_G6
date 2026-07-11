# Improved Source and Pilot Dataset / Dữ liệu nguồn và Pilot Improved

## English

### Purpose — English

The `Data/Improved` directory stores Improved Mojira source reports and the
official Improved Pilot dataset.

### Directory contents — English

| File or directory | Phase | Description |
| --- | --- | --- |
| `IMPROVED` | Full source | Improved JSON reports used to generate `Data/Full/All/Improved/full_sample_improved.csv`. |
| `pilot_sample_improved.csv` | Official Pilot | Improved Pilot sample containing 26 cases. |
| `pilot_ground_truth_improved.csv` | Official Pilot | Final Ground Truth for the 26 Improved Pilot cases. |
| `pilot_annotation_improved_author1.csv` | Pilot annotation | Improved Pilot annotations from Author 1. |
| `pilot_annotation_improved_author2.csv` | Pilot annotation | Improved Pilot annotations from Author 2. |
| `kappa_scores_improved.csv` | Pilot annotation | Inter-annotator agreement results for Improved Pilot. |
| `README.md` | Documentation | Documentation for this directory. |

### Role in the experiment — English

This directory supports two separate roles:

1. source JSON data for Full Improved sample generation;
2. official Improved Pilot input and Ground Truth.

The Pilot files are also reused as input for Full Pilot Validation, while its
results are written to `Results/Full/Pilot_Validation/Improved`.

### Important rules — English

- Do not delete `IMPROVED`; it is required to regenerate the Full Improved sample.
- Do not overwrite official Pilot files with Pilot Validation output.
- Keep annotation and Kappa files as evidence of the manual labeling process.
- Full Development and Holdout data belong under `Data/Full`, not here.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Improved` lưu báo cáo Mojira Improved nguồn và bộ dữ liệu Pilot
Improved chính thức.

### Nội dung thư mục — Tiếng Việt

| File hoặc thư mục | Giai đoạn | Mô tả |
| --- | --- | --- |
| `IMPROVED` | Nguồn Full | Báo cáo Improved JSON dùng để tạo `Data/Full/All/Improved/full_sample_improved.csv`. |
| `pilot_sample_improved.csv` | Pilot chính thức | Mẫu Pilot Improved gồm 26 case. |
| `pilot_ground_truth_improved.csv` | Pilot chính thức | Ground Truth cuối cho 26 case Pilot Improved. |
| `pilot_annotation_improved_author1.csv` | Gán nhãn Pilot | Kết quả gán nhãn Pilot Improved của Author 1. |
| `pilot_annotation_improved_author2.csv` | Gán nhãn Pilot | Kết quả gán nhãn Pilot Improved của Author 2. |
| `kappa_scores_improved.csv` | Gán nhãn Pilot | Kết quả đồng thuận giữa hai người gán nhãn cho Pilot Improved. |
| `README.md` | Tài liệu | Tài liệu mô tả thư mục này. |

### Vai trò trong thí nghiệm — Tiếng Việt

Thư mục này có hai vai trò riêng:

1. lưu JSON nguồn để tạo Full Improved sample;
2. lưu input và Ground Truth Pilot Improved chính thức.

Các file Pilot cũng được sử dụng lại làm input cho Full Pilot Validation, trong
khi kết quả được ghi vào `Results/Full/Pilot_Validation/Improved`.

### Quy tắc quan trọng — Tiếng Việt

- Không xóa `IMPROVED` vì cần thiết để tạo lại Full Improved sample.
- Không ghi đè file Pilot chính thức bằng output Pilot Validation.
- Giữ file annotation và Kappa làm bằng chứng của quy trình gán nhãn thủ công.
- Dữ liệu Full Development và Holdout phải nằm trong `Data/Full`, không nằm ở đây.
