# Airport Passenger Flow Simulation (SimPy + Streamlit)

A discrete-event simulation of passenger movement through airport check-in and security, built with **SimPy** and visualized through an interactive **Streamlit** dashboard. This project models passenger arrivals, queuing, and processing at key airport service points to analyze system performance, identify bottlenecks, and evaluate the impact of staffing decisions on wait times and throughput.

---

## 🔧 Features

* **Multi-stage Simulation**: Models passenger flow through check-in counters and security lanes.
* **Queue Analytics**: Tracks queue lengths, wait times, and server utilization over time.
* **Interactive Dashboard**: Streamlit-based UI for real-time parameter tuning and visualization.
* **Performance Metrics**: Calculates SLAs, throughput, average wait times, and resource efficiency.
* **Scenario Testing**: Easily adjust parameters like arrival rate, service times, and server counts.
* **Passenger-level Logging**: Detailed timeline for each passenger from arrival to exit.

---

## Project Structure

```
airport-simulation/
├── airport_des_sim.py        # Streamlit web application (main app)
├── airport_sim.py            # Core SimPy simulation model
├── airport_analysis.py       # Analytics utilities & DataFrame builders
├── test_sim.py               # Quick offline simulation test
├── test_analysis.py          # Analytics layer test
├── requirements.txt          # Dependencies
└── README.md                 # This file

---

## How It Works

Passengers are modeled as SimPy processes that move through two main service stages:

1. **Check‑in counters** – multiple parallel servers.
2. **Security scanners** – another set of parallel servers.

Each passenger’s journey is event‑driven:

* Arrival at the airport  
* Join check‑in queue → get served  
* Move to security queue → get scanned  
* Exit the system  

The simulation logs:

* Waiting times per stage
* Service times
* Queue lengths over time
* Server utilization
* Total system time per passenger
* Individual passenger timelines

Data is aggregated and visualized in the Streamlit dashboard for interactive analysis.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/airport-sim.git
cd airport-sim
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
The app will open automatically in your browser.

---

## 🧪 Running Tests

You can run the simulation and analytics modules directly:

```bash
# Run a quick simulation test
python test_sim.py

# Test analytics and DataFrame generation
python test_analysis.py
```

---

## 📊 Dashboard Overview

The Streamlit interface includes:

### **1. KPI Summary**
* Total passengers processed
* Average waiting times per stage
* Mean total system time

### **2. Queue Length Over Time**
* Real‑time charts for check‑in and security queues

### **3. Wait Time Distributions**
* Histograms for check‑in, security, and total time

### **4. Resource Utilization**
* Percentage of time servers are busy

### **5. SLA Compliance**
* Share of passengers processed within 5, 10, and 15 minutes

### **6. Passenger Timeline Table**
* Step‑by‑step timeline for each passenger (arrival → check‑in → security → exit)

---

## Adjustable Parameters

Use the sidebar to modify:

* **Simulation duration** (seconds)
* **Number of check‑in counters**
* **Number of security scanners**
* **Mean interarrival time**
* **Mean check‑in service time**
* **Mean security service time**

Example scenarios:
* “What if we add two more security lanes?”
* “How do wait times change during peak arrivals?”
* “What’s the effect of adding another check‑in counter?”

---

## Skills Demonstrated

* Discrete‑event simulation with SimPy
* Queueing theory and bottleneck analysis
* Interactive dashboard development with Streamlit
* Data processing and visualization for operational analytics
* Scenario‑based performance modeling
* Python engineering for simulation and analytics

---

## Deployment

Ready to deploy on **Streamlit Community Cloud**:

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Select your repository and point to `app.py`.
4. The app will build automatically and receive a public URL.

---

## 📄 License

MIT License. You are free to use, modify, and distribute this project.

---
