# Bank Teller Queuing Simulation

A discrete-event simulation of a bank teller queuing system built with Python and [SimPy](https://simpy.readthedocs.io/). This is a college MS Lab project developed by a team of 3 over 5 days.

The simulation models customer arrivals, waiting queues, and teller service — then compares two staffing scenarios to help a bank manager make a data-driven decision: **Is adding more tellers worth it?**

---

## Problem Statement

A bank branch currently operates with **2 tellers**. Customers arrive randomly and wait in a single FIFO queue. Management wants to know:

- How long do customers wait on average?
- How busy are the tellers?
- What is the average and peak queue length?
- Would adding more tellers meaningfully improve service?

---

## What's New (v2)

### ✅ Interactive User Input
All simulation parameters are now entered at runtime — no need to edit the code. Just run `python main.py` and you'll be prompted for each value. Press **Enter** to accept the default.

```
============================================================
  Bank Teller Queuing Simulation — Parameter Setup
  Press Enter to accept the default value shown in [ ]
============================================================
Simulation duration (minutes) [default: 240]: 
Number of replications [default: 10]: 
Mean customer inter-arrival time (minutes) [default: 3.0]: 
Mean service time per customer (minutes) [default: 5.0]: 
Base random seed (any integer, 0 = random each run) [default: 42]: 
Current number of tellers (Scenario A) [default: 2]: 
Proposed number of tellers (Scenario B) [default: 3]: 
```

You can now compare **any** two scenarios, not just 2 vs 3 tellers. Invalid inputs fall back to their defaults automatically.

### ✅ Reproducibility Control via Seed
- **Same seed → identical output every run** (useful for presentations, reports)
- **Enter `0` as the seed** and the simulation will use a different random seed each run, giving varied results

### ✅ Actionable Recommendation
The recommendation section now explains not just *whether* to add tellers, but **how** — with 5 practical implementation steps covering staffing, workstations, queue layout, scheduling, and post-deployment monitoring.

---

## Simulation Parameters (Defaults)

| Parameter | Default Value |
|---|---|
| Customer inter-arrival time | Exponential, mean = 3 minutes |
| Service time per customer | Exponential, mean = 5 minutes |
| Simulation duration | 240 minutes (4 hours) |
| Number of replications | 10 |
| Scenario A | 2 tellers (current setup) |
| Scenario B | 3 tellers (proposed upgrade) |
| Base random seed | 42 (fixed = reproducible) |

All of these can be changed at runtime via the prompts.

---

## Project Structure

```
bank_sim/
│
├── simulation.py       # Core SimPy simulation engine
├── analysis.py         # Statistical analysis, comparison tables & recommendation
├── plots.py            # Chart generation (4 PNG charts)
├── main.py             # Runner — collects input, executes both scenarios end to end
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
- Prints formatted comparison tables and actionable recommendation to the console

**`plots.py` — Team Member 3**
- Generates 4 matplotlib charts (saved as PNG to `output/`)
- Consistent color scheme: **blue** for current-teller scenario, **green** for proposed scenario

**`main.py` — Shared**
- Collects all parameters interactively from the user
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
1. Prompt you for simulation parameters (press Enter to use defaults)
2. Run replications for both scenarios
3. Print a formatted results table to the console
4. Print a recommendation with implementation steps
5. Save 4 charts to the `output/` folder

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
  SIMULATION RECOMMENDATION
============================================================

✅ VERDICT: Add 1 more teller (2 → 3)

📊 Key Metrics:
   Avg wait time   : 7.38 min → 1.37 min  (↓ 81.4%)
   Avg queue length: 2.65 → 0.46  (↓ 82.5%)
   Teller utiliz.  : 74.9% → 55.6%  (↓ 19.3 pp)

🔧 HOW TO ADD 1 TELLER:
   Step 1 — Staff:    Hire or reassign 1 trained teller.
   Step 2 — Workstation: Set up 1 additional teller counter
            with a PC, cash drawer, and receipt printer.
   Step 3 — Queuing:  Ensure the single FIFO queue feeds all
            3 tellers (do NOT create separate per-teller lines).
   Step 4 — Schedule: Run the 3-teller setup during peak hours.
   Step 5 — Monitor:  After 2–4 weeks, compare actual wait times
            with this simulation's prediction of ~1.4 min.
============================================================
```

---

## Output Charts

| Chart | Description |
|---|---|
| `chart1_avg_wait.png` | Bar chart — average wait time: Scenario A vs B |
| `chart2_queue_over_time.png` | Line chart — queue length over time (Scenario A, Rep 1) |
| `chart3_utilization.png` | Bar chart — teller utilization % for both scenarios |
| `chart4_wait_per_replication.png` | Grouped bar chart — avg wait per replication, both scenarios |

---

## Key Findings (Default Parameters)

| Metric | 2 Tellers | 3 Tellers | Improvement |
|---|---|---|---|
| Avg Wait Time | 7.38 min | 1.37 min | ↓ 81.4% |
| Avg Queue Length | 2.65 | 0.46 | ↓ 82.5% |
| Teller Utilization | 74.9% | 55.6% | ↓ 19.3 pp |

**Conclusion:** Adding a 3rd teller is strongly recommended. It reduces average customer wait time by over 80% while keeping tellers at a healthy utilization level (~55%), avoiding both understaffing and idle capacity.

---

## Notes

- **Reproducibility:** Random seeds are fixed per replication (`base_seed + rep`). The same seed always produces the same output. Enter `0` as the seed if you want different results each run.
- **High variance in Scenario A** (e.g., Rep 1 avg wait = 26 min vs Rep 2 = 0.75 min) is expected M/M/c behavior — it illustrates why multiple replications are necessary for reliable conclusions.
- The simulation uses SimPy's `Resource` with default **FIFO** queuing discipline.
- A single shared queue feeding all tellers is always more efficient than separate per-teller lines — this is reflected in Step 3 of the recommendation.

---

## Dependencies

- [SimPy](https://simpy.readthedocs.io/) — discrete-event simulation framework
- [Matplotlib](https://matplotlib.org/) — chart generation
- [NumPy](https://numpy.org/) — statistical calculations