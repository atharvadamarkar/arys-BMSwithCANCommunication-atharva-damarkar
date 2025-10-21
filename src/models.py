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
        """Update SOC using Coulomb counting"""
        if self.active:
            delta_soc = -current * dt / (self.capacity * 3600) * 100     # demo accelerated
            self.soc += delta_soc
            self.soc = max(0, min(100, self.soc))
            # Update voltage based on SOC (linear placeholder)
            self.voltage = 3.0 + 1.2 * (self.soc / 100)

            # Temperature rise for demo
            self.temp += abs(current) * 0.25

    def voltage_correction(self):
        """Adjust SOC based on voltage measurement"""
        voltage_soc = (self.voltage - 3.0) / (4.2 - 3.0) * 100
        self.soc = 0.8 * self.soc + 0.2 * voltage_soc
        self.soc = max(0, min(100, self.soc))
        # Update voltage again after SOC correction
        self.voltage = 3.0 + 1.2 * (self.soc / 100)


class BatteryPack:
    """2s2p battery pack"""
    def __init__(self):
        base_soc = 100
        soc_offsets = [0, -1, 1, -2]  # small SOC imbalance
        self.cells = [Cell() for _ in range(4)]
        for i, cell in enumerate(self.cells):
            cell.soc = base_soc + soc_offsets[i]
            cell.voltage = 3.0 + 1.2 * (cell.soc / 100)
        self.active = True
        self.series_pairs = [(0, 1), (2, 3)]

    def pack_voltage(self):
        """Compute pack terminal voltage for 2s2p"""
        v_s1 = self.cells[0].voltage + self.cells[1].voltage
        v_s2 = self.cells[2].voltage + self.cells[3].voltage
        return 0.5 * (v_s1 + v_s2)

    def update(self, current, dt):
        """Update cells with pack current"""
        if not self.active:
            current = 0
        n_parallel = 2
        current_per_string = current / n_parallel if n_parallel else 0
        for (i, j) in self.series_pairs:
            self.cells[i].update(current_per_string, dt)
            self.cells[j].update(current_per_string, dt)
            # Voltage-based SOC correction
            self.cells[i].voltage_correction()
            self.cells[j].voltage_correction()


class FaultMonitor:
    """Monitor battery faults"""
    def __init__(self, overvoltage=4.2, undervoltage=3.5, overtemp=30, undertemp=0,
                 imbalance_threshold=0.05, overcurrent=None):
        self.overvoltage = overvoltage
        self.undervoltage = undervoltage
        self.overtemp = overtemp
        self.undertemp = undertemp
        self.imbalance_threshold = imbalance_threshold
        self.overcurrent = overcurrent

    def check(self, pack, pack_current=0.0):
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

        # Overcurrent
        if self.overcurrent is not None and abs(pack_current) > self.overcurrent:
            faults.append("Overcurrent Detected")

        return faults

    def shutdown(self, pack):
        pack.active = False
        for cell in pack.cells:
            cell.active = False
        print("Pack shutdown triggered!")

    def cooling(self, pack):
        for cell in pack.cells:
            if cell.temp > self.overtemp:
                cell.temp -= 1
        print("Cooling system activated!")

    def balancing(self, pack):
        avg_soc = sum(cell.soc for cell in pack.cells) / 4
        soc_diff = max(cell.soc for cell in pack.cells) - min(cell.soc for cell in pack.cells)

        if avg_soc > 90 and soc_diff > self.imbalance_threshold * 100:
            for cell in pack.cells:
                cell.soc += (avg_soc - cell.soc) * 0.5
                cell.voltage = 3.0 + 1.2 * (cell.soc / 100)
            print("Balancing cells (high SOC)...")
        else:
            print("Balancing skipped (conditions not met).")
