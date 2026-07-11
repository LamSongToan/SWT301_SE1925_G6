from pathlib import Path
import csv
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[2]

PILOT_DATA_IMPROVED_DIR = BASE_DIR / "Data" / "Improved"
FULL_DATA_IMPROVED_DIR = BASE_DIR / "Data" / "Full" / "Improved"

PILOT_RESULTS_IMPROVED_DIR = BASE_DIR / "Results" / "Improved"
FULL_RESULTS_IMPROVED_DIR = BASE_DIR / "Results" / "Full" / "Improved"

FULL_GROUND_TRUTH_FILE = (
    FULL_DATA_IMPROVED_DIR / "full_ground_truth_improved.csv"
)


REQUIRED_PILOT_DATA_FILES = [
    "kappa_scores_improved.csv",
    "pilot_annotation_improved_author1.csv",
    "pilot_annotation_improved_author2.csv",
    "pilot_ground_truth_improved.csv",
    "pilot_sample_improved.csv",
]

REQUIRED_FULL_DATA_FILES = [
    "full_ground_truth_improved.csv",
    "full_sample_improved.csv",
]

EXPECTED_PILOT_RESULT_FILES = [
    "pilot_llm_output_improved.csv",
    "pilot_api_log_improved.csv",
    "summary_improved.csv",
    "mismatch_analysis_improved.csv",
]

EXPECTED_FULL_RESULT_FILES = [
    "full_llm_output_improved.csv",
    "full_api_log_improved.csv",
    "summary_full_improved.csv",
    "mismatch_analysis_full_improved.csv",
]


def read_csv_rows(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Cannot find CSV file: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))

    if not rows:
        raise ValueError(f"CSV file has no rows: {path}")

    return rows


def normalize_issue_key(value: str) -> str:
    return (
        value.strip()
        .replace(" Improved", "")
        .replace(" Raw", "")
        .replace("_improved", "")
        .replace("_raw", "")
        .strip()
    )


def extract_first_column_keys(rows):
    keys = []

    for row in rows[1:]:
        if not row or not row[0].strip():
            continue

        keys.append(normalize_issue_key(row[0]))

    return keys


def extract_kappa_case_keys(rows):
    keys = []

    for row in rows[1:]:
        if not row or not row[0].strip():
            continue

        first_value = row[0].strip()

        if first_value.startswith("MC-"):
            keys.append(normalize_issue_key(first_value))

    return keys


def find_column_index(header, column_name):
    target = column_name.strip().lower()

    for index, value in enumerate(header):
        if value.strip().lower() == target:
            return index

    return None


def count_s2r_labels(rows):
    if not rows:
        return Counter()

    header = rows[0]
    label_index = find_column_index(header, "S2R Label")

    if label_index is None:
        label_index = find_column_index(header, "s2r_label")

    if label_index is None:
        return Counter()

    labels = []

    for row in rows[1:]:
        if not row or not row[0].strip():
            continue

        if len(row) > label_index:
            label = row[label_index].strip()

            if label:
                labels.append(label)

    return Counter(labels)


def parse_kappa_summary(rows):
    summary = {}

    for row in rows:
        if not row or not row[0].strip():
            continue

        key = row[0].strip()

        if key in ["N", "Cohen Kappa", "Agreement"]:
            summary[key] = row[1].strip() if len(row) > 1 else ""

    return summary


