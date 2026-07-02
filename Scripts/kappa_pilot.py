"""
kappa_pilot.py -- Tinh Cohen's Kappa cho pilot (raw vs improved)
Chay: python scripts/kappa_pilot.py  (tu DG_deliverables/, sau generate_pilot.py)
Output: result/kappa_scores_raw.csv
        result/kappa_scores_improved.csv

"""

import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE       = SCRIPT_DIR.parent
ANNOT_DIR  = BASE / "data" / "annotations"
RESULT_DIR = BASE / "results"

A1_CSV = ANNOT_DIR / "Author 1 Responses.csv"
A2_CSV = ANNOT_DIR / "Author 2 Responses.csv"
RAW_GT = BASE / "data" / "pilot_ground_truth_raw.csv"
IMP_GT = BASE / "data" / "pilot_ground_truth_improved.csv"

# ---------- helpers ----------

def score(row):
    s2r = row.get("s2r",""); irr = row.get("irr","")
    ob, obl = row.get("ob",""), row.get("obl","")
    eb, ebl = row.get("eb",""), row.get("ebl","")
    if s2r == "Executable":
        return 5 if (ob=="Present" and obl=="Sufficient" and eb=="Present" and ebl=="Accurate") else 4
    if irr == "Wrong Information": return 1
    if ob=="Present" and eb=="Present": return 3
    if ob=="Present" or eb=="Present": return 2
    return 1

def load_annot(path, tag="Raw"):
    data = {}
    suffix = " " + tag
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip().endswith(suffix): continue
            key = row[0].strip()[:-len(suffix)].strip()
            def g(i, r=row): return r[i].strip() if i < len(r) else ""
            data[key] = {"s2r": g(1), "irr": g(2), "ob": g(4), "obl": g(5), "eb": g(7), "ebl": g(8)}
    return data

def read_gt_keys(path, tag="Raw"):
    keys = []
    suffix = " " + tag
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip().endswith(suffix): continue
            keys.append(row[0].strip()[:-len(suffix)].strip())
    return keys

def cohen_kappa(s_a, s_b, keys):
    n = len(keys)
    if n == 0: return 0.0
    po = sum(1 for k in keys if s_a.get(k) == s_b.get(k)) / n
    pe = sum((sum(1 for k in keys if s_a.get(k)==c)/n) *
             (sum(1 for k in keys if s_b.get(k)==c)/n) for c in range(1,6))
    return round((po - pe) / (1 - pe) if pe < 1 else 1.0, 4)

# ---------- main ----------

for label, gt_path, out_name, tag in [
    ("raw",      RAW_GT, "kappa_scores_raw.csv",      "Raw"),
    ("improved", IMP_GT, "kappa_scores_improved.csv", "Improved"),
]:
    a1 = load_annot(A1_CSV, tag)
    a2 = load_annot(A2_CSV, tag)
    keys = read_gt_keys(gt_path, tag)
    rows = []
    for key in keys:
        s1 = score(a1[key]) if key in a1 else ""
        s2 = score(a2[key]) if key in a2 else ""
        rows.append({"issue_key": key, "author1_score": s1, "author2_score": s2,
                     "agree": int(s1==s2) if s1!="" and s2!="" else ""})

    valid_keys = [r["issue_key"] for r in rows if r["agree"] != ""]
    s_a1 = {r["issue_key"]: r["author1_score"] for r in rows if r["agree"] != ""}
    s_a2 = {r["issue_key"]: r["author2_score"] for r in rows if r["agree"] != ""}
    k = cohen_kappa(s_a1, s_a2, valid_keys)
    n = len(valid_keys)
    agree = sum(r["agree"] for r in rows if r["agree"] != "")

    out = RESULT_DIR / out_name
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["issue_key","author1_score","author2_score","agree"])
        w.writeheader()
        w.writerows(rows)
        f.write(f"\nN,{n},,\n")
        f.write(f"Cohen Kappa,{k},,\n")
        f.write(f"Agreement,{agree}/{n},,\n")
    print(f"{out_name}: kappa={k}  agree={agree}/{n}")

print("Done.")
