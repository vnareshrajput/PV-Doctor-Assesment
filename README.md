# PV Doctor — Performance Ratio Analysis & Visualization

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C)
![CLI](https://img.shields.io/badge/CLI-argparse-4B8BBE)
![Status](https://img.shields.io/badge/Status-Complete-2E7D32)

A small, modular Python project that turns raw daily PR (Performance Ratio) and GHI
(Global Horizontal Irradiance) CSV files from a solar PV plant into a single merged
dataset and a Performance Ratio Evolution chart — with a bonus command-line interface
for regenerating the chart over any custom date range.

## Project Overview

Solar PV plants generate two independent daily readings that matter for judging plant
health: **PR**, how efficiently the plant converts available sunlight into delivered
energy, and **GHI**, how much sunlight was actually available that day. This project
recursively reads both datasets from their raw, month-wise folder structure, merges
them into one dataframe on `Date`, and produces a chart that overlays daily PR
(colour-coded by GHI), a 30-day moving average, a dynamically-degrading budget target,
and supporting statistics — everything a plant operator needs to judge performance at
a glance.

The preprocessing and visualization logic were developed and validated first in
Jupyter notebooks, then restructured into a clean, importable Python project
(`main.py`, `preprocess.py`, `visualization.py`) to support the bonus command-line
requirement.

## Features

- Recursively reads every PR and GHI CSV file, regardless of folder depth (`pathlib.rglob`).
- Merges PR and GHI into a single dataframe on `Date` (inner join).
- Exports the merged dataset to `output/merged_data.csv`.
- Scatter plot of daily PR, colour-coded by GHI band:
  - Navy — GHI < 2
  - Sky blue — 2 ≤ GHI < 4
  - Orange — 4 ≤ GHI < 6
  - Brown — GHI ≥ 6
- Red line — 30-day moving average of PR.
- Dark green line — dynamically computed Target Budget PR, starting at 73.9 in the
  first financial year (Jul 2019 – Jun 2020) and compounding down 0.8% every
  subsequent financial year. Nothing here is hard-coded per year.
- "Points above Target Budget PR" — shown overall and broken down per financial year,
  annotated directly on the budget line.
- Statistics box — average PR over the last 7 / 30 / 60 / 90 / 365 days, and lifetime.
- Custom legend covering all scatter colours and line series.
- High-resolution (300 DPI) PNG output.
- **Bonus:** `--start_date` / `--end_date` command-line arguments to regenerate the
  chart — moving average, budget line, financial-year counts, and statistics all
  recalculated automatically — for any custom date range.

## Dataset Structure

Raw data is provided as two parallel folder trees, each split into monthly
sub-folders holding several daily CSV files:

| Column | Found In | Description |
|---|---|---|
| `Date` | PR and GHI files | Calendar date of the reading (read as text, converted to datetime). |
| `PR` | PR files | Daily Performance Ratio (%). |
| `GHI` | GHI files | Daily Global Horizontal Irradiance. |

- 394 raw CSV files in total (197 PR, 197 GHI), covering 33 months (Jul 2019 – Mar 2022).
- After merging, the dataset holds **982 rows**, with no duplicate dates or missing
  values in either source.

## Folder Structure

```
PV-Doctor-Assesment/
│
├── data/
│   ├── PR/                          # Raw daily PR CSVs (month-wise folders)
│   └── GHI/                         # Raw daily GHI CSVs (month-wise folders)
│
├── output/
│   ├── merged_data.csv               # Generated: merged PR + GHI dataset
│   └── performance_ratio.png         # Generated: Performance Ratio Evolution graph
│
├── 01-Preprocessing_pvDoctor.ipynb    # Exploratory development of preprocess_data()
├── 02-Visualization.ipynb             # Exploratory development of plot_performance_ratio()
├── preprocess.py                      # preprocess_data(pr_folder, ghi_folder)
├── visualization.py                    # plot_performance_ratio(data, output_path)
├── main.py                             # CLI entry point (argparse, orchestration)
├── requirements.txt
├── README.md
└── .gitignore
```

## Project Workflow

```
Reading PR files recursively (Path.rglob)
        ↓
Reading GHI files recursively (Path.rglob)
        ↓
Creating PR dataframe (pd.concat)          Creating GHI dataframe (pd.concat)
        └───────────────┬────────────────────────┘
                         ▼
              Merging on "Date" (pd.merge, how="inner")
                         ▼
        Data preprocessing (datetime conversion, sort)
                         ▼
   Feature Engineering (GHI colour, 30-day MA, budget, financial year)
                         ▼
        Optional --start_date / --end_date filter
                         ▼
              Performance Ratio Evolution chart (.png)
```

## Installation

### Clone the repository

```bash
git clone https://github.com/vnareshrajput/PV-Doctor-Assesment.git
cd PV-Doctor-Assesment
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

### Run Bonus (custom date range)

```bash
python main.py --start_date 2020-01-01 --end_date 2020-12-31
```

If `--start_date` is later than `--end_date`, the script exits with a clear error
instead of generating an incorrect chart.

## Output

Running the project produces:

- `output/merged_data.csv` — the full merged `Date / PR / GHI` dataset, regenerated
  on every run regardless of any date filter.
- `output/performance_ratio.png` — the Performance Ratio Evolution chart, filtered to
  the requested date range (or the full dataset if no range is supplied).

Console output looks like:

```
Merged data saved -> output/merged_data.csv (982 rows)
Graph saved -> output/performance_ratio.png (982 rows plotted)
```

### Screenshot

<img width="5364" height="2374" alt="performance_ratio" src="https://github.com/user-attachments/assets/576a1924-1a65-43e3-9602-db8e74dd8941" />

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Reading, merging, and transforming PR/GHI data |
| NumPy | Underlying numerical support |
| Matplotlib | Chart construction |
| Pathlib | Recursive CSV discovery |
| Argparse | Command-line interface for the bonus feature |
| Jupyter Notebook | Initial exploratory development |
| Git / GitHub | Version control and hosting |

## Results

- **Merged dataset:** 982 rows, 1 Jul 2019 – 24 Mar 2022, no duplicate or missing dates.
- **Budget PR:** 73.90% (Year 1), 73.31% (Year 2), 72.72% (Year 3) — computed entirely
  from the compounding 0.8% degradation formula, with no year-specific values hard-coded.
- **Points above budget:** 179/366 (Year 1), 170/349 (Year 2), 130/267 (Year 3, partial)
  — roughly 49% of days beat budget in every financial year.
- **Statistics:** average PR of 73.8% (last 7 days), 71.9% (last 30 days), 73.0% (last
  60 days), 73.1% (last 90 days), 72.8% (last 365 days), 72.7% lifetime.
- **Bonus:** verified working for both the full dataset and custom `--start_date` /
  `--end_date` ranges, with every derived figure recalculating correctly.

## Future Improvements

- Add automated tests for `preprocess_data()` and the budget/financial-year functions.
- Package the project for `pip install`.
- Add a `--output_dir` argument so outputs can be redirected without editing the code.
- Export the statistics summary as its own CSV alongside the chart.
- Add an interactive (Plotly/Bokeh) version of the chart for exploratory use.

## Author

**Naresh V**
B.Tech, Biosciences & Bioengineering (Data Science & Analytics), IIT Roorkee
Take Home Assessment — PV Doctor
