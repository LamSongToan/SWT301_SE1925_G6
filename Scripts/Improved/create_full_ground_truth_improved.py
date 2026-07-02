from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parents[2]

FINAL_RESULTS_FILE = BASE_DIR / "Data" / "Annotations" / "Final Results.csv"
OUTPUT_FILE = BASE_DIR / "Data" / "Improved" / "full_ground_truth_improved.csv"


def is_empty_row(row):
    return all(not cell.strip() for cell in row)


def main():
    print("Creating full_ground_truth_improved.csv...")
    print("-" * 60)

    if not FINAL_RESULTS_FILE.exists():
        raise FileNotFoundError(f"Cannot find file: {FINAL_RESULTS_FILE}")

    with FINAL_RESULTS_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if not rows:
        raise ValueError("Final Results.csv is empty.")

    header = rows[0]

    useful_column_indexes = [
        index for index, column_name in enumerate(header)
        if column_name.strip() and not column_name.strip().startswith("Unnamed")
    ]

    clean_header = [header[index] for index in useful_column_indexes]

    improved_rows = []

    for row in rows[1:]:
        if not row or is_empty_row(row):
            continue

        row = row + [""] * (len(header) - len(row))

        bug_id = row[0].strip()

        if bug_id.endswith(" Improved"):
            clean_row = [row[index] for index in useful_column_indexes]
            improved_rows.append(clean_row)

    if not improved_rows:
        raise ValueError("No Improved rows found in Final Results.csv.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(clean_header)
        writer.writerows(improved_rows)

    print(f"Source file    : {FINAL_RESULTS_FILE}")
    print(f"Output file    : {OUTPUT_FILE}")
    print(f"Improved cases : {len(improved_rows)}")
    print("-" * 60)
    print("Created full_ground_truth_improved.csv successfully.")


if __name__ == "__main__":
    main()