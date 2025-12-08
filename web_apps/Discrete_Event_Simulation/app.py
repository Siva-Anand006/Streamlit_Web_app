# app.py
import streamlit as st
from src.sim_model import bank_sim  # import the function we just defined


st.title("Simple Queue Simulation with SimPy 🏦")

st.markdown(
    """
This app simulates a simple **single-server queue** (like one ATM or counter)
using **SimPy**.  
Use the controls on the sidebar to change the parameters and then run the simulation.
"""
)

# Sidebar inputs
st.sidebar.header("Simulation parameters")

num_customers = st.sidebar.slider("Number of customers", 10, 500, 100)
interarrival_mean = st.sidebar.number_input(
    "Mean interarrival time", min_value=0.1, value=2.0, step=0.1
)
service_mean = st.sidebar.number_input(
    "Mean service time", min_value=0.1, value=1.5, step=0.1
)
seed = st.sidebar.number_input("Random seed", min_value=0, value=42, step=1)

if st.button("Run simulation"):
    results, wait_times, system_times, arrival_times = bank_sim(
        num_customers=num_customers,
        interarrival_mean=interarrival_mean,
        service_mean=service_mean,
        seed=seed,
    )

    st.subheader("Key Results")
    st.write(f"**Number of customers:** {results['num_customers']}")
    st.write(f"**Simulation end time:** {results['simulation_end_time']:.2f}")
    st.write(f"**Average waiting time:** {results['avg_wait']:.2f}")
    st.write(f"**Average time in system:** {results['avg_system_time']:.2f}")
    st.write(f"**Maximum waiting time:** {results['max_wait']:.2f}")
    st.write(f"**Server utilization:** {results['server_utilization']:.2%}")

    st.subheader("Distributions")

    st.markdown("**Waiting times (per customer)**")
    st.line_chart(wait_times)

    st.markdown("**Time in system (per customer)**")
    st.line_chart(system_times)
else:
    st.info("Set your parameters on the left and click **Run simulation**.")
