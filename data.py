import argparse
import sys
import zipfile
from pathlib import Path

import pandas as pd


def find_csv_in_zip(zip_path: Path) -> str:
    with zipfile.ZipFile(zip_path) as zf:
        csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if not csv_names:
        sys.exit("No CSV file found inside the zip archive.")
    main = [n for n in csv_names if "openpowerlifting" in n.lower()]
    return (main or csv_names)[0]


def load_data(path: Path, nrows: int | None = None) -> pd.DataFrame:
    """Load the dataset from a .csv or .zip file."""
    if not path.exists():
        sys.exit(f"File not found: {path}")

    if path.suffix.lower() == ".zip":
        inner = find_csv_in_zip(path)
        print(f"Reading '{inner}' from zip archive...")
        with zipfile.ZipFile(path) as zf, zf.open(inner) as f:
            return pd.read_csv(f, nrows=nrows, low_memory=False)

    print(f"Reading '{path}'...")
    return pd.read_csv(path, nrows=nrows, low_memory=False)


def show_data(df: pd.DataFrame, rows: int) -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("\n" + "=" * 60)
    print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

    print("\n--- Columns and types ---")
    print(df.dtypes.to_string())

    print(f"\n--- First {rows} rows ---")
    print(df.head(rows).to_string())

    print("\n--- Missing values per column ---")
    missing = df.isna().sum()
    print(missing[missing > 0].sort_values(ascending=False).to_string())

    numeric_cols = [
        c for c in ["BodyweightKg", "Best3SquatKg", "Best3BenchKg",
                    "Best3DeadliftKg", "TotalKg", "Dots"]
        if c in df.columns
    ]
    if numeric_cols:
        print("\n--- Summary of key numeric columns ---")
        print(df[numeric_cols].describe().to_string())

    for col in ["Sex", "Event", "Equipment", "Federation", "Country"]:
        if col in df.columns:
            print(f"\n--- Top values: {col} ---")
            print(df[col].value_counts().head(10).to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Show OpenPowerlifting data.")
    parser.add_argument("file", type=Path, help="Path to the .csv or .zip file")
    parser.add_argument("--rows", type=int, default=10,
                        help="Number of rows to preview (default 10)")
    parser.add_argument("--sample", type=int, default=None,
                        help="Only read the first N rows (useful for a quick look)")
    args = parser.parse_args()

    df = load_data(args.file, nrows=args.sample)
    show_data(df, args.rows)


if __name__ == "__main__":
    main()
