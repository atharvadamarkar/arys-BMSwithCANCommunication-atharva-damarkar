# can_utils.py
from dataclasses import dataclass

@dataclass
class CANMessage:
    """Simple CAN message representation"""
    arbitration_id: int
    data: bytes
    dlc: int = 8  # standard 8 bytes


class CANEncoder:
    """Encode battery pack data into CAN messages"""

    def encode_pack_voltage(self, pack) -> bytes:
        """Encode total pack voltage into 2 bytes (0.01 V resolution)"""
        voltage_int = int(pack.pack_voltage() * 100)
        return voltage_int.to_bytes(2, byteorder='big')

    def encode_cell_voltages(self, pack) -> bytes:
        """Encode 4 cell voltages, 2 bytes each"""
        data = bytearray()
        for cell in pack.cells:
            v_int = int(cell.voltage * 100)
            data += v_int.to_bytes(2, byteorder='big')
        return data  # 8 bytes

    def encode_socs_and_temps(self, pack) -> bytes:
        """Encode SOCs (0-100) and temps (deg C) for 4 cells"""
        data = bytearray()
        for cell in pack.cells:
            data.append(int(cell.soc))
        for cell in pack.cells:
            data.append(int(cell.temp))
        return data  # 8 bytes total

    def encode_faults(self, faults) -> bytes:
        """Encode faults into 1 byte (bit mapping)"""
        byte = 0
        for f in faults:
            if "Overvoltage" in f: byte |= 1 << 0
            if "Undervoltage" in f: byte |= 1 << 1
            if "Overtemperature" in f: byte |= 1 << 2
            if "Undertemperature" in f: byte |= 1 << 3
            if "SOC Imbalance" in f: byte |= 1 << 4
            if "Overcurrent" in f: byte |= 1 << 5
        return byte.to_bytes(1, byteorder='big')

    def encode_pack_messages(self, pack, faults) -> list[CANMessage]:
        """Return list of CANMessages"""
        messages = [
            CANMessage(0x200, self.encode_pack_voltage(pack)),
            CANMessage(0x201, self.encode_cell_voltages(pack)),
            CANMessage(0x202, self.encode_socs_and_temps(pack)),
            CANMessage(0x203, self.encode_faults(faults))
        ]
        return messages

    def print_can_messages(self, messages):
        """Pretty print CAN messages"""
        for msg in messages:
            hex_data = " ".join(f"{b:02X}" for b in msg.data)
            msg_type = {
                0x200: "Pack Voltage",
                0x201: "Cell Voltages",
                0x202: "SOCs & Temps",
                0x203: "Faults"
            }.get(msg.arbitration_id, "Unknown")
            print(f"CAN ID: {hex(msg.arbitration_id)} ({msg_type}), Data: {hex_data}")


# ---------- NEW ADDITIONS ----------

def decode_faults(data: bytes):
    """Decode fault byte into readable list"""
    fault_names = [
        "Overvoltage", "Undervoltage", "Overtemperature",
        "Undertemperature", "SOC Imbalance", "Overcurrent"
    ]
    byte_val = data[0]
    active_faults = [name for i, name in enumerate(fault_names) if (byte_val >> i) & 1]
    return active_faults
