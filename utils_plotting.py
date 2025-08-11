SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42

COLUMN_LABELS = {
    "lwc [g/m^3]": r"$LWC \ (g/m^{3})$",
    "rh [%]": "RH (%)",
    "wind_w [m/s]": r"$wind_{up} \ (m/s)$",
    "ss_total [%]": "Seed score (%)",
    "temp_amb [C]": "$T_{amb} \ (\degree C)$" 
}

def col_to_label(col):
    if col not in COLUMN_LABELS:
        print(f"Note: {col} not found in COLUMN_LABELS")
    return COLUMN_LABELS.get(col, col)
