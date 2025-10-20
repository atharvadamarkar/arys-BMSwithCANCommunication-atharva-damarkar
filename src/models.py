class Cell:
    """Single battery cell model"""
    def __init__(self, voltage=3.7, capacity=2.5, internal_resistance=0.05, temp=25):
        self.voltage = voltage
        self.capacity = capacity  # Ah
        self.internal_resistance = internal_resistance  # Ohms
        self.temp = temp  # Celsius
        self.soc = 100  # initial SOC (%)
        self.active = True  # for shutdown effect

    def update(self, current, dt):
        """Update SOC and voltage (stops if cell inactive due to shutdown)"""
        if self.active:
            # Gradual SOC drop
            delta_soc = -current * dt / (self.capacity * 3600) * 100 * 5
            self.soc += delta_soc
            self.soc = max(0, min(100, self.soc))
            self.voltage = 3.7 * (self.soc / 100)

            # Simple temperature rise due to current
            self.temp += abs(current) * 0.25  # small heating effect


class BatteryPack:
    """2s2p battery pack"""
    def __init__(self):
        base_soc = 100
        soc_offsets = [0, -1, 1, -2]  # small SOC imbalance
        self.cells = [Cell() for _ in range(4)]
        for i, cell in enumerate(self.cells):
            cell.soc = base_soc + soc_offsets[i]
            cell.voltage = 3.7 * (cell.soc / 100)
        self.active = True  # pack shutdown

    def pack_voltage(self):
        # Correct 2s2p voltage: series string voltage
        series1 = self.cells[0].voltage + self.cells[1].voltage
        return series1

    def update(self, current, dt):
        """Update cells with pack current (0 if shutdown)"""
        if not self.active:
            current = 0
        for cell in self.cells:
            cell.update(current, dt)


class FaultMonitor:
    """Monitor battery faults"""
    def __init__(self, overvoltage=4.2, undervoltage=3.5, overtemp=30, undertemp=0, imbalance_threshold=0.05):
        self.overvoltage = overvoltage
        self.undervoltage = undervoltage
        self.overtemp = overtemp
        self.undertemp = undertemp
        self.imbalance_threshold = imbalance_threshold  # fraction (0.05 = 5%)

    def check(self, pack):
        faults = []
        voltages = [cell.voltage for cell in pack.cells]
        temps = [cell.temp for cell in pack.cells]
        socs = [cell.soc for cell in pack.cells]

        # Voltage faults
        for i, v in enumerate(voltages):
            if v > self.overvoltage:
                faults.append(f"Cell {i} Overvoltage")
            if v < self.undervoltage:
                faults.append(f"Cell {i} Undervoltage")

        # Temperature faults
        for i, t in enumerate(temps):
            if t > self.overtemp:
                faults.append(f"Cell {i} Overtemperature")
            if t < self.undertemp:
                faults.append(f"Cell {i} Undertemperature")

        # SOC imbalance
        if max(socs) - min(socs) > self.imbalance_threshold * 100:
            faults.append("SOC Imbalance Detected")

        return faults

    def shutdown(self, pack):
        pack.active = False
        for cell in pack.cells:
            cell.active = False
        print("Pack shutdown triggered!")

    def cooling(self, pack):
        for cell in pack.cells:
            if cell.temp > self.overtemp:
                cell.temp -= 1  # cooling effect
        print("Cooling system activated!")

    def balancing(self, pack):
        avg_soc = sum(cell.soc for cell in pack.cells) / 4
        soc_diff = max(cell.soc for cell in pack.cells) - min(cell.soc for cell in pack.cells)

        # Balancing only near full charge and when imbalance is significant
        if avg_soc > 90 and soc_diff > self.imbalance_threshold * 100:
            for cell in pack.cells:
                cell.soc += (avg_soc - cell.soc) * 0.5  # simple proportional correction
                cell.voltage = 3.7 * (cell.soc / 100)
            print("Balancing cells (high SOC)...")
        else:
            print("Balancing skipped (conditions not met).")
