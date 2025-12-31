# delivery_sim.py
import simpy
import random
import math
import statistics
from collections import defaultdict


def euclidean(p1, p2):
    """Simple Euclidean distance between two (x, y) points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def plan_route_nearest_neighbor(orders, depot=(0.0, 0.0)):
    """
    Very simple route planner:
    - Start at depot
    - Always go to the nearest undelivered order next
    Returns the orders in delivery sequence.
    """
    remaining = orders.copy()
    route = []
    current_pos = depot

    while remaining:
        # choose order whose location is nearest to current position
        nearest = min(remaining, key=lambda o: euclidean(current_pos, o["location"]))
        route.append(nearest)
        current_pos = nearest["location"]
        remaining.remove(nearest)

    return route


def order_source(env, order_store, params, stats):
    """
    Generates customer orders over time.
    Each order has:
      - created_time
      - location (x, y)
    They are put into a shared SimPy Store for drivers to pick up.
    """
    i = 0
    while env.now < params["sim_time"]:
        # time until next order
        inter = random.expovariate(1.0 / params["mean_interarrival"])
        yield env.timeout(inter)

        i += 1
        order = {
            "id": i,
            "created_time": env.now,
            "location": (
                random.uniform(-params["city_half_size"], params["city_half_size"]),
                random.uniform(-params["city_half_size"], params["city_half_size"]),
            ),
        }
        stats["orders_created"] += 1
        stats["orders_list"].append(order)
        yield order_store.put(order)


def driver(env, name, order_store, params, stats):
    """
    Each driver:
      - Waits for orders
      - Picks up a batch (up to vehicle_capacity)
      - Plans a route using nearest neighbor
      - Delivers all orders in the batch
      - Returns to depot
      - Repeats
    """
    depot = (0.0, 0.0)
    last_busy_start = None

    while True:
        batch = []

        # --- Wait for at least one order ---
        # If there are no orders, this will block
        first_order = yield order_store.get()
        batch.append(first_order)

        # Try to build up to capacity from whatever is in the store right now
        while len(batch) < params["vehicle_capacity"] and len(order_store.items) > 0:
            # Non-blocking: only take if already available
            batch.append(order_store.items.pop(0))

        # Mark driver as busy (for utilization)
        busy_start = env.now
        if last_busy_start is None:
            last_busy_start = busy_start

        # --- Plan route & deliver batch ---
        route = plan_route_nearest_neighbor(batch, depot=depot)
        current_pos = depot

        for order in route:
            dist = euclidean(current_pos, order["location"])
            travel_time = dist / params["avg_speed"] * params["traffic_factor"]
            yield env.timeout(travel_time)
            current_pos = order["location"]

            # Mark delivery
            delivered_time = env.now
            order["delivered_time"] = delivered_time
            stats["orders_delivered"] += 1
            stats["delivery_times"].append(delivered_time - order["created_time"])
            stats["per_order_records"].append(
                {
                    "order_id": order["id"],
                    "created_time": order["created_time"],
                    "delivered_time": delivered_time,
                    "delivery_time": delivered_time - order["created_time"],
                    "driver": name,
                }
            )

        # Return to depot (optional to model)
        dist_back = euclidean(current_pos, depot)
        return_time = dist_back / params["avg_speed"] * params["traffic_factor"]
        yield env.timeout(return_time)

        # Update driver busy statistics
        busy_end = env.now
        stats["driver_busy_time"][name] += (busy_end - busy_start)
        stats["driver_trips"][name] += 1


def run_delivery_sim(
    sim_time=8 * 3600,         # 8 hours
    num_drivers=5,
    vehicle_capacity=5,
    mean_interarrival=120.0,   # seconds between orders on average
    avg_speed=30.0,            # km/h
    traffic_factor=1.2,        # >1 means slower due to traffic
    city_half_size=5.0,        # "radius" of city in km (from depot at 0,0)
    seed=42,
):
    """
    Runs the last-mile delivery simulation.

    Returns:
      results: summary KPIs
      stats: raw collected data
    """
    random.seed(seed)

    env = simpy.Environment()
    order_store = simpy.Store(env)

    params = {
        "sim_time": sim_time,
        "num_drivers": num_drivers,
        "vehicle_capacity": vehicle_capacity,
        "mean_interarrival": mean_interarrival,
        "avg_speed": avg_speed / 3.6,  # convert km/h to m/s-ish scale if you want seconds; we keep units abstract
        "traffic_factor": traffic_factor,
        "city_half_size": city_half_size,
    }

    stats = {
        "orders_created": 0,
        "orders_delivered": 0,
        "orders_list": [],
        "delivery_times": [],
        "per_order_records": [],
        "driver_busy_time": defaultdict(float),
        "driver_trips": defaultdict(int),
    }

    # Start processes
    env.process(order_source(env, order_store, params, stats))

    for d in range(num_drivers):
        env.process(driver(env, f"Driver-{d+1}", order_store, params, stats))

    # Run
    env.run(until=sim_time)

    # --- KPIs ---
    def safe_mean(lst):
        return statistics.mean(lst) if lst else 0.0

    avg_delivery_time = safe_mean(stats["delivery_times"])
    orders_created = stats["orders_created"]
    orders_delivered = stats["orders_delivered"]
    backlog = orders_created - orders_delivered

    # Utilization per driver (busy_time / sim_time)
    driver_utilization = {
        name: busy / sim_time for name, busy in stats["driver_busy_time"].items()
    }

    results = {
        "sim_time": sim_time,
        "num_drivers": num_drivers,
        "vehicle_capacity": vehicle_capacity,
        "orders_created": orders_created,
        "orders_delivered": orders_delivered,
        "backlog": backlog,
        "avg_delivery_time": avg_delivery_time,
        "driver_utilization": driver_utilization,
    }

    return results, stats


# Quick test when run directly
if __name__ == "__main__":
    results, stats = run_delivery_sim()
    print("=== Last-Mile Delivery Simulation (Batched) ===")
    print(f"Simulated time: {results['sim_time'] / 3600:.1f} hours")
    print(f"Drivers: {results['num_drivers']}, Capacity per trip: {results['vehicle_capacity']}")
    print(f"Orders created:   {results['orders_created']}")
    print(f"Orders delivered: {results['orders_delivered']}")
    print(f"Backlog:          {results['backlog']}")
    print(f"Average delivery time: {results['avg_delivery_time'] / 60:.2f} minutes")

    print("\nDriver utilization:")
    for name, util in results["driver_utilization"].items():
        print(f"  {name}: {util*100:.1f}%")
