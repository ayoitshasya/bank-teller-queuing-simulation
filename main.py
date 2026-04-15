# main.py
# Runner Script — ties everything together.
# Run this file to execute both scenarios, print results, and save charts.
#
# Usage:
#   pip install simpy matplotlib numpy
#   python main.py

from simulation import run_simulation
from analysis import (
    analyze_scenario,
    print_comparison,
    print_scenario_table,
    print_recommendation,
)
from plots import generate_all_charts

# ── Simulation Parameters ──────────────────────────────────────────────────────
SIM_DURATION   = 240    # Total simulation time in minutes (4 hours)
NUM_REPS       = 10     # Number of independent replications
ARRIVAL_MEAN   = 3.0    # Mean inter-arrival time in minutes (≈ 20 customers/hr)
SERVICE_MEAN   = 5.0    # Mean service time per customer in minutes
BASE_SEED      = 42     # Base random seed for reproducibility

# ── Run Both Scenarios ─────────────────────────────────────────────────────────
print("Running Scenario A: 2 Tellers...")
results_a = run_simulation(
    num_tellers=2,
    num_replications=NUM_REPS,
    sim_duration=SIM_DURATION,
    arrival_mean=ARRIVAL_MEAN,
    service_mean=SERVICE_MEAN,
    base_seed=BASE_SEED,
)

print("Running Scenario B: 3 Tellers...")
results_b = run_simulation(
    num_tellers=3,
    num_replications=NUM_REPS,
    sim_duration=SIM_DURATION,
    arrival_mean=ARRIVAL_MEAN,
    service_mean=SERVICE_MEAN,
    base_seed=BASE_SEED,
)

# ── Analyze Results ────────────────────────────────────────────────────────────
per_rep_a, overall_a = analyze_scenario(results_a, num_tellers=2,
                                        sim_duration=SIM_DURATION)
per_rep_b, overall_b = analyze_scenario(results_b, num_tellers=3,
                                        sim_duration=SIM_DURATION)

# ── Print to Console ───────────────────────────────────────────────────────────
print_comparison(overall_a, overall_b, NUM_REPS, SIM_DURATION, ARRIVAL_MEAN)
print_scenario_table("Scenario A: 2 Tellers", per_rep_a, overall_a)
print_scenario_table("Scenario B: 3 Tellers", per_rep_b, overall_b)
print_recommendation(overall_a, overall_b)

# ── Generate Charts ────────────────────────────────────────────────────────────
generate_all_charts(overall_a, overall_b, per_rep_a, per_rep_b, results_a)
