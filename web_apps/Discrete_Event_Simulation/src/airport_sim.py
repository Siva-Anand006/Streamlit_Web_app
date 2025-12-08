# airport_sim.py

import simpy
import random
import statistics


def passenger(env, name, check_in, security, params, stats):
    arrival_time = env.now  # passenger arrival to system

    # Record timeline start
    timeline = {"name": name, "arrival": arrival_time}

    # ===== CHECK-IN =====
    timeline["ci_queue_len"] = len(check_in.queue)

    with check_in.request() as req:
        yield req

        start_ci = env.now
        timeline["start_checkin"] = start_ci

        wait_ci = start_ci - arrival_time
        stats["wait_checkin"].append(wait_ci)

        service_time_ci = random.expovariate(1.0 / params["mean_service_checkin"])
        yield env.timeout(service_time_ci)

        finish_ci = env.now
        timeline["finish_checkin"] = finish_ci

        # Track server busy time
        stats["busy_checkin"] += service_time_ci

    # ===== SECURITY =====
    timeline["sec_queue_len"] = len(security.queue)

    with security.request() as req:
        yield req

        start_sec = env.now
        timeline["start_security"] = start_sec

        wait_sec = start_sec - finish_ci
        stats["wait_security"].append(wait_sec)

        service_time_sec = random.expovariate(1.0 / params["mean_service_security"])
        yield env.timeout(service_time_sec)

        finish_sec = env.now
        timeline["finish_security"] = finish_sec

        # Track server busy time
        stats["busy_security"] += service_time_sec

    # Total time in system
    total_time = env.now - arrival_time
    stats["system_times"].append(total_time)

    # Save passenger timeline
    stats["timeline"].append(timeline)


def passenger_arrivals(env, check_in, security, params, stats):
    i = 0
    while True:
        interarrival = random.expovariate(1.0 / params["mean_interarrival"])
        yield env.timeout(interarrival)

        i += 1
        env.process(passenger(env, f"Passenger {i}", check_in, security, params, stats))


def track_queue_lengths(env, check_in, security, stats, sample_interval=10):
    """
    Every sample_interval seconds, record queue lengths.
    This is ESSENTIAL for plotting time-series queue charts.
    """
    while True:
        stats["queue_time"].append(env.now)
        stats["queue_checkin"].append(len(check_in.queue))
        stats["queue_security"].append(len(security.queue))
        yield env.timeout(sample_interval)


def run_airport_sim(
    sim_time=3600,
    num_checkin=4,
    num_security=3,
    mean_interarrival=10.0,
    mean_service_checkin=5.0,
    mean_service_security=4.0,
    sample_interval=10,
    seed=42,
):

    random.seed(seed)
    env = simpy.Environment()

    check_in = simpy.Resource(env, capacity=num_checkin)
    security = simpy.Resource(env, capacity=num_security)

    params = {
        "mean_interarrival": mean_interarrival,
        "mean_service_checkin": mean_service_checkin,
        "mean_service_security": mean_service_security,
    }

    stats = {
        "wait_checkin": [],
        "wait_security": [],
        "system_times": [],
        "timeline": [],

        # Queue length tracking
        "queue_time": [],
        "queue_checkin": [],
        "queue_security": [],

        # Busy time tracking
        "busy_checkin": 0.0,
        "busy_security": 0.0,
    }

    # Start processes
    env.process(passenger_arrivals(env, check_in, security, params, stats))
    env.process(track_queue_lengths(env, check_in, security, stats, sample_interval))

    env.run(until=sim_time)

    # KPI helper
    def safe_mean(lst):
        return statistics.mean(lst) if lst else 0.0

    # Utilization = busy time / (servers * total time)
    util_checkin = stats["busy_checkin"] / (num_checkin * sim_time)
    util_security = stats["busy_security"] / (num_security * sim_time)

    results = {
        "sim_time": sim_time,
        "num_passengers": len(stats["system_times"]),

        "avg_wait_checkin": safe_mean(stats["wait_checkin"]),
        "avg_wait_security": safe_mean(stats["wait_security"]),
        "avg_time_in_system": safe_mean(stats["system_times"]),

        "util_checkin": util_checkin,
        "util_security": util_security,

        "max_queue_checkin": max(stats["queue_checkin"]) if stats["queue_checkin"] else 0,
        "max_queue_security": max(stats["queue_security"]) if stats["queue_security"] else 0,
    }

    return results, stats

