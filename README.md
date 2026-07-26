# PV Plant Performance Ratio (PR) Evolution

## Project Overview

This project processes daily **PR (Performance Ratio)** and **GHI (Global Horizontal
Irradiance)** data for a solar PV plant and generates a **Performance Ratio Evolution**
graph — combining a colour-coded scatter plot, a 30-day moving average, a dynamically
degrading Target Budget PR line, and key performance statistics.

The raw data is organized as year-month sub-folders of daily CSV files under `data/PR/`
and `data/GHI/`. The project merges all of this into a single dataset and produces a
publication-quality PNG chart.

## Features

- ✔ Recursively reads every PR and GHI CSV file, regardless of folder depth.
- ✔ Merges PR and GHI into a single dataframe on `Date`.
- ✔ Exports the merged dataset to `output/merged_data.csv`.
- ✔ Scatter plot of daily PR values, colour-coded by GHI band:
  - Navy: GHI < 2
  - Sky blue: 2 ≤ GHI < 4
  - Orange: 4 ≤ GHI < 6
  - Brown: GHI ≥ 6
- ✔ Red line: 30-day moving average of PR.
- ✔ Dark-green line: dynamically computed Target Budget PR — starts at 73.9 in the
  first financial year (Jul 2019 - Jun 2020) and compounds down by 0.8% every
  subsequent financial year (never hard-coded per-year).
- ✔ "Points above Target Budget PR" — shown both overall and broken down per
  financial year, annotated directly on the budget line.
- ✔ Statistics box: average PR over the last 7 / 30 / 60 / 90 / 365 days and lifetime.
- ✔ Clean, custom legend for all scatter colours and line series.
- ✔ High-resolution (300 DPI) PNG output.
- ✔ **Bonus:** `--start_date` / `--end_date` command-line arguments to regenerate the
  graph (moving average, statistics, budget line, and financial-year counts all
  recalculated automatically) for any custom date range.

## Folder Structure

```
take_home_assessment/
│
├── data/
│   ├── PR/                     # Raw daily PR CSVs, organized by year-month
│   └── GHI/                    # Raw daily GHI CSVs, organized by year-month
│
├── output/
│   ├── merged_data.csv         # Generated: merged PR + GHI dataset
│   └── performance_ratio.png   # Generated: Performance Ratio Evolution graph
│
├── preprocess.py                # preprocess_data(pr_folder, ghi_folder) -> DataFrame
├── visualization.py              # plot_performance_ratio(data, output_path)
├── main.py                       # CLI entry point (argparse, orchestration)
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

## Run Project

Generate the graph for the **complete dataset**:

```bash
python main.py
```

## Run Bonus Examples

Generate the graph for a **custom date range**:

```bash
python main.py --start_date 2020-01-01 --end_date 2020-12-31
python main.py --start_date 2021-07-01 --end_date 2022-03-24
```

If `--start_date` is later than `--end_date`, the script exits with a friendly error
instead of generating an incorrect graph.

## Expected Output

Running the project produces:

- `output/merged_data.csv` — the merged Date / PR / GHI dataset (full dataset, always
  regenerated on every run regardless of date filters).
- `output/performance_ratio.png` — the Performance Ratio Evolution graph, filtered to
  the requested date range (or the full dataset if no range is supplied).

Console output looks like:

```
Merged data saved -> output/merged_data.csv (982 rows)
Graph saved -> output/performance_ratio.png (982 rows plotted)
```

## Screenshots

_Add a screenshot of `output/performance_ratio.png` here._

![Performance Ratio Evolution](output/performance_ratio.png)

## Notes

- The core preprocessing and plotting logic is carried over from the original
  `data_preprocessing_pvDoctor.ipynb` and `visualization.ipynb` notebooks; this
  project only restructures that logic into a clean, reusable, script-based package
  and adds the date-range (bonus) capability.
- The per-financial-year "points above budget" breakdown was already computed in the
  original notebook (`groupby("Budget_Year")`) but not yet wired into the final chart —
  it has been added to the graph here to satisfy the full "Financial Year Points Above
  Budget" requirement.
