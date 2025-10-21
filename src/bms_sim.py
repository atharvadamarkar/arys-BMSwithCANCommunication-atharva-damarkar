from models import BatteryPack, FaultMonitor
import matplotlib.pyplot as plt

def simulate_pack(duration_sec=100, dt=1):
    pack = BatteryPack()
    monitor = FaultMonitor(overcurrent=2.0)  # Example threshold: 2A

    time_log, voltage_log, soc_log = [], [], []
    shutdown_times = []  # store tuples: (time, reason)
    cooling_times, balancing_times = [], []

    for t in range(0, duration_sec, dt):
        # Simulate current (overcurrent at t=50s for demo)
        current = 3.0 if t == 50 else 1.0
        pack.update(current, dt)

        # Check faults including overcurrent
        faults = monitor.check(pack, pack_current=current)
        if faults:
            print(f"Time {t}s: Faults -> {faults}")

            # Determine shutdown reason if applicable
            shutdown_reason = None
            if any("Overcurrent" in f for f in faults):
                shutdown_reason = "Overcurrent"
            elif any("Undervoltage" in f or "Overvoltage" in f for f in faults):
                shutdown_reason = "Over/Undervoltage"

            # Trigger actions
            if shutdown_reason and pack.active:
                monitor.shutdown(pack)
                shutdown_times.append((t, shutdown_reason))

            if "SOC Imbalance Detected" in faults:
                monitor.balancing(pack)
                balancing_times.append(t)
            if any("Overtemperature" in f for f in faults):
                monitor.cooling(pack)
                cooling_times.append(t)

        # Print debug info
        for i, cell in enumerate(pack.cells):
            print(f"Cell {i}: V={cell.voltage:.2f}V, SOC={cell.soc:.1f}%, Temp={cell.temp:.1f} degree C")

        time_log.append(t)
        voltage_log.append(pack.pack_voltage())
        soc_log.append(sum(cell.soc for cell in pack.cells)/len(pack.cells))

    # Plot pack voltage and average SOC
    plt.figure(figsize=(12,6))
    plt.plot(time_log, voltage_log, label='Pack Voltage (V)')
    plt.plot(time_log, soc_log, label='Average SOC (%)')

    # Mark shutdowns with reason
    for t, reason in shutdown_times:
        plt.axvline(t, color='red', linestyle='--', label='Shutdown')
        plt.text(t, max(voltage_log), f'Shutdown ({reason})', color='red', rotation=90, va='top')

    # Mark cooling and balancing events
    for t in cooling_times:
        plt.scatter(t, voltage_log[t], color='blue', marker='o', s=80, label='Cooling')
    for t in balancing_times:
        plt.scatter(t, soc_log[t], color='green', marker='s', s=80, label='Balancing')

    # Avoid duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.xlabel('Time (s)')
    plt.ylabel('Voltage / SOC')
    plt.title('2s2p Battery Pack Simulation with Realistic Fault Actions')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    simulate_pack()
