from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path


FAMILY_COLORS = {
    "1": "#1f6f78",
    "2": "#c65d3b",
    "3": "#d49a25",
    "4": "#557a46",
    "5": "#2e5687",
    "6": "#8a4f46",
}


def create_figure(result: dict):
    from matplotlib.figure import Figure

    rows = result.get("detections", [])
    figure = Figure(figsize=(11, 7.2), dpi=100, facecolor="#f3efe5")
    grid = figure.add_gridspec(2, 2, hspace=0.42, wspace=0.3)
    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
        figure.add_subplot(grid[1, 1]),
    ]
    for axis in axes:
        axis.set_facecolor("#fbf8f0")
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", color="#d8d1c2", linewidth=0.6, alpha=0.8)
        axis.tick_params(labelsize=8)
    if not rows:
        for axis in axes:
            axis.axis("off")
        axes[0].text(
            0.5,
            0.5,
            "Run an analysis to create figures.",
            ha="center",
            va="center",
            fontsize=13,
        )
        figure.suptitle("METAPHORIQ Zero-Shot · no results", fontsize=15)
        return figure

    family_counts = Counter(row["taxonomy"]["family_id"] for row in rows)
    family_labels = {
        row["taxonomy"]["family_id"]: row["taxonomy"]["family_label"] for row in rows
    }
    families = sorted(family_counts)
    axes[0].bar(
        [family_labels[item] for item in families],
        [family_counts[item] for item in families],
        color=[FAMILY_COLORS.get(item, "#555555") for item in families],
    )
    axes[0].set_title("Detected spans by taxonomy family", loc="left", fontweight="bold")
    axes[0].set_ylabel("Annotated-span count")
    axes[0].tick_params(axis="x", rotation=28)

    class_counts = Counter(
        (row["taxonomy"]["class_id"], row["taxonomy"]["class_label"]) for row in rows
    )
    leading = class_counts.most_common(10)
    axes[1].barh(
        [f"{class_id} {label}" for (class_id, label), _ in reversed(leading)],
        [count for _, count in reversed(leading)],
        color="#2e5687",
    )
    axes[1].set_title("Leading provisional classes", loc="left", fontweight="bold")
    axes[1].set_xlabel("Detected-span count")

    model_ids = result["manifest"]["models"]
    agreement = Counter(row["positive_votes"] for row in rows)
    vote_levels = list(range(1, len(model_ids) + 1))
    axes[2].bar(
        vote_levels,
        [agreement[level] for level in vote_levels],
        color="#c65d3b",
        width=0.7,
    )
    axes[2].set_xticks(vote_levels)
    axes[2].set_xlabel(f"Positive detector votes (of {len(model_ids)})")
    axes[2].set_ylabel("Detected-span count")
    axes[2].set_title("Model agreement", loc="left", fontweight="bold")

    similarities = [row["taxonomy"]["similarity"] for row in rows]
    margins = [row["taxonomy"]["margin"] for row in rows]
    axes[3].scatter(
        similarities,
        margins,
        c=[FAMILY_COLORS.get(row["taxonomy"]["family_id"], "#555") for row in rows],
        alpha=0.78,
        edgecolors="white",
        linewidths=0.4,
    )
    axes[3].axhline(0.05, color="#8a4f46", linestyle="--", linewidth=1)
    axes[3].set_xlabel("Prototype cosine similarity")
    axes[3].set_ylabel("Top-two margin")
    axes[3].set_title("Taxonomy decision separation", loc="left", fontweight="bold")

    period = result["manifest"]["period"]["label"]
    figure.suptitle(
        f"METAPHORIQ Zero-Shot · {len(rows)} spans · {period}",
        fontsize=15,
        fontweight="bold",
        x=0.04,
        ha="left",
    )
    return figure


def save_figure(result: dict, path: Path, dpi: int = 180) -> None:
    figure = create_figure(result)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=figure.get_facecolor())

