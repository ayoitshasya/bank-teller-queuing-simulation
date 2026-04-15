# Bank Teller Queuing Simulation

A discrete-event simulation of a bank teller queuing system built with Python and [SimPy](https://simpy.readthedocs.io/). This is a college MS Lab project developed by a team of 3 over 5 days.

The simulation models customer arrivals, waiting queues, and teller service — then compares two staffing scenarios to help a bank manager make a data-driven decision: **Is adding a 3rd teller worth it?**

---

## Problem Statement

A bank branch currently operates with **2 tellers**. Customers arrive randomly and wait in a single FIFO queue. Management wants to know:

- How long do customers wait on average?
- How busy are the tellers?
- What is the average and peak queue length?
- Would adding a **3rd teller** meaningfully improve service?

---

## Simulation Parameters

| Parameter | Value |
|---|---|
| Customer inter-arrival time | Exponential, mean = 3 minutes |
| Service time per customer | Exponential, mean = 5 minutes |
| Simulation duration | 240 minutes (4 hours) |
| Number of replications | 10 |
| Scenario A | 2 tellers (current setup) |
| Scenario B | 3 tellers (proposed upgrade) |

---

## Project Structure

```
bank_sim/
│
├── simulation.py       # Core SimPy simulation engine
├── analysis.py         # Statistical analysis & comparison tables
├── plots.py            # Chart generation (4 PNG charts)
├── main.py             # Runner — executes both scenarios end to end
├── requirements.txt    # Python dependencies
└── output/             # Generated charts saved here
    ├── chart1_avg_wait.png
    ├── chart2_queue_over_time.png
    ├── chart3_utilization.png
    └── chart4_wait_per_replication.png
```

### File Responsibilities

**`simulation.py` — Team Member 1**
- Implements the SimPy environment, customer process, and Poisson arrival generator
- Tracks per-customer data: arrival time, wait time, service time, departure time
- Tracks queue length at every arrival event
- Exposes `run_simulation(num_tellers, num_replications, sim_duration, seed)`

**`analysis.py` — Team Member 2**
- Computes per-replication statistics: avg/max wait, avg/max queue length, teller utilization %
- Averages metrics across all replications
- Prints formatted comparison tables to the console

**`plots.py` — Team Member 3**
- Generates 4 matplotlib charts (saved as PNG to `output/`)
- Consistent color scheme: **blue** for 2-teller scenario, **green** for 3-teller scenario

**`main.py` — Shared**
- Wires all modules together
- Runs both scenarios, prints results, generates charts, prints recommendation

---

## Getting Started

### 1. Install Dependencies

```bash
pip install simpy matplotlib numpy
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Run the Simulation

```bash
python main.py
```

This will:
- Run 10 replications for each scenario (2 tellers and 3 tellers)
- Print a formatted results table to the console
- Save 4 charts to the `output/` folder

---

## Sample Console Output

```
============================================================
  Bank Teller Queuing Simulation — Results Summary
  Simulation: 240 min | 10 Replications | Arrival rate: 3.0 min
============================================================

--- Scenario A: 2 Tellers ---
Replication  Customers   Avg Wait     Max Wait     Avg Queue    Utilization
---------------------------------------------------------------------------
1            80          26.41        52.4         9.44         97.4%
2            64          0.75         4.5          0.16         61.3%
...
Overall      72.8        7.38         23.4         2.65         74.9%

--- Scenario B: 3 Tellers ---
Replication  Customers   Avg Wait     Max Wait     Avg Queue    Utilization
---------------------------------------------------------------------------
1            92          2.05         22.2         0.64         67.8%
2            80          2.13         17.7         0.95         55.4%
...
Overall      80.5        1.37         11.6         0.46         55.6%

============================================================
RECOMMENDATION: Adding a 3rd teller reduces average wait
time by ~81.4% (from 7.38 min to 1.37 min).
Teller utilization drops from 74.9% to 55.6%.
============================================================
```

---

## Output Charts

| Chart | Description |
|---|---|
| `chart1_avg_wait.png` | Bar chart — average wait time: 2 vs 3 tellers |
| `chart2_queue_over_time.png` | Line chart — queue length over time (Scenario A, Rep 1) |
| `chart3_utilization.png` | Bar chart — teller utilization % for both scenarios |
| `chart4_wait_per_replication.png` | Grouped bar chart — avg wait per replication, both scenarios |

---

## Key Findings

| Metric | 2 Tellers | 3 Tellers | Improvement |
|---|---|---|---|
| Avg Wait Time | 7.38 min | 1.37 min | ↓ 81.4% |
| Avg Queue Length | 2.65 | 0.46 | ↓ 82.6% |
| Teller Utilization | 74.9% | 55.6% | ↓ 19.3 pp |

**Conclusion:** Adding a 3rd teller is strongly recommended. It reduces average customer wait time by over 80% while keeping tellers at a healthy utilization level (~55%), avoiding both understaffing and idle capacity.

---

## Notes

- Random seeds are set per replication (`base_seed + rep`) to ensure **reproducibility**
- High variance across Scenario A replications (e.g., Rep 1 avg wait = 26 min vs Rep 2 = 0.75 min) is expected M/M/2 behavior — it illustrates why multiple replications are necessary
- The simulation uses SimPy's `Resource` with default FIFO queuing discipline

---

## Dependencies

- [SimPy](https://simpy.readthedocs.io/) — discrete-event simulation framework
- [Matplotlib](https://matplotlib.org/) — chart generation
- [NumPy](https://numpy.org/) — statistical calculations

---

## Team

Built as part of an MS Lab assignment by a team of 3 students over 5 days.
