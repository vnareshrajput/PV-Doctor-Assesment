"""
visualization.py

Generates the "Performance Ratio Evolution" graph from a merged
PR/GHI dataframe.

All plotting logic is reused as-is from the original
`visualization.ipynb` notebook (colour coding, 30-day moving average,
dynamic budget line, points-above-budget annotation, statistics box,
legend). The only functional addition is breaking the "points above
budget" figure down per financial year, since that was already
computed in the notebook (via `groupby("Budget_Year")`) but not yet
wired into the final chart.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

import pandas as pd

# ---- GHI colour-coding thresholds (from the notebook's get_color) ----
def get_color(ghi: float) -> str:
    """Map a GHI value to its scatter-point colour band."""
    if ghi < 2:
        return "navy"
    elif ghi < 4:
        return "skyblue"
    elif ghi < 6:
        return "orange"
    else:
        return "brown"


# ---- Dynamic Target Budget PR (from the notebook's budget_year / calculate_budget) ----
BASE_BUDGET = 73.9
DEGRADATION = 0.008  # 0.8% compounding reduction every financial year


def budget_year(date: pd.Timestamp) -> int:
    """
    Financial-year index for a date, anchored to the plant's first
    financial year (Jul 2019 - Jun 2020 -> 0, Jul 2020 - Jun 2021 -> 1, ...).
    """
    if date.month >= 7:
        return date.year - 2019
    else:
        return date.year - 2020


def calculate_budget(date: pd.Timestamp) -> float:
    """Dynamically compute the Budget PR for a date's financial year."""
    years = budget_year(date)
    return BASE_BUDGET * ((1 - DEGRADATION) ** years)


def average_last_days(df: pd.DataFrame, days: int) -> float:
    """Average PR over the trailing `days` rows of the (date-sorted) dataframe."""
    return df.tail(days)["PR"].mean()


def plot_performance_ratio(data: pd.DataFrame, output_path: str) -> None:
    """
    Build and save the full Performance Ratio Evolution graph.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with columns Date, PR, GHI (already filtered to the
        desired date range, if any). All derived columns (Color,
        moving average, budget, etc.) are computed inside this function
        so the graph always reflects exactly the rows passed in.
    output_path : str
        File path (including filename) to save the PNG graph to.
    """
    data = data.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    # --- Derived columns ---
    data["Color"] = data["GHI"].apply(get_color)
    data["PR_30MA"] = data["PR"].rolling(window=30).mean()
    data["Budget_Year"] = data["Date"].apply(budget_year)
    data["Budget"] = data["Date"].apply(calculate_budget)
    data["Above_Budget"] = data["PR"] > data["Budget"]

    # --- Statistics ---
    avg7 = average_last_days(data, 7)
    avg30 = average_last_days(data, 30)
    avg60 = average_last_days(data, 60)
    avg90 = average_last_days(data, 90)
    avg365 = average_last_days(data, 365)
    avg_lifetime = data["PR"].mean()

    # --- Points Above Budget (overall + per financial year) ---
    points_above = data["Above_Budget"].sum()
    percentage = (points_above / len(data)) * 100
    points_above_by_year = data.groupby("Budget_Year")["Above_Budget"].sum()

    # --- Figure ---
    fig, ax = plt.subplots(figsize=(18, 8))

    # Scatter Plot (GHI colour coded)
    ax.scatter(
        data["Date"],
        data["PR"],
        c=data["Color"],
        s=10,
        alpha=0.8,
    )

    # 30-Day Moving Average
    ax.plot(
        data["Date"],
        data["PR_30MA"],
        color="red",
        linewidth=2,
        label="30-Day Moving Average",
    )

    # Dynamic Budget Line
    ax.plot(
        data["Date"],
        data["Budget"],
        color="darkgreen",
        linewidth=2,
        label="Budget PR",
    )

    # Title
    ax.set_title(
        f"Performance Ratio Evolution\nFrom {data['Date'].min().date()} to {data['Date'].max().date()}",
        fontsize=16,
        fontweight="bold",
    )

    # Axis Labels
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Performance Ratio (%)", fontsize=12)

    # X Axis Formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    plt.xticks(rotation=45)

    # Grid
    ax.grid(True, linestyle="--", alpha=0.3)

    # Custom Legend
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", label="GHI < 2", markerfacecolor="navy", markersize=8),
        Line2D([0], [0], marker="o", color="w", label="2 \u2264 GHI < 4", markerfacecolor="skyblue", markersize=8),
        Line2D([0], [0], marker="o", color="w", label="4 \u2264 GHI < 6", markerfacecolor="orange", markersize=8),
        Line2D([0], [0], marker="o", color="w", label="GHI \u2265 6", markerfacecolor="brown", markersize=8),
        Line2D([0], [0], color="red", lw=2, label="30-Day Moving Average"),
        Line2D([0], [0], color="darkgreen", lw=2, label="Budget PR"),
    ]
    ax.legend(handles=legend_elements, loc="upper left")

    # Points Above Budget - overall
    ax.text(
        0.35,
        0.28,
        f"Points above Target Budget PR : {points_above}/{len(data)} = {percentage:.1f}%",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
    )

    # Points Above Budget - per financial year (annotated directly on the budget line)
    for fy, fy_group in data.groupby("Budget_Year"):
        fy_group = fy_group.sort_values("Date")
        mid_date = fy_group["Date"].iloc[len(fy_group) // 2]
        budget_value = fy_group["Budget"].iloc[0]
        fy_count = int(points_above_by_year.loc[fy])
        ax.annotate(
            f"{fy_count} pts\nabove budget",
            xy=(mid_date, budget_value),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="darkgreen",
            fontweight="bold",
        )

    # Statistics Box
    stats_text = (
        f"Average PR Last 7 Days : {avg7:.1f}%\n"
        f"Average PR Last 30 Days : {avg30:.1f}%\n"
        f"Average PR Last 60 Days : {avg60:.1f}%\n"
        f"Average PR Last 90 Days : {avg90:.1f}%\n"
        f"Average PR Last 365 Days : {avg365:.1f}%\n"
        f"Average PR Lifetime : {avg_lifetime:.1f}%"
    )

    ax.text(
        0.98,
        0.05,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        ha="right",
        va="bottom",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    ax.set_xlim(data["Date"].min(), data["Date"].max())

    # Save - high-resolution PNG output
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
