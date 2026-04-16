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


# ── Helper: Validated Input ────────────────────────────────────────────────────
def get_float(prompt, default, min_val=0.1):
    """Ask user for a float, fall back to default on blank/invalid input."""
    raw = input(f"{prompt} [default: {default}]: ").strip()
    if raw == "":
        return default
    try:
        val = float(raw)
        if val < min_val:
            print(f"  ⚠  Value must be ≥ {min_val}. Using default ({default}).")
            return default
        return val
    except ValueError:
        print(f"  ⚠  Invalid input. Using default ({default}).")
        return default


def get_int(prompt, default, min_val=1):
    """Ask user for an integer, fall back to default on blank/invalid input."""
    raw = input(f"{prompt} [default: {default}]: ").strip()
    if raw == "":
        return default
    try:
        val = int(raw)
        if val < min_val:
            print(f"  ⚠  Value must be ≥ {min_val}. Using default ({default}).")
            return default
        return val
    except ValueError:
        print(f"  ⚠  Invalid input. Using default ({default}).")
        return default


# ── Collect Parameters from User ───────────────────────────────────────────────
print("=" * 60)
print("  Bank Teller Queuing Simulation — Parameter Setup")
print("  Press Enter to accept the default value shown in [ ]")
print("=" * 60)

SIM_DURATION     = get_float("Simulation duration (minutes)",                    default=240,  min_val=10)
NUM_REPS         = get_int  ("Number of replications",                           default=10,   min_val=1)
ARRIVAL_MEAN     = get_float("Mean customer inter-arrival time (minutes)",       default=3.0)
SERVICE_MEAN     = get_float("Mean service time per customer (minutes)",         default=5.0)
BASE_SEED        = get_int  ("Base random seed (any integer, 0 = random each run)", default=42, min_val=0)
CURRENT_TELLERS  = get_int  ("Current number of tellers (Scenario A)",           default=2,    min_val=1)
PROPOSED_TELLERS = get_int  ("Proposed number of tellers (Scenario B)",          default=3,    min_val=1)

if PROPOSED_TELLERS <= CURRENT_TELLERS:
    print(f"\n  ⚠  Proposed ({PROPOSED_TELLERS}) must be > current ({CURRENT_TELLERS}).")
    print(f"     Automatically setting proposed tellers to {CURRENT_TELLERS + 1}.")
    PROPOSED_TELLERS = CURRENT_TELLERS + 1

print()

# ── Run Both Scenarios ─────────────────────────────────────────────────────────
print(f"Running Scenario A: {CURRENT_TELLERS} Tellers...")
results_a = run_simulation(
    num_tellers=CURRENT_TELLERS,
    num_replications=NUM_REPS,
    sim_duration=SIM_DURATION,
    arrival_mean=ARRIVAL_MEAN,
    service_mean=SERVICE_MEAN,
    base_seed=BASE_SEED,
)

print(f"Running Scenario B: {PROPOSED_TELLERS} Tellers...")
results_b = run_simulation(
    num_tellers=PROPOSED_TELLERS,
    num_replications=NUM_REPS,
    sim_duration=SIM_DURATION,
    arrival_mean=ARRIVAL_MEAN,
    service_mean=SERVICE_MEAN,
    base_seed=BASE_SEED,
)

# ── Analyze Results ────────────────────────────────────────────────────────────
per_rep_a, overall_a = analyze_scenario(results_a, num_tellers=CURRENT_TELLERS,
                                        sim_duration=SIM_DURATION)
per_rep_b, overall_b = analyze_scenario(results_b, num_tellers=PROPOSED_TELLERS,
                                        sim_duration=SIM_DURATION)

# ── Print to Console ───────────────────────────────────────────────────────────
print_comparison(overall_a, overall_b, NUM_REPS, SIM_DURATION, ARRIVAL_MEAN)
print_scenario_table(f"Scenario A: {CURRENT_TELLERS} Tellers", per_rep_a, overall_a)
print_scenario_table(f"Scenario B: {PROPOSED_TELLERS} Tellers", per_rep_b, overall_b)
print_recommendation(overall_a, overall_b, CURRENT_TELLERS, PROPOSED_TELLERS)

# ── Generate Charts ────────────────────────────────────────────────────────────
generate_all_charts(overall_a, overall_b, per_rep_a, per_rep_b, results_a)
