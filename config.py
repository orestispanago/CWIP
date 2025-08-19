import os

PARENT_DIR = os.getcwd()


RAW_DATA = os.path.join(PARENT_DIR, "data", "KSA CWIP Files")
SPLIT_DATA = os.path.join(PARENT_DIR, "data", "split")


TABLES = os.path.join(PARENT_DIR, "out", "tables")
BOXPLOTS = os.path.join(PARENT_DIR, "plots", "boxplots")
CALPLOTS = os.path.join(PARENT_DIR, "plots", "calplots")
MAPS = os.path.join(PARENT_DIR, "plots", "maps")
TIMESERIES = os.path.join(PARENT_DIR, "plots", "timeseries")

# CASE STUDY
CS_TABLES = os.path.join(PARENT_DIR, "out", "tables", "case-study")
CS_BARPLOTS = os.path.join(PARENT_DIR, "plots", "case-study", "barplots")
CS_BOXPLOTS = os.path.join(PARENT_DIR, "plots", "case-study", "boxplots")
CS_TIMESERIES = os.path.join(PARENT_DIR, "plots", "case-study", "timeseries")
CS_MAPS = os.path.join(PARENT_DIR, "plots", "case-study", "maps")

PLOTS_REVERSE = os.path.join(PARENT_DIR, "plots", "reverse-engineering")
