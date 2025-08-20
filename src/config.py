import os

PARENT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

SHAPEFILES = os.path.join(PARENT, "data", "shapefiles")
RAW_DATA = os.path.join(PARENT, "data", "KSA CWIP Files")
SPLIT_DATA = os.path.join(PARENT, "data", "split")


TABLES = os.path.join(PARENT, "out", "tables")
BOXPLOTS = os.path.join(PARENT, "out", "plots", "boxplots")
CALPLOTS = os.path.join(PARENT, "out", "plots", "calplots")
MAPS = os.path.join(PARENT, "out", "plots", "maps")
TIMESERIES = os.path.join(PARENT, "out", "plots", "timeseries")

# CASE STUDY
CS_TABLES = os.path.join(PARENT, "out", "tables", "case-study")
CS_BARPLOTS = os.path.join(PARENT, "out", "plots", "case-study", "barplots")
CS_BOXPLOTS = os.path.join(PARENT, "out", "plots", "case-study", "boxplots")
CS_TIMESERIES = os.path.join(PARENT, "out", "plots", "case-study", "timeseries")
CS_MAPS = os.path.join(PARENT, "out", "plots", "case-study", "maps")

PLOTS_REVERSE = os.path.join(PARENT, "plots", "reverse-engineering")
