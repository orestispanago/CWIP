import os
import matplotlib.pyplot as plt

SMALL_SIZE = 8
MEDIUM_SIZE = 12
LARGE_SIZE = 16

COLUMN_LABELS = {
    "lwc [g/m^3]": r"$LWC \ (g/m^{3})$",
    "rh [%]": "RH (%)",
    "wind_w [m/s]": r"$wind_{up} \ (m/s)$",
    "ss_total [%]": "Seed score (%)",
    "temp_amb [C]": "$T_{amb} \ (\degree C)$",
}


def col_to_label(col):
    if col not in COLUMN_LABELS:
        print(f"Note: {col} not found in COLUMN_LABELS")
    return COLUMN_LABELS.get(col, col)


def savefig(filename, **kwargs):
    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, bbox_inches="tight")
