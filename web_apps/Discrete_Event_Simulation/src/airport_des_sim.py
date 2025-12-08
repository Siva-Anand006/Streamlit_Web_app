import streamlit as st
import pandas as pd
from airport_sim import run_airport_sim
from airport_analysis import (
    make_queue_df,
    make_distribution_df,
    make_timeline_df,
    compute_sla,
    compute_throughput,
    make_utilization_df
)


# ------------------------
# Streamlit UI
# ------------------------

st.set_page_config(page_title="Airport Simulation Dashboard", layout="wide")

st.title("✈️ Airport Passenger Flow Simulation")
st.write("A Discrete Event Simulation built using **SimPy** and visualized with **Streamlit**.")


# ------------------------
# Sidebar Inputs
# ------------------------

st.sidebar.header("Simulation Parameters")

sim_time = st.sidebar.number_input("Simulation Time (seconds)", 300, 20000, 3600, step=300)
num_checkin = st.sidebar.slider("Number of Check-in Counters", 1, 20, 4)
num_security = st.sidebar.slider("Number of Security Scanners", 1, 20, 3)
mean_interarrival = st.sidebar.number_input("Mean Interarrival Time (seconds)", 1.0, 300.0, 10.0)
mean_service_checkin = st.sidebar.number_input("Mean Check-in Service Time (sec)", 1.0, 300.0, 5.0)
mean_service_security = st.sidebar.number_input("Mean Security Service Time (sec)", 1.0, 300.0, 4.0)

run_button = st.sidebar.button("Run Simulation")


# ------------------------
# Run simulation when user clicks the button
# ------------------------

if run_button:

    with st.spinner("Running simulation..."):
        results, stats = run_airport_sim(
            sim_time=sim_time,
            num_checkin=num_checkin,
            num_security=num_security,
            mean_interarrival=mean_interarrival,
            mean_service_checkin=mean_service_checkin,
            mean_service_security=mean_service_security,
        )

    st.success("Simulation complete!")

    # ------------------------
    # KPI Metrics
    # ------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Passengers Processed", results["num_passengers"])
    col2.metric("Avg Wait at Check-in", f"{results['avg_wait_checkin']:.2f} sec")
    col3.metric("Avg Wait at Security", f"{results['avg_wait_security']:.2f} sec")
    col4.metric("Avg Time in System", f"{results['avg_time_in_system']:.2f} sec")

    # ------------------------
    # Queue Charts
    # ------------------------

    st.subheader("📈 Queue Length Over Time")

    queue_df = make_queue_df(stats)
    st.line_chart(queue_df, x="time", y=["checkin_queue", "security_queue"])

    # ------------------------
    # Wait Time Distributions
    # ------------------------

    st.subheader("⏳ Wait Time Distributions")

    dist_df = make_distribution_df(stats)

    colA, colB, colC = st.columns(3)

    colA.bar_chart(dist_df["wait_checkin"].dropna(), use_container_width=True)
    colA.caption("Check-in Wait Times")

    colB.bar_chart(dist_df["wait_security"].dropna(), use_container_width=True)
    colB.caption("Security Wait Times")

    colC.bar_chart(dist_df["system_time"].dropna(), use_container_width=True)
    colC.caption("Total Time in System")


    # ------------------------
    # Utilization
    # ------------------------

    st.subheader("⚙️ Resource Utilization")

    util_df = make_utilization_df(results)
    st.bar_chart(util_df, x="resource", y="utilization")


    # ------------------------
    # SLA Metrics
    # ------------------------

    st.subheader("🎯 SLA Metrics (Security Waiting Times)")

    sla = compute_sla(stats)
    st.json(sla)


    # ------------------------
    # Passenger Timeline Table
    # ------------------------

    st.subheader("📊 Passenger Timeline Overview")

    timeline_df = make_timeline_df(stats)
    st.dataframe(timeline_df, use_container_width=True)


else:
    st.info("Set parameters on the left and click **Run Simulation** to begin.")
