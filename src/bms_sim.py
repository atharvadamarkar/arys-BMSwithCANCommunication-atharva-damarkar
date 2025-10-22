# bms_sim.py
from models import BatteryPack, FaultMonitor
from can_utils import CANEncoder
from vcu_receiver import VCUReceiver
import matplotlib.pyplot as plt

def simulate_pack_with_can(duration_sec=100, dt=1):
    pack = BatteryPack()
    monitor = FaultMonitor(overcurrent=2.0)
    encoder = CANEncoder()
    vcu = VCUReceiver()  # simple receiver instance

    time_log, voltage_log, soc_log = [], [], []
    shutdown_times, cooling_times, balancing_times = [], [], []
    can_messages_log = []
    fault_times = []

    for t in range(0, duration_sec, dt):
        current = 3.0 if t == 50 else 1.0
        pack.update(current, dt)

        faults = monitor.check(pack, pack_current=current)
        if faults:
            print(f"Time {t}s: Faults -> {faults}")
            fault_times.append(t)

            shutdown_reason = None
            if any("Overcurrent" in f for f in faults):
                shutdown_reason = "Overcurrent"
            elif any("Undervoltage" in f or "Overvoltage" in f for f in faults):
                shutdown_reason = "Over/Undervoltage"

            if shutdown_reason and pack.active:
                monitor.shutdown(pack)
                shutdown_times.append((t, shutdown_reason))

            if "SOC Imbalance Detected" in faults:
                monitor.balancing(pack)
                balancing_times.append(t)
            if any("Overtemperature" in f for f in faults):
                monitor.cooling(pack)
                cooling_times.append(t)

        # Encode CAN messages for pack & faults
        msgs = encoder.encode_pack_messages(pack, faults)
        can_messages_log.append(msgs)

        print(f"\nTime {t}s CAN messages:")
        encoder.print_can_messages(msgs)

        # --- Simulate VCU receiving CAN frames ---
        for msg in msgs:
            vcu.receive(msg)

        # Log voltage and SOC
        time_log.append(t)
        voltage_log.append(pack.pack_voltage())
        soc_log.append(sum(cell.soc for cell in pack.cells)/len(pack.cells))

    # (Plotting code same as before)
    plt.figure(figsize=(12,6))
    plt.plot(time_log, voltage_log, label='Pack Voltage (V)')
    plt.plot(time_log, soc_log, label='Average SOC (%)')

    for t, reason in shutdown_times:
        plt.axvline(t, color='red', linestyle='--', label='Shutdown')
        plt.text(t, max(voltage_log), f'Shutdown ({reason})', color='red', rotation=90, va='top')
    for t in cooling_times:
        plt.scatter(t, voltage_log[t], color='blue', marker='o', s=80, label='Cooling')
    for t in balancing_times:
        plt.scatter(t, soc_log[t], color='green', marker='s', s=80, label='Balancing')

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.xlabel('Time (s)')
    plt.ylabel('Voltage / SOC')
    plt.title('2s2p Battery Pack Simulation with Fault Actions + CAN + VCU')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    simulate_pack_with_can()
