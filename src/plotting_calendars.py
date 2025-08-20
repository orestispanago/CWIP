import pandas as pd
import matplotlib.pyplot as plt
import calplot
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

from utils.plotting import savefig


def calplot_seed_events(df, filename=""):
    seed_counts = df.resample("D").size()
    # Fill missing dates with 0 (days with no seeding)
    all_dates = pd.date_range(
        start=seed_counts.index.min(), end=seed_counts.index.max(), freq="D"
    )
    seed_counts = seed_counts.reindex(all_dates, fill_value=0)
    fig, ax = calplot.calplot(
        seed_counts,
        cmap="jet",
        figsize=(12, 4),
        yearlabel_kws={"fontname": "sans-serif"},
    )
    fig.suptitle("Seed svents per day")
    savefig(filename)
    plt.show()


def calplot_planes_per_day(df, filename=""):
    # Count unique planes per day
    daily_aircraft_counts = (
        df.groupby(df.index.date)["aircraft"].nunique().rename("num_planes")
    )
    # Convert index back to datetime for calplot
    daily_aircraft_counts.index = pd.to_datetime(daily_aircraft_counts.index)
    fig, ax = calplot.calplot(
        daily_aircraft_counts,
        cmap="jet",
        figsize=(12, 4),
        yearlabel_kws={"fontname": "sans-serif"},
    )
    fig.axes[-1].yaxis.set_major_locator(MaxNLocator(integer=True))
    fig.suptitle("Operating planes per day")
    savefig(filename)
    plt.show()


def regions_per_day(regions):
    rset = set(regions)
    if "Central" in rset and "SW" in rset:
        return "both"
    elif "Central" in rset:
        return "Central"
    elif "SW" in rset:
        return "SW"
    else:
        return "none"


def calplot_regions_per_day(df, filename=""):
    daily_region = df.groupby(pd.Grouper(freq="D"))["region"].apply(
        regions_per_day
    )

    categories = ["Central", "SW", "both"]
    cmap = ListedColormap(
        [
            "tab:blue",  # Central
            "tab:orange",  # SW
            "tab:green",  # Both
        ]
    )

    daily_region_cat = pd.Categorical(
        daily_region, categories=categories, ordered=True
    )
    daily_region_int = (
        pd.Series(daily_region_cat.codes, index=daily_region.index) + 1
    )

    fig, ax = calplot.calplot(
        daily_region_int,
        yearlabel_kws={"fontname": "sans-serif"},
        cmap=cmap,
        figsize=(12, 4),
        colorbar=False,
    )

    # Legend
    legend_patches = [
        Patch(color=cmap(i), label=label) for i, label in enumerate(categories)
    ]
    plt.legend(
        handles=legend_patches,
        title="Region(s)",
        loc="lower left",
        bbox_to_anchor=(1.04, 0.5),
    )
    plt.suptitle("Seeding Regions by Day")
    savefig(filename)
    plt.show()
