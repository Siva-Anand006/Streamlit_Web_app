import streamlit as st
import pandas as pd

from delivery_sim import run_delivery_sim
from delivery_analysis import (
    make_order_df,
    make_driver_utilization_df,
    make_driver_trips_df,
    compute_sla,
    compute_throughput,
    compute_summary_stats,
)

# ------------------------
# Page config
# ------------------------
st.set_page_config(
    page_title="Last-Mile Delivery Simulation",
    layout="wide"
)

st.title("🚚 Last-Mile Delivery Simulation (Batched Orders)")
st.write(
    "Simulates a last-mile delivery operation with multiple orders per trip, "
    "using **SimPy** for the discrete-event simulation and **Streamlit** for visualization."
)

# ------------------------
# Sidebar: parameters
# ------------------------

st.sidebar.header("Simulation Parameters")

sim_time_hours = st.sidebar.number_input(
    "Simulation Time (hours)", min_value=1.0, max_value=24.0, value=8.0, step=1.0
)
sim_time = sim_time_hours * 3600  # convert to seconds

num_drivers = st.sidebar.slider(
    "Number of Drivers", min_value=1, max_value=50, value=5, step=1
)

vehicle_capacity = st.sidebar.slider(
    "Vehicle Capacity (orders per trip)", min_value=1, max_value=20, value=5, step=1
)

mean_interarrival = st.sidebar.number_input(
    "Mean Time Between Orders (seconds)",
    min_value=10.0, max_value=3600.0, value=120.0, step=10.0
)

avg_speed = st.sidebar.number_input(
    "Average Speed (km/h)",
    min_value=5.0, max_value=80.0, value=30.0, step=1.0
)

traffic_factor = st.sidebar.number_input(
    "Traffic Factor ( >1 = slower )",
    min_value=0.5, max_value=3.0, value=1.2, step=0.1
)

city_half_size = st.sidebar.number_input(
    "City Half-Size (km from depot)",
    min_value=1.0, max_value=50.0, value=5.0, step=1.0
)

seed = st.sidebar.number_input(
    "Random Seed", min_value=0, max_value=999999, value=42, step=1
)

run_button = st.sidebar.button("Run Simulation")

# ------------------------
# Main: run + display
# ------------------------

if run_button:
    with st.spinner("Running simulation..."):
        results, stats = run_delivery_sim(
            sim_time=sim_time,
            num_drivers=num_drivers,
            vehicle_capacity=vehicle_capacity,
            mean_interarrival=mean_interarrival,
            avg_speed=avg_speed,
            traffic_factor=traffic_factor,
            city_half_size=city_half_size,
            seed=seed,
        )

        order_df = make_order_df(stats)
        util_df = make_driver_utilization_df(results)
        trips_df = make_driver_trips_df(stats)
        sla = compute_sla(order_df)
        throughput = compute_throughput(results)
        summary = compute_summary_stats(order_df)

    st.success("Simulation complete!")

    # ------------------------
    # Top-level KPIs
    # ------------------------
    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Orders Created", results["orders_created"])
    col2.metric("Orders Delivered", results["orders_delivered"])
    col3.metric("Backlog (Undelivered)", results["backlog"])
    col4.metric(
        "Throughput (deliveries/hour)",
        f"{throughput:.2f}"
    )

    col5, col6, col7 = st.columns(3)
    col5.metric(
        "Avg Delivery Time (min)",
        f"{summary['mean_delivery_min']:.1f}"
    )
    col6.metric(
        "90th Percentile Delivery Time (min)",
        f"{summary['p90_delivery_min']:.1f}"
    )
    col7.metric(
        "Max Delivery Time (min)",
        f"{summary['max_delivery_min']:.1f}"
    )

    # ------------------------
    # SLA section
    # ------------------------
    st.subheader("🎯 SLA Performance (Delivery Time Targets)")
    st.write("SLA = % of orders delivered within the specified time window.")

    sla_cols = st.columns(len(sla) if sla else 1)
    for (label, value), c in zip(sla.items(), sla_cols):
        minutes = label.split("_")[1]
        c.metric(
            f"<= {minutes} minutes",
            f"{value*100:.1f} %"
        )

    # ------------------------
    # Driver metrics
    # ------------------------
    st.subheader("🧑‍✈️ Driver Utilization & Trips")

    c1, c2 = st.columns(2)

    if not util_df.empty:
        util_plot_df = util_df.copy()
        util_plot_df["util_percent"] = util_plot_df["utilization"] * 100.0
        c1.bar_chart(util_plot_df.set_index("driver")["util_percent"])
        c1.caption("Driver utilization (%)")

    if not trips_df.empty:
        c2.bar_chart(trips_df.set_index("driver")["trips"])
        c2.caption("Trips per driver")

    # ------------------------
    # Delivery time distribution
    # ------------------------
    st.subheader("⏱ Delivery Time Distribution")

    if not order_df.empty:
        order_df_display = order_df.copy()
        order_df_display["delivery_min"] = order_df_display["delivery_time"] / 60.0

        st.bar_chart(order_df_display["delivery_min"])
        st.caption("Delivery times (minutes)")

    # ------------------------
    # Orders table
    # ------------------------
    st.subheader("📦 Order-Level Details")

    if not order_df.empty:
        display_cols = [
            "order_id",
            "created_time",
            "delivered_time",
            "delivery_time",
            "driver",
        ]
        df_display = order_df[display_cols].copy()
        df_display["delivery_time_min"] = df_display["delivery_time"] / 60.0
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No orders were delivered in this run. Try increasing simulation time or reducing interarrival time.")

else:
    st.info("Set parameters in the sidebar and click **Run Simulation** to start.")