def check_required_data_files():
    print("Checking Pilot data: Data/Improved...")
    print("-" * 60)

    missing_files = []
    empty_files = []

    for filename in REQUIRED_PILOT_DATA_FILES:
        path = PILOT_DATA_IMPROVED_DIR / filename

        if path.exists() and path.stat().st_size > 0:
            print(f"FOUND   : {filename}")
        elif path.exists() and path.stat().st_size == 0:
            print(f"EMPTY   : {filename}")
            empty_files.append(str(path))
        else:
            print(f"MISSING : {filename}")
            missing_files.append(str(path))

    print("-" * 60)

    if missing_files:
        raise FileNotFoundError(
            "Missing required Improved Pilot data files: "
            + ", ".join(missing_files)
        )

    if empty_files:
        raise ValueError(
            "Empty required Improved Pilot data files: "
            + ", ".join(empty_files)
        )

    print("All required Improved Pilot data files exist.")
    print()

    print("Checking Full data: Data/Full/Improved...")
    print("-" * 60)

    missing_files = []
    empty_files = []

    for filename in REQUIRED_FULL_DATA_FILES:
        path = FULL_DATA_IMPROVED_DIR / filename

        if path.exists() and path.stat().st_size > 0:
            print(f"FOUND   : {filename}")
        elif path.exists() and path.stat().st_size == 0:
            print(f"EMPTY   : {filename}")
            empty_files.append(str(path))
        else:
            print(f"MISSING : {filename}")
            missing_files.append(str(path))

    print("-" * 60)

    if missing_files:
        raise FileNotFoundError(
            "Missing required Improved Full data files: "
            + ", ".join(missing_files)
        )

    if empty_files:
        raise ValueError(
            "Empty required Improved Full data files: "
            + ", ".join(empty_files)
        )

    print("All required Improved Full data files exist.")
    print()


def check_results_status():
    print("Checking Improved result folders...")
    print("=" * 60)

    print("Pilot results: Results/Improved")
    print("-" * 60)

    if not PILOT_RESULTS_IMPROVED_DIR.exists():
        print("PENDING : Results/Improved folder does not exist yet.")
        print("This is OK before running the Improved pilot experiment.")
    else:
        readme_file = PILOT_RESULTS_IMPROVED_DIR / "README.md"
        gitkeep_file = PILOT_RESULTS_IMPROVED_DIR / ".gitkeep"

        if readme_file.exists():
            print("FOUND   : README.md")
        else:
            print("MISSING : README.md")

        if gitkeep_file.exists():
            print("FOUND   : .gitkeep")
        else:
            print("OPTIONAL: .gitkeep is missing")

        for filename in EXPECTED_PILOT_RESULT_FILES:
            path = PILOT_RESULTS_IMPROVED_DIR / filename

            if path.exists() and path.stat().st_size > 0:
                print(f"FOUND   : {filename}")
            elif path.exists() and path.stat().st_size == 0:
                print(
                    f"EMPTY   : {filename} "
                    "- should be regenerated by experiment scripts"
                )
            else:
                print(f"PENDING : {filename}")

    print()
    print("Full results: Results/Full/Improved")
    print("-" * 60)

    if not FULL_RESULTS_IMPROVED_DIR.exists():
        print("PENDING : Results/Full/Improved folder does not exist yet.")
        print("This is OK before running the Improved full experiment.")
    else:
        for filename in EXPECTED_FULL_RESULT_FILES:
            path = FULL_RESULTS_IMPROVED_DIR / filename

            if path.exists() and path.stat().st_size > 0:
                print(f"FOUND   : {filename}")
            elif path.exists() and path.stat().st_size == 0:
                print(
                    f"EMPTY   : {filename} "
                    "- should be regenerated by experiment scripts"
                )
            else:
                print(f"PENDING : {filename}")

    print("=" * 60)
    print("Improved result files may be pending before running the LLM.")
    print()


def print_key_consistency(base_name, base_keys, target_name, target_keys):
    missing_in_target = sorted(set(base_keys) - set(target_keys))
    extra_in_target = sorted(set(target_keys) - set(base_keys))

    if not missing_in_target and not extra_in_target:
        print(f"{base_name} vs {target_name}: OK")
        return

    print(f"{base_name} vs {target_name}: NOT OK")
    print(f"Missing in {target_name}: {missing_in_target}")
    print(f"Extra in {target_name}  : {extra_in_target}")


def fail_if_key_mismatch(base_name, base_keys, target_name, target_keys):
    missing_in_target = sorted(set(base_keys) - set(target_keys))
    extra_in_target = sorted(set(target_keys) - set(base_keys))

    if missing_in_target or extra_in_target:
        raise ValueError(
            f"{base_name} and {target_name} do not contain the same issue keys."
        )


