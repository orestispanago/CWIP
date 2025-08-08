import matplotlib.pyplot as plt


SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


def plot_hist(df, col, filename=""):
    plt.figure(figsize=(6, 4))
    plt.hist(df[col], bins=50, edgecolor="k")
    plt.rc("font", size=MEDIUM_SIZE)
    plt.xlabel(col)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_temp_ss_seed_ab(df):
    seed_a = df[(df["seed-a [cnt]"].diff() > 0)]
    seed_b = df[(df["seed-b [cnt]"].diff() > 0)]
    temp_a = seed_a["Ambient Temperature (C)"]
    temp_b = seed_b["Ambient Temperature (C)"]
    ss_a = seed_a["ss_total [%]"]
    ss_b = seed_b["ss_total [%]"]
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(ss_b, temp_b, edgecolor="k", label="seed-b")
    plt.scatter(ss_a, temp_a, edgecolor="k", label="seed-a")
    plt.ylabel("Ambient Temperature (C)")
    plt.gca().invert_yaxis()
    plt.xlabel("ss_total [%]")
    plt.legend()
    plt.show()


def plot_scatter(df, x, y, filename="", title=""):
    plt.rc("font", size=MEDIUM_SIZE)
    plt.scatter(df[x], df[y], edgecolor="k")
    # plt.xlim(-3,7)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()


def plot_scatter_gif(df_list, x, y, filename=""):
    ss_min, ss_max = 0, 100
    temp_min, temp_max = -17, 12

    fig, ax = plt.subplots()
    plt.rc("font", size=MEDIUM_SIZE)

    def update(frame):
        ax.clear()
        ax.invert_yaxis()
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_xlim(ss_min, ss_max)
        ax.set_ylim(temp_max, temp_min)

        past_alpha = 0.2
        current_alpha = 1.0
        color = "C0"

        # Plot all previous frames with faded alpha
        for i in range(frame):
            df = df_list[i]
            ax.scatter(
                df[x], df[y], color=color, alpha=past_alpha, edgecolor="k"
            )
        # Plot current frame with full alpha
        df = df_list[frame]
        ax.scatter(
            df[x], df[y], color=color, alpha=current_alpha, edgecolor="k"
        )
        ax.set_title(df.index[0].date())
        fig.tight_layout()
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(df_list), blit=False, repeat=False
    )
    if filename:
        ani.save(filename, writer="pillow", fps=1)
    plt.show()


def plot_bar(df, col):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(df.index, df[col], edgecolor="black")
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.set_ylabel(col)
    plt.rc("font", size=MEDIUM_SIZE)
    plt.show()


def plot_bar_stacked(df, col1, col2):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(df.index, df[col1], label=col1, edgecolor="black")
    ax.bar(df.index, df[col2], bottom=df[col1], label=col2, edgecolor="black")
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.5)
    ax.legend()
    plt.rc("font", size=MEDIUM_SIZE)
    plt.show()
