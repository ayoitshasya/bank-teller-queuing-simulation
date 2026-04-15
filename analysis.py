# analysis.py
# Team Member 2: Statistical Analysis & Results Comparison
# Processes raw simulation data to compute per-replication
# statistics, then compares the two teller scenarios side by side.

import numpy as np


def compute_replication_stats(rep_data, num_tellers, sim_duration):
    """
    Computes summary statistics for a single simulation replication.

    Parameters:
      rep_data     – Dict with 'customers' and 'queue_over_time' lists
      num_tellers  – Number of tellers (used to compute utilization)
      sim_duration – Length of the simulation in minutes

    Returns a dict with:
      - num_customers   : total customers served
      - avg_wait        : mean time customers waited in queue
      - max_wait        : worst-case wait time
      - avg_queue       : mean queue length (sampled at arrival events)
      - max_queue       : peak queue length observed
      - utilization_pct : percentage of total teller-time that was busy
    """
    customers = rep_data["customers"]
    queue_snapshots = rep_data["queue_over_time"]

    if not customers:
        # Edge case: no customers arrived (shouldn't happen with our params)
        return {
            "num_customers": 0,
            "avg_wait": 0.0, "max_wait": 0.0,
            "avg_queue": 0.0, "max_queue": 0,
            "utilization_pct": 0.0,
        }

    wait_times = [c["wait"] for c in customers]
    service_times = [c["service"] for c in customers]

    # Teller utilization: total service time / (num_tellers × sim_duration)
    total_service = sum(service_times)
    utilization = (total_service / (num_tellers * sim_duration)) * 100

    queue_lengths = [q for (_, q) in queue_snapshots] if queue_snapshots else [0]

    return {
        "num_customers": len(customers),
        "avg_wait": np.mean(wait_times),
        "max_wait": max(wait_times),
        "avg_queue": np.mean(queue_lengths),
        "max_queue": max(queue_lengths),
        "utilization_pct": utilization,
    }


def analyze_scenario(all_rep_data, num_tellers, sim_duration):
    """
    Applies compute_replication_stats() to every replication in a scenario
    and also computes the cross-replication averages.

    Returns:
      per_rep   – List of stat dicts (one per replication)
      overall   – Dict of averages across all replications
    """
    per_rep = []
    for rep_data in all_rep_data:
        stats = compute_replication_stats(rep_data, num_tellers, sim_duration)
        per_rep.append(stats)

    # Average each metric across replications
    keys = ["num_customers", "avg_wait", "max_wait", "avg_queue",
            "max_queue", "utilization_pct"]
    overall = {k: np.mean([r[k] for r in per_rep]) for k in keys}

    return per_rep, overall


def print_scenario_table(label, per_rep, overall):
    """
    Prints a formatted table for one scenario to the console.
    """
    print(f"\n--- {label} ---")
    header = f"{'Replication':<12} {'Customers':<11} {'Avg Wait':<12} " \
             f"{'Max Wait':<12} {'Avg Queue':<12} {'Utilization'}"
    print(header)
    print("-" * len(header))

    for i, r in enumerate(per_rep, start=1):
        print(
            f"{i:<12} "
            f"{r['num_customers']:<11} "
            f"{r['avg_wait']:<12.2f} "
            f"{r['max_wait']:<12.1f} "
            f"{r['avg_queue']:<12.2f} "
            f"{r['utilization_pct']:.1f}%"
        )

    print("-" * len(header))
    print(
        f"{'Overall':<12} "
        f"{overall['num_customers']:<11.1f} "
        f"{overall['avg_wait']:<12.2f} "
        f"{overall['max_wait']:<12.1f} "
        f"{overall['avg_queue']:<12.2f} "
        f"{overall['utilization_pct']:.1f}%"
    )


def print_comparison(overall_a, overall_b, num_rep, sim_duration, arrival_mean):
    """
    Prints the full comparison banner: header, both scenario tables,
    and a final recommendation.
    """
    print("\n" + "=" * 60)
    print("  Bank Teller Queuing Simulation — Results Summary")
    print(f"  Simulation: {sim_duration} min | {num_rep} Replications "
          f"| Arrival rate: {arrival_mean} min")
    print("=" * 60)


def print_recommendation(overall_a, overall_b):
    """
    Computes and prints the improvement from adding a 3rd teller.
    """
    wait_reduction_pct = (
        (overall_a["avg_wait"] - overall_b["avg_wait"]) / overall_a["avg_wait"]
    ) * 100

    util_a = overall_a["utilization_pct"]
    util_b = overall_b["utilization_pct"]

    print("\n" + "=" * 60)
    print("RECOMMENDATION: Adding a 3rd teller reduces average wait")
    print(f"time by ~{wait_reduction_pct:.1f}% "
          f"(from {overall_a['avg_wait']:.2f} min to {overall_b['avg_wait']:.2f} min).")
    print(f"Teller utilization drops from {util_a:.1f}% to {util_b:.1f}%.")
    print("=" * 60)
