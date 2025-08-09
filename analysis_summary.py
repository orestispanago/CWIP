import pandas as pd
from plotting_analysis import plot_bar, plot_bar_stacked,area_plot, plot_bar_multiple_side_by_side, plot_lines

summary = pd.read_csv("summary.csv")

summary["penetrations025_total"] = summary["penetrations025"] - summary["seed_total"]
summary["penetrations03_total"] = summary["penetrations03"] - summary["seed_total"]
summary["penetrations035_total"] = summary["penetrations035"] - summary["seed_total"]

print(f'Total seed: {summary["seed_total"].sum()}')
print(f'Penetrations 02: {summary["penetrations02"].sum()}')
print(f'Penetrations 025: {summary["penetrations025"].sum()}')
print(f'Penetrations 03: {summary["penetrations03"].sum()}')
print(f'Penetrations 035: {summary["penetrations035"].sum()}')
print(f'Penetrations 04: {summary["penetrations04"].sum()}')

print(f'Penetrations 025 - total: {summary["penetrations025_total"].median()}')
print(f'Penetrations 03  - total: {summary["penetrations03_total"].median()}')
print(f'Penetrations 035 - total: {summary["penetrations035_total"].median()}')

plot_bar(summary, "seed_total")
plot_bar(summary, "penetrations025_total")
plot_bar(summary, "penetrations03_total")
plot_bar(summary, "penetrations035_total")

plot_bar_stacked(summary, "seed_a", "seed_b")

plot_bar_multiple_side_by_side(summary, ["penetrations025", "seed_total", ])

plot_lines(summary, ["penetrations025", "seed_total", ])

area_plot(summary, [ "seed_total","penetrations025", ])

