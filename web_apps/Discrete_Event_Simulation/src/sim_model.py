def bank_sim(num_customers=100,
             interarrival_mean=2.0,
             service_mean=1.5,
             seed=42):

    import simpy
    import random
    import statistics

    random.seed(seed)

    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)

    wait_times = []
    system_times = []
    service_times = []
    arrival_times = []

    def customer(env, name, server):
        arrival = env.now
        arrival_times.append(arrival)

        with server.request() as req:
            yield req

            wait = env.now - arrival
            wait_times.append(wait)

            service_time = random.expovariate(1.0 / service_mean)
            service_times.append(service_time)

            yield env.timeout(service_time)

            system_time = env.now - arrival
            system_times.append(system_time)

    def customer_generator(env, server):
        for i in range(num_customers):
            interarrival = random.expovariate(1.0 / interarrival_mean)
            yield env.timeout(interarrival)
            env.process(customer(env, f"Customer {i+1}", server))

    env.process(customer_generator(env, server))
    env.run()

    results = {
        "num_customers": num_customers,
        "simulation_end_time": env.now,
        "avg_wait": statistics.mean(wait_times) if wait_times else 0.0,
        "avg_system_time": statistics.mean(system_times) if system_times else 0.0,
        "max_wait": max(wait_times) if wait_times else 0.0,
        "server_utilization": (
            sum(service_times) / (env.now * server.capacity)
            if env.now > 0 else 0.0
        ),
    }

    return results, wait_times, system_times, arrival_times
