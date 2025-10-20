class Cell:
    """Represents a single battery cell"""
    def __init__(self, voltage=3.7, capacity=2.5, internal_resistance=0.05, temp=25):
        self.voltage = voltage
        self.capacity = capacity  # Ah
        self.internal_resistance = internal_resistance  # Ohms
        self.temp = temp
        self.soc = 100  # initial SOC (%)
    
    def update(self, current, dt):
        """Update SOC using simple coulomb counting"""
        delta_soc = -current * dt / (self.capacity * 3600) * 100
        self.soc += delta_soc
        self.soc = max(0, min(100, self.soc))
        self.voltage = 3.7 * (self.soc / 100)  # simple linear model
