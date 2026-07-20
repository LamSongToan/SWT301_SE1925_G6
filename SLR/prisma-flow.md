# PRISMA Flow – Bug Report Quality Assessment with LLM

```
[Records từ database searching (N = 249 )]  ← Tổng từ search-log.md
      ↓
[Sau khi xóa duplicate (N = 197 )]  ← = dòng trong 01_all_records.csv
      ↓
┌────────────────────────────────────────────────────────┐
│ Screened title + abstract (N = 197 )                   │
│  └── Excluded (N = 168 ):                              │
│                                                        │
└────────────────────────────────────────────────────────┘
      ↓  29 papers pass  ← = INCLUDE + Unsure trong 02_after_screening_v1
┌────────────────────────────────────────────────────────┐
│ Full-text assessed (N = 29 )                            │
│  └── Excluded (N = 16 ):                                │
│                                                        │
└────────────────────────────────────────────────────────┘
      ↓
[Final included (N = 13 )]  ← = Include trong 03_final_included.csv
```