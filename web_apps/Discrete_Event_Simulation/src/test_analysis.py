from airport_sim import run_airport_sim
from airport_analysis import *

results, stats = run_airport_sim(sim_time=3600)

queue_df = make_queue_df(stats)
dist_df = make_distribution_df(stats)
timeline_df = make_timeline_df(stats)
sla = compute_sla(stats, wait_thresholds=[5,10,15])
util_df = make_utilization_df(results)

print("\n--- Queue Data ---")
print(queue_df.head())

print("\n--- Distributions ---")
print(dist_df.describe())

print("\n--- Timeline Sample ---")
print(timeline_df.head())

print("\n--- SLA ---")
print(sla)

print("\n--- Utilization ---")
print(util_df)
