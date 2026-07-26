"""
main.py

Coordinates the PV plant Performance Ratio project:
  1. Reads and merges the raw PR/GHI data (preprocess.py).
  2. Optionally filters the merged data to a --start_date / --end_date range.
  3. Generates the Performance Ratio Evolution graph (visualization.py).
  4. Saves both the merged CSV and the graph PNG under output/.

Examples
--------
Full dataset:
    python main.py

Bonus - date-ranged graph:
    python main.py --start_date 2020-01-01 --end_date 2020-12-31
    python main.py --start_date 2021-07-01 --end_date 2022-03-24
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

from preprocess import preprocess_data
from visualization import plot_performance_ratio

# --- Project paths ---
PR_FOLDER = "data/PR"
GHI_FOLDER = "data/GHI"
OUTPUT_DIR = Path("output")
MERGED_CSV_PATH = OUTPUT_DIR / "merged_data.csv"
GRAPH_PATH = OUTPUT_DIR / "performance_ratio.png"


def parse_args() -> argparse.Namespace:
    """Parse and validate the --start_date / --end_date command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate the PV plant Performance Ratio Evolution graph."
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default=None,
        help="Start date to filter the graph (YYYY-MM-DD). Defaults to the full dataset.",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default=None,
        help="End date to filter the graph (YYYY-MM-DD). Defaults to the full dataset.",
    )
    args = parser.parse_args()

    if args.start_date and args.end_date:
        if pd.to_datetime(args.start_date) > pd.to_datetime(args.end_date):
            parser.error("--start_date must not be later than --end_date.")

    return args


def main() -> None:
    args = parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- Preprocess: merge PR and GHI data ---
    data = preprocess_data(PR_FOLDER, GHI_FOLDER)
    data.to_csv(MERGED_CSV_PATH, index=False)
    print(f"Merged data saved -> {MERGED_CSV_PATH} ({len(data)} rows)")

    # --- Filter to requested date range, if any ---
    if args.start_date:
        data = data[data["Date"] >= pd.to_datetime(args.start_date)]
    if args.end_date:
        data = data[data["Date"] <= pd.to_datetime(args.end_date)]
    data = data.reset_index(drop=True)

    if data.empty:
        print("No data found in the requested date range.", file=sys.stderr)
        sys.exit(1)

    # --- Visualize: generate the Performance Ratio Evolution graph ---
    plot_performance_ratio(data, output_path=str(GRAPH_PATH))
    print(f"Graph saved -> {GRAPH_PATH} ({len(data)} rows plotted)")


if __name__ == "__main__":
    main()
