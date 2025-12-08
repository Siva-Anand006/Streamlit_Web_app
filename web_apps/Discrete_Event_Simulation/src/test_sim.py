from airport_sim import run_airport_sim

# Run the simulation for 1 hour (3600 seconds)
results, stats = run_airport_sim(sim_time=3600)

print("\n=== Airport Simulation Test Run ===")
print(f"Simulated Time: {results['sim_time']} seconds")
print(f"Passengers processed: {results['num_passengers']}")
print("---------------------------------------")
print(f"Average wait at CHECK-IN: {results['avg_wait_checkin']:.2f} sec")
print(f"Average wait at SECURITY: {results['avg_wait_security']:.2f} sec")
print(f"Average TOTAL time in system: {results['avg_time_in_system']:.2f} sec")
print("---------------------------------------")
print(f"Utilization - Check-in: {results['util_checkin']*100:.1f}%")
print(f"Utilization - Security: {results['util_security']*100:.1f}%")
print("---------------------------------------")
print(f"Max queue length (Check-in): {results['max_queue_checkin']}")
print(f"Max queue length (Security): {results['max_queue_security']}")
print("---------------------------------------")
