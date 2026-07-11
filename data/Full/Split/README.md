# Full Split Metadata / Metadata phép chia Full

## English

### Purpose — English

The `Data/Full/Split` directory records the deterministic assignment of all 139
Full issue keys into Pilot, Development, and Holdout subsets.

### Split configuration — English

| Item | Value |
| --- | --- |
| Split seed | `210` |
| Total cases | `139` |
| Pilot cases | `26` |
| Development cases | `75` |
| Holdout cases | `38` |
| Stratification | Joint Raw–Improved Ground Truth label pair |

### Directory contents — English

| File | Description |
| --- | --- |
| `pilot_issue_keys.csv` | List of the 26 issue keys assigned to Pilot. |
| `development_issue_keys.csv` | List of the 75 issue keys assigned to Development. |
| `holdout_issue_keys.csv` | List of the 38 issue keys assigned to Holdout. |
| `split_assignment.csv` | Complete issue-level assignment for all 139 cases. |
| `split_summary.csv` | Split counts and joint Raw–Improved label-stratum summary. |

### Required integrity conditions — English

- Pilot, Development, and Holdout issue-key sets must not overlap.
- Their union must contain exactly 139 unique issue keys.
- Raw and Improved files must use the same issue-key assignment.
- Development must contain exactly 75 cases.
- Holdout must contain exactly 38 cases.
- The split seed must remain `210`.

### Important rules — English

- Do not edit issue-key manifests manually.
- Do not regenerate the split after Holdout evaluation has started.
- Keep these files as reproducibility evidence.
- Issue-key manifests identify membership only and should not be treated as
  prediction or metric output.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Data/Full/Split` ghi lại phép phân công cố định của toàn bộ 139 issue key
Full vào các tập Pilot, Development và Holdout.

### Cấu hình phép chia — Tiếng Việt

| Hạng mục | Giá trị |
| --- | --- |
| Seed phép chia | `210` |
| Tổng số case | `139` |
| Số case Pilot | `26` |
| Số case Development | `75` |
| Số case Holdout | `38` |
| Phân tầng | Cặp nhãn Ground Truth Raw–Improved |

### Nội dung thư mục — Tiếng Việt

| File | Mô tả |
| --- | --- |
| `pilot_issue_keys.csv` | Danh sách 26 issue key được phân vào Pilot. |
| `development_issue_keys.csv` | Danh sách 75 issue key được phân vào Development. |
| `holdout_issue_keys.csv` | Danh sách 38 issue key được phân vào Holdout. |
| `split_assignment.csv` | Phân công đầy đủ ở cấp issue cho toàn bộ 139 case. |
| `split_summary.csv` | Tổng hợp số lượng và các tầng nhãn Raw–Improved của phép chia. |

### Điều kiện toàn vẹn bắt buộc — Tiếng Việt

- Tập issue key Pilot, Development và Holdout không được trùng nhau.
- Hợp của ba tập phải có đúng 139 issue key duy nhất.
- File Raw và Improved phải sử dụng cùng phân công issue key.
- Development phải có đúng 75 case.
- Holdout phải có đúng 38 case.
- Seed phép chia phải giữ nguyên là `210`.

### Quy tắc quan trọng — Tiếng Việt

- Không sửa thủ công các file danh sách issue key.
- Không tạo lại phép chia sau khi đã bắt đầu đánh giá Holdout.
- Giữ các file này làm bằng chứng tái lập.
- File issue key chỉ thể hiện thành viên của tập, không phải output dự đoán hoặc
  metric.
