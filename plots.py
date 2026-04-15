# plots.py
# Team Member 3: Visualization
# Generates 4 charts comparing the two teller scenarios.
# All charts are saved as PNG files in the output/ folder.

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.use("Agg")  # Use non-interactive backend (safe for script mode)

# Consistent color scheme throughout all charts
COLOR_A = "#2196F3"   # Blue  → Scenario A (2 tellers)
COLOR_B = "#4CAF50"   # Green → Scenario B (3 tellers)

OUTPUT_DIR = "output"


def ensure_output_dir():
    """Creates the output/ folder if it doesn't already exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def chart1_avg_wait_comparison(overall_a, overall_b):
    """
    Chart 1 — Bar chart: Average wait time for 2 vs 3 tellers.
    Gives a quick visual of the biggest customer-facing improvement.
    """
    fig, ax = plt.subplots(figsize=(6, 5))

    scenarios = ["2 Tellers\n(Current)", "3 Tellers\n(Proposed)"]
    values = [overall_a["avg_wait"], overall_b["avg_wait"]]
    colors = [COLOR_A, COLOR_B]

    bars = ax.bar(scenarios, values, color=colors, width=0.45, edgecolor="white",
                  linewidth=1.2)

    # Annotate bars with exact values
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{val:.2f} min", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title("Average Customer Wait Time\n2 Tellers vs 3 Tellers", fontsize=13,
                 fontweight="bold", pad=12)
    ax.set_ylabel("Average Wait Time (minutes)", fontsize=11)
    ax.set_ylim(0, max(values) * 1.3)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart1_avg_wait.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart2_queue_over_time(results_a):
    """
    Chart 2 — Line chart: Queue length over time for a single replication.
    Shows how the queue builds and drains during the simulation day.
    Uses the first replication of Scenario A (2 tellers).
    """
    rep_data = results_a[0]  # First replication
    times = [t for (t, _) in rep_data["queue_over_time"]]
    lengths = [q for (_, q) in rep_data["queue_over_time"]]

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.step(times, lengths, where="post", color=COLOR_A, linewidth=1.5,
            label="Queue Length")
    ax.fill_between(times, lengths, step="post", alpha=0.15, color=COLOR_A)

    ax.set_title("Queue Length Over Time — Scenario A (2 Tellers, Rep 1)",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Simulation Time (minutes)", fontsize=11)
    ax.set_ylabel("Number of Customers in Queue", fontsize=11)
    ax.set_xlim(0, max(times) if times else 240)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart2_queue_over_time.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart3_utilization(overall_a, overall_b):
    """
    Chart 3 — Bar chart: Teller utilization % for both scenarios.
    Helps management understand whether tellers are over- or under-loaded.
    """
    fig, ax = plt.subplots(figsize=(6, 5))

    scenarios = ["2 Tellers\n(Current)", "3 Tellers\n(Proposed)"]
    values = [overall_a["utilization_pct"], overall_b["utilization_pct"]]
    colors = [COLOR_A, COLOR_B]

    bars = ax.bar(scenarios, values, color=colors, width=0.45, edgecolor="white",
                  linewidth=1.2)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # Draw a reference line at 100% (capacity ceiling)
    ax.axhline(y=100, color="red", linestyle="--", linewidth=1, label="100% Capacity")

    ax.set_title("Teller Utilization Rate\n2 Tellers vs 3 Tellers",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Utilization (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart3_utilization.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart4_wait_per_replication(per_rep_a, per_rep_b):
    """
    Chart 4 — Grouped bar chart: Avg wait time for every replication,
    both scenarios side by side. Shows consistency (or variability) across runs.
    """
    n = len(per_rep_a)
    x = np.arange(n)
    bar_width = 0.35

    waits_a = [r["avg_wait"] for r in per_rep_a]
    waits_b = [r["avg_wait"] for r in per_rep_b]

    fig, ax = plt.subplots(figsize=(11, 5))

    bars_a = ax.bar(x - bar_width / 2, waits_a, bar_width,
                    label="2 Tellers", color=COLOR_A, edgecolor="white", linewidth=0.8)
    bars_b = ax.bar(x + bar_width / 2, waits_b, bar_width,
                    label="3 Tellers", color=COLOR_B, edgecolor="white", linewidth=0.8)

    ax.set_title("Average Wait Time per Replication — Both Scenarios",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Replication Number", fontsize=11)
    ax.set_ylabel("Average Wait Time (minutes)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([str(i + 1) for i in range(n)])
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "chart4_wait_per_replication.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def generate_all_charts(overall_a, overall_b, per_rep_a, per_rep_b, results_a):
    """
    Entry point: generates all 4 charts and saves them to output/.
    Called from main.py.
    """
    ensure_output_dir()
    print("\nGenerating charts...")
    chart1_avg_wait_comparison(overall_a, overall_b)
    chart2_queue_over_time(results_a)
    chart3_utilization(overall_a, overall_b)
    chart4_wait_per_replication(per_rep_a, per_rep_b)
    print("Charts saved to output/ folder.")
