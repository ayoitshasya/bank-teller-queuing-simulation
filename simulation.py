# simulation.py
# Team Member 1: Core Simulation Engine
# Implements the bank teller queuing model using SimPy.
# Customers arrive randomly (Poisson process) and wait in a
# single FIFO queue served by one or more tellers.

import simpy
import random
import numpy as np


def customer(env, name, teller, service_mean, results):
    """
    Represents a single customer going through the bank.

    Steps:
      1. Arrive at the bank → record arrival time
      2. Request a teller (may have to wait in queue)
      3. Get served → sample service time
      4. Leave → record wait and departure times
    """
    arrival_time = env.now

    # Request a teller — this may block if all tellers are busy
    with teller.request() as request:
        yield request  # Wait until a teller is free

        wait_time = env.now - arrival_time  # Time spent in queue

        # Sample how long this customer takes to be served
        service_time = random.expovariate(1.0 / service_mean)
        yield env.timeout(service_time)  # Simulate service

        departure_time = env.now

        # Store this customer's data for later analysis
        results["customers"].append({
            "name": name,
            "arrival": arrival_time,
            "wait": wait_time,
            "service": service_time,
            "departure": departure_time,
        })


def arrival_process(env, teller, arrival_mean, service_mean, results):
    """
    Generates customers arriving at the bank over time.
    Inter-arrival times follow an exponential distribution
    (i.e., a Poisson arrival process with mean = arrival_mean minutes).
    """
    customer_id = 0
    while True:
        # Wait until the next customer arrives
        inter_arrival = random.expovariate(1.0 / arrival_mean)
        yield env.timeout(inter_arrival)

        customer_id += 1

        # Record queue length at this moment (before new customer joins)
        queue_len = len(teller.queue)
        results["queue_over_time"].append((env.now, queue_len))

        # Launch a new customer process (non-blocking — runs concurrently)
        env.process(customer(env, f"C{customer_id}", teller, service_mean, results))


def run_simulation(num_tellers, num_replications, sim_duration,
                   arrival_mean=3.0, service_mean=5.0, base_seed=42):
    """
    Runs the bank teller simulation for a given number of replications.

    Parameters:
      num_tellers      – Number of tellers available (capacity of the resource)
      num_replications – How many independent runs to perform
      sim_duration     – How long each run lasts (in minutes)
      arrival_mean     – Mean inter-arrival time in minutes (default: 3)
      service_mean     – Mean service time in minutes (default: 5)
      base_seed        – Base random seed for reproducibility

    Returns:
      A list of result dicts, one per replication.
    """
    all_results = []

    for rep in range(num_replications):
        # Each replication gets a different but deterministic seed
        random.seed(base_seed + rep)

        # Initialize a fresh SimPy environment for this replication
        env = simpy.Environment()

        # The teller counter — shared resource with FIFO queue (default)
        teller = simpy.Resource(env, capacity=num_tellers)

        # Dictionary to collect data during this replication
        results = {
            "customers": [],        # One entry per customer
            "queue_over_time": [],  # (time, queue_length) snapshots
        }

        # Start the arrival process and run the simulation
        env.process(arrival_process(env, teller, arrival_mean, service_mean, results))
        env.run(until=sim_duration)

        all_results.append(results)

    return all_results
