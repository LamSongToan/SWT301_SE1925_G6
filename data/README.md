# Data Directory Overview / Tổng quan thư mục Data

## English

### Purpose — English

The `Data` directory stores all source data, human annotations, Pilot datasets,
Full datasets, split metadata, and supporting presentation materials used in the
Bug Report Quality Assessment with LLM project.

### Directory structure — English

| Directory | Phase | Purpose |
| --- | --- | --- |
| `Annotations` | Shared source | Human annotation responses, the final consolidated labels, and the evaluation rubric. |
| `Raw` | Source + Pilot | Original Raw JSON reports and the official Raw Pilot dataset. |
| `Improved` | Source + Pilot | Improved JSON reports and the official Improved Pilot dataset. |
| `Full` | Full experiment | Complete 139-case dataset, Development subset, protected Holdout subset, and split metadata. |
| `Presentation` | Supporting material | Presentation files and supporting materials not used directly as experiment input. |

### Phase classification — English

| Phase | Location | Number of cases | Main use |
| --- | --- | ---: | --- |
| Official Pilot Raw | `Data/Raw` | `26` | Initial Raw calibration and official Pilot evaluation. |
| Official Pilot Improved | `Data/Improved` | `26` | Initial Improved calibration and official Pilot evaluation. |
| Full All | `Data/Full/All` | `139` | Complete Raw and Improved Full datasets. |
| Full Development | `Data/Full/Development` | `75` | Prompt development, rule calibration, and mismatch analysis. |
| Full Holdout | `Data/Full/Holdout` | `38` | Final protected evaluation only. |
| Full Split | `Data/Full/Split` | `139` assignments | Records the Pilot, Development, and Holdout assignments. |

### Data flow — English

1. Human annotations are stored in `Data/Annotations`.
2. Original Raw and Improved JSON reports are stored in `Data/Raw/RAW` and
   `Data/Improved/IMPROVED`.
3. Official Pilot datasets are stored in `Data/Raw` and `Data/Improved`.
4. The complete 139-case Full datasets are generated in `Data/Full/All`.
5. The 26 Pilot issue keys are excluded from Full development.
6. The remaining 113 cases are divided into 75 Development cases and 38
   protected Holdout cases.
7. The final assignments are recorded in `Data/Full/Split`.

### Important rules — English

- Do not delete `Data/Raw` or `Data/Improved`; they contain both source JSON data
  and official Pilot files.
- Do not use `Data/Full/Holdout` for prompt tuning or rule development.
- Do not regenerate the split after Holdout evaluation has started.
- Keep `Data/Full/All` and `Data/Full/Split` for reproducibility.
- The final research conclusion must be based on the protected Holdout results.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data` lưu toàn bộ dữ liệu nguồn, dữ liệu gán nhãn thủ công, dữ liệu
Pilot, dữ liệu Full, metadata của phép chia và tài liệu trình bày hỗ trợ của dự
án Bug Report Quality Assessment with LLM.

### Cấu trúc thư mục — Tiếng Việt

| Thư mục | Giai đoạn | Mục đích |
| --- | --- | --- |
| `Annotations` | Nguồn dùng chung | Kết quả gán nhãn thủ công, nhãn tổng hợp cuối và rubric đánh giá. |
| `Raw` | Dữ liệu nguồn + Pilot | Báo cáo Raw JSON gốc và bộ Pilot Raw chính thức. |
| `Improved` | Dữ liệu nguồn + Pilot | Báo cáo Improved JSON và bộ Pilot Improved chính thức. |
| `Full` | Thí nghiệm Full | Bộ dữ liệu 139 case, tập Development, tập Holdout được bảo vệ và metadata phép chia. |
| `Presentation` | Tài liệu hỗ trợ | File trình bày và tài liệu hỗ trợ, không dùng trực tiếp làm input thí nghiệm. |

### Phân loại theo giai đoạn — Tiếng Việt

| Giai đoạn | Vị trí | Số case | Mục đích chính |
| --- | --- | ---: | --- |
| Pilot Raw chính thức | `Data/Raw` | `26` | Hiệu chỉnh ban đầu và đánh giá Pilot Raw chính thức. |
| Pilot Improved chính thức | `Data/Improved` | `26` | Hiệu chỉnh ban đầu và đánh giá Pilot Improved chính thức. |
| Full All | `Data/Full/All` | `139` | Toàn bộ dữ liệu Full Raw và Improved. |
| Full Development | `Data/Full/Development` | `75` | Phát triển prompt, hiệu chỉnh rule và phân tích mismatch. |
| Full Holdout | `Data/Full/Holdout` | `38` | Chỉ dùng cho đánh giá cuối được bảo vệ. |
| Full Split | `Data/Full/Split` | `139` phân công | Ghi lại phân công Pilot, Development và Holdout. |

### Luồng dữ liệu — Tiếng Việt

1. Dữ liệu gán nhãn thủ công được lưu trong `Data/Annotations`.
2. Báo cáo JSON Raw và Improved gốc được lưu trong `Data/Raw/RAW` và
   `Data/Improved/IMPROVED`.
3. Dữ liệu Pilot chính thức được lưu trong `Data/Raw` và `Data/Improved`.
4. Bộ dữ liệu Full đầy đủ 139 case được tạo trong `Data/Full/All`.
5. 26 issue key Pilot được loại khỏi tập dùng để phát triển Full.
6. 113 case còn lại được chia thành 75 case Development và 38 case Holdout được
   bảo vệ.
7. Kết quả phép chia cuối được ghi trong `Data/Full/Split`.

### Quy tắc quan trọng — Tiếng Việt

- Không xóa `Data/Raw` hoặc `Data/Improved` vì hai thư mục này chứa cả JSON nguồn
  và file Pilot chính thức.
- Không dùng `Data/Full/Holdout` để chỉnh prompt hoặc phát triển rule.
- Không tạo lại phép chia sau khi đã bắt đầu đánh giá Holdout.
- Giữ `Data/Full/All` và `Data/Full/Split` để bảo đảm khả năng tái lập.
- Kết luận nghiên cứu cuối phải dựa trên kết quả Holdout được bảo vệ.
