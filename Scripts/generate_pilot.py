"""
generate_pilot.py -- Tao pilot files cho RT-SWT-004

Input:
  RAW/                    -- 139 raw bug report JSON
  IMPROVED/               -- 139 improved bug report JSON (co S2R, OB, EB, Env)
  annotations/
    Author 1 Responses.csv
    Author 2 Responses.csv
    Final Results.csv

Output (result/):
  pilot_sample_raw.csv                  -- 26 issues tu RAW
  pilot_sample_improved.csv             -- 26 issues tu IMPROVED (co them S2R, OB, EB, Env)
  pilot_ground_truth_raw.csv            -- ground truth (Final Results) cho raw
  pilot_ground_truth_improved.csv       -- ground truth (Final Results) cho improved
  pilot_annotation_raw_author1.csv      -- annotation Author 1 cho 26 raw issues
  pilot_annotation_raw_author2.csv      -- annotation Author 2 cho 26 raw issues
  pilot_annotation_improved_author1.csv -- annotation Author 1 cho 26 improved issues
  pilot_annotation_improved_author2.csv -- annotation Author 2 cho 26 improved issues

Chay: python scripts/generate_pilot.py  (tu DG_deliverables/)
"""

import csv, json, random
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent   # scripts/
BASE         = SCRIPT_DIR.parent                  # repo root
RAW_DIR      = BASE / "data" / "raw" / "RAW"
IMPROVED_DIR = BASE / "data" / "raw" / "IMPROVED"
ANNOT_DIR    = BASE / "data" / "annotations"
FINAL_CSV    = ANNOT_DIR / "Final Results.csv"
A1_CSV       = ANNOT_DIR / "Author 1 Responses.csv"
A2_CSV       = ANNOT_DIR / "Author 2 Responses.csv"
OUT_DIR      = BASE / "data"

# ============================================================
# CONFIG -- chinh sua o day truoc khi chay
# ============================================================
RANDOM_SEED = 210  # seed de random 26 issues (doi so nay de ra bo issues khac)
N_SAMPLE    = 26   # so luong issues can sample
# ============================================================

RAW_FIELDS = ["Issue Key","Summary","Type","Affects Version/s","Labels",
              "Confirmation Status","Category","Resolution","Fix Version/s","Description"]

IMP_FIELDS = ["Issue Key","Summary","Type","Affects Version/s","Labels",
              "Confirmation Status","Category","Resolution","Fix Version/s","Description",
              "Steps to Reproduce","Observed Behavior","Expected Behavior","Environment"]

def to_str(val):
    if isinstance(val, list): return "; ".join(str(v) for v in val) if val else "None"
    return str(val) if val else "None"

def load_annot_full(path, tag="Raw"):
    """Load full annotation rows keyed by issue key."""
    header, rows = None, {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or not row[0].strip(): continue
            bid = row[0].strip()
            if not bid.endswith(" " + tag): continue
            rows[bid[:-len(" " + tag)].strip()] = row
    return header, rows

# --- Sample ---
all_keys = sorted(f.stem for f in RAW_DIR.glob("*.json"))
random.seed(RANDOM_SEED)
sampled = random.sample(all_keys, N_SAMPLE)
OUT_DIR.mkdir(exist_ok=True)
print(f"Sampled {len(sampled)} issues (seed={RANDOM_SEED})")

# --- File 1: pilot_sample_raw.csv ---
raw_records = []
for key in sampled:
    with open(RAW_DIR / f"{key}.json", encoding="utf-8") as f:
        d = json.load(f)
    raw_records.append({
        "Issue Key":           key,
        "Summary":             d.get("summary","") or "",
        "Type":                "Bug",
        "Affects Version/s":   to_str(d.get("affected_versions",[])),
        "Labels":              to_str(d.get("labels",[])),
        "Confirmation Status": d.get("confirmation_status","") or "Unconfirmed",
        "Category":            d.get("category","") or "(Unassigned)",
        "Resolution":          d.get("resolution","") or "None",
        "Fix Version/s":       to_str(d.get("fix_versions",[])),
        "Description":         d.get("description","") or "",
    })
with open(OUT_DIR / "pilot_sample_raw.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=RAW_FIELDS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(raw_records)
print("pilot_sample_raw.csv              -> OK")

# --- File 2: pilot_sample_improved.csv ---
imp_records = []
for key in sampled:
    with open(IMPROVED_DIR / f"{key}_improved.json", encoding="utf-8") as f:
        d = json.load(f)
    versions = d.get("affected_versions",[])
    if isinstance(versions, str): versions = [versions]
    desc_parts = [d.get("description","") or ""]
    for sec in ["Steps to Reproduce","Observed Behavior","Expected Behavior","Environment"]:
        content = (d.get(sec,"") or "").strip()
        if content: desc_parts.append(f"\n[{sec}]\n{content}")
    imp_records.append({
        "Issue Key":           key,
        "Summary":             d.get("summary","") or "",
        "Type":                "Bug",
        "Affects Version/s":   to_str(versions),
        "Labels":              to_str(d.get("labels",[])),
        "Confirmation Status": "Unconfirmed",
        "Category":            "(Unassigned)",
        "Resolution":          d.get("resolution","") or "None",
        "Fix Version/s":       "None",
        "Description":         "\n".join(desc_parts).strip(),
        "Steps to Reproduce":  (d.get("Steps to Reproduce","") or "").strip(),
        "Observed Behavior":   (d.get("Observed Behavior","") or "").strip(),
        "Expected Behavior":   (d.get("Expected Behavior","") or "").strip(),
        "Environment":         (d.get("Environment","") or "").strip(),
    })
with open(OUT_DIR / "pilot_sample_improved.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=IMP_FIELDS, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(imp_records)
print("pilot_sample_improved.csv         -> OK")

# --- File 3+4: pilot_ground_truth_raw/improved.csv ---
for fname, tag in [("pilot_ground_truth_raw.csv", "Raw"), ("pilot_ground_truth_improved.csv", "Improved")]:
    h, data = load_annot_full(FINAL_CSV, tag)
    with open(OUT_DIR / fname, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        if h: w.writerow(h)
        for key in sampled:
            row = data.get(key)
            w.writerow(row if row else [key + " " + tag] + [""] * ((len(h)-1) if h else 9))
    print(f"{fname:<42} -> OK")

# --- File 5-8: pilot_annotation_raw/improved_author1/2.csv ---
for fname, src_csv, tag in [
    ("pilot_annotation_raw_author1.csv",      A1_CSV, "Raw"),
    ("pilot_annotation_raw_author2.csv",      A2_CSV, "Raw"),
    ("pilot_annotation_improved_author1.csv", A1_CSV, "Improved"),
    ("pilot_annotation_improved_author2.csv", A2_CSV, "Improved"),
]:
    h, data = load_annot_full(src_csv, tag)
    with open(OUT_DIR / fname, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        if h: w.writerow(h)
        for key in sampled:
            row = data.get(key)
            w.writerow(row if row else [key + " " + tag] + [""] * ((len(h)-1) if h else 9))
    print(f"{fname:<42} -> OK")

print("\nDone.")
