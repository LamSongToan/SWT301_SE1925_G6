# Full All Dataset / Bộ dữ liệu Full All

## English

### Purpose — English

The `Data/Full/All` directory stores the complete 139-case Raw and Improved Full
datasets before Development and Holdout subsets are created.

### Directory contents — English

#### `Raw` directory — English

| File | Description |
| --- | --- |
| `full_sample_raw.csv` | Complete Raw sample containing 139 Mojira bug reports. |
| `full_ground_truth_raw.csv` | Complete Raw Ground Truth containing 139 labels and annotation fields. |

#### `Improved` directory — English

| File | Description |
| --- | --- |
| `full_sample_improved.csv` | Complete Improved sample containing 139 Mojira bug reports. |
| `full_ground_truth_improved.csv` | Complete Improved Ground Truth containing 139 labels and annotation fields. |

### Data origin — English

- Ground Truth files are generated from `Data/Annotations/Final Results.csv`.
- Sample files are generated from `Data/Raw/RAW` and
  `Data/Improved/IMPROVED`.
- Raw and Improved Full files must contain the same 139 normalized issue keys.

### Usage — English

This directory is used to:

- verify all 139 cases;
- reproduce Development and Holdout subsets;
- check Raw–Improved issue-key alignment;
- preserve the source order of the Full dataset.

### Important rules — English

- Do not manually edit generated rows unless the source data is corrected first.
- Keep all four files for reproducibility.
- Do not use `All` directly as the final evaluation set after the split has been
  established.
- Do not change issue-key order without regenerating and validating the split.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Full/All` lưu toàn bộ dữ liệu Full Raw và Improved gồm 139 case
trước khi tạo các tập Development và Holdout.

### Nội dung thư mục — Tiếng Việt

#### Thư mục `Raw` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `full_sample_raw.csv` | Mẫu Raw đầy đủ gồm 139 báo cáo lỗi Mojira. |
| `full_ground_truth_raw.csv` | Ground Truth Raw đầy đủ gồm 139 nhãn và các trường gán nhãn. |

#### Thư mục `Improved` — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `full_sample_improved.csv` | Mẫu Improved đầy đủ gồm 139 báo cáo lỗi Mojira. |
| `full_ground_truth_improved.csv` | Ground Truth Improved đầy đủ gồm 139 nhãn và các trường gán nhãn. |

### Nguồn dữ liệu — Tiếng Việt

- File Ground Truth được tạo từ `Data/Annotations/Final Results.csv`.
- File sample được tạo từ `Data/Raw/RAW` và `Data/Improved/IMPROVED`.
- Các file Full Raw và Improved phải có cùng 139 issue key đã chuẩn hóa.

### Mục đích sử dụng — Tiếng Việt

Thư mục này được dùng để:

- kiểm tra toàn bộ 139 case;
- tái tạo các tập Development và Holdout;
- kiểm tra sự khớp issue key giữa Raw và Improved;
- giữ nguyên thứ tự nguồn của bộ dữ liệu Full.

### Quy tắc quan trọng — Tiếng Việt

- Không sửa thủ công các dòng đã sinh nếu chưa sửa dữ liệu nguồn trước.
- Giữ cả bốn file để bảo đảm khả năng tái lập.
- Không dùng `All` trực tiếp làm tập đánh giá cuối sau khi phép chia đã được chốt.
- Không thay đổi thứ tự issue key nếu chưa tạo lại và kiểm tra phép chia.
