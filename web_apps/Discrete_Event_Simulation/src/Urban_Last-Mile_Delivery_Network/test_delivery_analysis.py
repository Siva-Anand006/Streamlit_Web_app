from delivery_sim import run_delivery_sim
from delivery_analysis import (
    make_order_df,
    make_driver_utilization_df,
    make_driver_trips_df,
    compute_sla,
    compute_throughput,
    compute_summary_stats
)

results, stats = run_delivery_sim()

order_df = make_order_df(stats)
util_df = make_driver_utilization_df(results)
trips_df = make_driver_trips_df(stats)
sla = compute_sla(order_df)
throughput = compute_throughput(results)
summary = compute_summary_stats(order_df)

print("\n=== ORDER DATA SAMPLE ===")
print(order_df.head())

print("\n=== DRIVER UTILIZATION ===")
print(util_df)

print("\n=== DRIVER TRIPS ===")
print(trips_df)

print("\n=== SLA RESULTS ===")
print(sla)

print("\n=== THROUGHPUT ===")
print(f"{throughput:.2f} deliveries per hour")

print("\n=== SUMMARY STATS ===")
print(summary)
