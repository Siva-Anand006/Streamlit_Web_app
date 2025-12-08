# airport_analysis.py
import pandas as pd
import numpy as np


# ----------------------------
# Convert stats into DataFrames
# ----------------------------

def make_queue_df(stats):

    df = pd.DataFrame({
        "time": stats["queue_time"],
        "checkin_queue": stats["queue_checkin"],
        "security_queue": stats["queue_security"],
    })
    return df


def make_distribution_df(stats):

    df = pd.DataFrame({
        "wait_checkin": pd.Series(stats["wait_checkin"]),
        "wait_security": pd.Series(stats["wait_security"]),
        "system_time": pd.Series(stats["system_times"]),
    })

    return df


def make_timeline_df(stats):

    df = pd.DataFrame(stats["timeline"])
    df = df.sort_values("arrival")
    return df


# ----------------------------
# SLA (Service Level Analysis)
# ----------------------------

def compute_sla(stats, wait_thresholds=[5, 10, 15]):

    results = {}
    waits = np.array(stats["wait_security"])

    for t in wait_thresholds:
        if len(waits) == 0:
            results[f"SLA_sec_{t}min"] = 0.0
        else:
            results[f"SLA_sec_{t}min"] = np.mean(waits < t * 60)

    return results


# ----------------------------
# Throughput
# ----------------------------

def compute_throughput(stats, sim_time):

    pax = len(stats["system_times"])
    hours = sim_time / 3600
    return pax / hours if hours > 0 else 0.0


# ----------------------------
# Utilization Chart Data
# ----------------------------

def make_utilization_df(results):

    df = pd.DataFrame({
        "resource": ["Check-in", "Security"],
        "utilization": [
            results["util_checkin"],
            results["util_security"],
        ]
    })
    return df
