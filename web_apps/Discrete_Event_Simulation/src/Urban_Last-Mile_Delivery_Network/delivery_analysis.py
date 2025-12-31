# delivery_analysis.py

import pandas as pd
import numpy as np
import statistics


# ---------------------------------------------
# Convert raw stats into clean DataFrames
# ---------------------------------------------

def make_order_df(stats):
    """
    Returns a DataFrame of per-order delivery records:
    order_id | created_time | delivered_time | delivery_time | driver
    """
    df = pd.DataFrame(stats["per_order_records"])
    if not df.empty:
        df = df.sort_values("created_time")
    return df


def make_driver_utilization_df(results):
    """
    Returns DataFrame of utilization per driver.
    """
    util = results["driver_utilization"]
    df = pd.DataFrame({
        "driver": list(util.keys()),
        "utilization": list(util.values())
    })
    return df


def make_driver_trips_df(stats):
    """
    Returns DataFrame summarizing how many trips each driver made.
    """
    trips = stats["driver_trips"]
    df = pd.DataFrame({
        "driver": list(trips.keys()),
        "trips": list(trips.values())
    })
    return df


# ---------------------------------------------
# SLA (Service Level Agreement) calculations
# ---------------------------------------------

def compute_sla(order_df, thresholds_minutes=[30, 45, 60]):
    """
    SLA: percentage of orders delivered within threshold minutes.
    Returns dict: { 'SLA_30': 0.84, 'SLA_45': 0.92, ... }
    """
    sla = {}
    if order_df.empty:
        for t in thresholds_minutes:
            sla[f"SLA_{t}"] = 0.0
        return sla

    # Convert seconds to minutes
    delivery_min = order_df["delivery_time"] / 60.0

    for t in thresholds_minutes:
        sla[f"SLA_{t}"] = float((delivery_min <= t).mean())

    return sla


# ---------------------------------------------
# Throughput calculations
# ---------------------------------------------

def compute_throughput(results):
    """
    Throughput = delivered_orders / hours
    """
    hours = results["sim_time"] / 3600
    if hours <= 0:
        return 0.0
    return results["orders_delivered"] / hours


# ---------------------------------------------
# Summary statistics for reporting
# ---------------------------------------------

def compute_summary_stats(order_df):
    """
    Provides summary stats for delivery times.
    """
    if order_df.empty:
        return {
            "mean_delivery_min": 0,
            "p90_delivery_min": 0,
            "max_delivery_min": 0
        }

    delivery_min = order_df["delivery_time"] / 60.0

    return {
        "mean_delivery_min": float(delivery_min.mean()),
        "p90_delivery_min": float(delivery_min.quantile(0.90)),
        "max_delivery_min": float(delivery_min.max()),
    }