def main():
    check_required_data_files()
    check_results_status()

    pilot_sample_rows = read_csv_rows(PILOT_DATA_IMPROVED_DIR / "pilot_sample_improved.csv")
    pilot_gt_rows = read_csv_rows(PILOT_DATA_IMPROVED_DIR / "pilot_ground_truth_improved.csv")
    full_sample_rows = read_csv_rows(FULL_DATA_IMPROVED_DIR / "full_sample_improved.csv")
    full_gt_rows = read_csv_rows(FULL_GROUND_TRUTH_FILE)
    author1_rows = read_csv_rows(PILOT_DATA_IMPROVED_DIR / "pilot_annotation_improved_author1.csv")
    author2_rows = read_csv_rows(PILOT_DATA_IMPROVED_DIR / "pilot_annotation_improved_author2.csv")
    kappa_rows = read_csv_rows(PILOT_DATA_IMPROVED_DIR / "kappa_scores_improved.csv")

    pilot_sample_keys = extract_first_column_keys(pilot_sample_rows)
    pilot_gt_keys = extract_first_column_keys(pilot_gt_rows)
    full_sample_keys = extract_first_column_keys(full_sample_rows)
    full_gt_keys = extract_first_column_keys(full_gt_rows)
    author1_keys = extract_first_column_keys(author1_rows)
    author2_keys = extract_first_column_keys(author2_rows)
    kappa_keys = extract_kappa_case_keys(kappa_rows)

    print("Improved data row count:")
    print("-" * 60)
    print(f"pilot_sample_improved.csv              : {len(pilot_sample_keys)} cases")
    print(f"pilot_ground_truth_improved.csv        : {len(pilot_gt_keys)} cases")
    print(f"full_sample_improved.csv               : {len(full_sample_keys)} cases")
    print(f"full_ground_truth_improved.csv         : {len(full_gt_keys)} cases")
    print(f"pilot_annotation_improved_author1.csv  : {len(author1_keys)} cases")
    print(f"pilot_annotation_improved_author2.csv  : {len(author2_keys)} cases")
    print(f"kappa_scores_improved.csv              : {len(kappa_keys)} case rows")
    print()

    print("Checking pilot issue key consistency:")
    print("-" * 60)

    print_key_consistency(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_ground_truth_improved.csv",
        pilot_gt_keys,
    )

    print_key_consistency(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_annotation_improved_author1.csv",
        author1_keys,
    )

    print_key_consistency(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_annotation_improved_author2.csv",
        author2_keys,
    )

    print_key_consistency(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "kappa_scores_improved.csv",
        kappa_keys,
    )

    fail_if_key_mismatch(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_ground_truth_improved.csv",
        pilot_gt_keys,
    )
    fail_if_key_mismatch(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_annotation_improved_author1.csv",
        author1_keys,
    )
    fail_if_key_mismatch(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "pilot_annotation_improved_author2.csv",
        author2_keys,
    )
    fail_if_key_mismatch(
        "pilot_sample_improved.csv",
        pilot_sample_keys,
        "kappa_scores_improved.csv",
        kappa_keys,
    )

    print()

    print("Checking full issue key consistency:")
    print("-" * 60)

    print_key_consistency(
        "full_sample_improved.csv",
        full_sample_keys,
        "full_ground_truth_improved.csv",
        full_gt_keys,
    )

    fail_if_key_mismatch(
        "full_sample_improved.csv",
        full_sample_keys,
        "full_ground_truth_improved.csv",
        full_gt_keys,
    )

    print()

    print("Improved S2R Label distribution:")
    print("-" * 60)
    print("Pilot Ground Truth:", dict(count_s2r_labels(pilot_gt_rows)))
    print("Full Ground Truth :", dict(count_s2r_labels(full_gt_rows)))
    print("Author 1          :", dict(count_s2r_labels(author1_rows)))
    print("Author 2          :", dict(count_s2r_labels(author2_rows)))
    print()

    print("Kappa summary:")
    print("-" * 60)

    kappa_summary = parse_kappa_summary(kappa_rows)

    if kappa_summary:
        for key, value in kappa_summary.items():
            print(f"{key}: {value}")
    else:
        print("No kappa summary found.")

    print()
    print("Improved folder check completed successfully.")


if __name__ == "__main__":
    main()
