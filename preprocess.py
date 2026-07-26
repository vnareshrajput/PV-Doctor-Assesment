"""
preprocess.py

Reads the raw PR and GHI CSV files and merges them into a single,
date-sorted dataframe.

Logic reused as-is from the original `data_preprocessing_pvDoctor.ipynb`
notebook (recursive file discovery -> concat -> merge on Date -> sort).
"""

from pathlib import Path

import pandas as pd


def preprocess_data(pr_folder: str, ghi_folder: str) -> pd.DataFrame:
    """
    Build the merged PR/GHI dataframe from the raw data folders.

    Parameters
    ----------
    pr_folder : str
        Path to the folder containing PR CSV files (searched recursively).
    ghi_folder : str
        Path to the folder containing GHI CSV files (searched recursively).

    Returns
    -------
    pd.DataFrame
        Merged dataframe with columns: Date, PR, GHI, sorted by Date.
    """
    # --- Read every PR CSV recursively ---
    pr_files = sorted(Path(pr_folder).rglob("*.csv"))
    pr_data = [pd.read_csv(file) for file in pr_files]
    pr_df = pd.concat(pr_data, ignore_index=True)

    # --- Read every GHI CSV recursively ---
    ghi_files = sorted(Path(ghi_folder).rglob("*.csv"))
    ghi_data = [pd.read_csv(file) for file in ghi_files]
    ghi_df = pd.concat(ghi_data, ignore_index=True)

    # --- Merge PR and GHI on Date ---
    merged_df = pd.merge(pr_df, ghi_df, on="Date", how="inner")

    # --- Convert Date to datetime and sort ---
    merged_df["Date"] = pd.to_datetime(merged_df["Date"])
    merged_df = merged_df.sort_values("Date")
    merged_df = merged_df.reset_index(drop=True)

    return merged_df
