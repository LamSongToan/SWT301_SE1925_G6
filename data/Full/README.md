# Full Dataset Overview / Tổng quan dữ liệu Full

## English

### Purpose — English

The `Data/Full` directory stores the complete 139-case Full dataset and the
deterministic split used for Development and protected Holdout evaluation.

### Directory structure — English

| Directory | Role | Cases |
| --- | --- | ---: |
| `All` | Complete Raw and Improved Full datasets before splitting. | `139` |
| `Development` | Cases used for prompt development and Full-only rule calibration. | `75` |
| `Holdout` | Protected cases used only for the final evaluation. | `38` |
| `Split` | Issue-key assignments and split summary metadata. | `139` assignments |

### Final split — English

The split uses seed `210`.

| Subset | Cases | Use |
| --- | ---: | --- |
| Pilot | `26` | Stored in `Data/Raw` and `Data/Improved`; used for official Pilot and Pilot Validation. |
| Development | `75` | Used for Full prompt and rule development. |
| Holdout | `38` | Used once for the final protected evaluation. |
| Total | `139` | Complete Full dataset. |

### Relationship between directories — English

- `All` is the complete 139-case source set.
- `Development` and `Holdout` are generated from `All`.
- Pilot cases are not duplicated under `Data/Full`; their issue keys are recorded
  in `Data/Full/Split/pilot_issue_keys.csv`.
- Raw and Improved subsets must contain matching issue keys for each split.

### Important rules — English

- Keep `All` as the reproducible source for the split.
- Use only `Development` for Full prompt tuning and rule calibration.
- Do not inspect or tune on `Holdout` before the final evaluation.
- Do not recreate the split after the Holdout evaluation has begun.
- Keep all files in `Split` to document the deterministic assignment.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Full` lưu bộ dữ liệu Full đầy đủ 139 case và phép chia cố định dùng
cho Development cùng đánh giá Holdout được bảo vệ.

### Cấu trúc thư mục — Tiếng Việt

| Thư mục | Vai trò | Số case |
| --- | --- | ---: |
| `All` | Toàn bộ dữ liệu Full Raw và Improved trước khi chia. | `139` |
| `Development` | Dùng để phát triển prompt và hiệu chỉnh Full-only rule. | `75` |
| `Holdout` | Tập được bảo vệ, chỉ dùng cho đánh giá cuối. | `38` |
| `Split` | Danh sách issue key và metadata tổng hợp phép chia. | `139` phân công |

### Phép chia cuối — Tiếng Việt

Phép chia sử dụng seed `210`.

| Tập con | Số case | Mục đích sử dụng |
| --- | ---: | --- |
| Pilot | `26` | Lưu trong `Data/Raw` và `Data/Improved`; dùng cho Pilot chính thức và Pilot Validation. |
| Development | `75` | Dùng để phát triển prompt và rule Full. |
| Holdout | `38` | Chỉ chạy một lần cho đánh giá cuối được bảo vệ. |
| Tổng cộng | `139` | Toàn bộ bộ dữ liệu Full. |

### Quan hệ giữa các thư mục — Tiếng Việt

- `All` là bộ nguồn hoàn chỉnh 139 case.
- `Development` và `Holdout` được sinh từ `All`.
- Case Pilot không được sao chép vào `Data/Full`; issue key của chúng được ghi
  trong `Data/Full/Split/pilot_issue_keys.csv`.
- Tập Raw và Improved trong mỗi split phải có cùng issue key.

### Quy tắc quan trọng — Tiếng Việt

- Giữ `All` làm nguồn tái lập của phép chia.
- Chỉ dùng `Development` để chỉnh prompt và hiệu chỉnh rule Full.
- Không xem hoặc tuning trên `Holdout` trước đánh giá cuối.
- Không tạo lại phép chia sau khi đã bắt đầu đánh giá Holdout.
- Giữ toàn bộ file trong `Split` để chứng minh phép chia cố định.
