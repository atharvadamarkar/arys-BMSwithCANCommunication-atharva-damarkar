# vcu_receiver.py
from can_utils import decode_faults

class VCUReceiver:
    """Simple simulated Vehicle Control Unit (VCU)"""

    def __init__(self):
        self.system_shutdown = False  # Latches when a critical fault occurs

    def receive(self, can_msg):
        """Process a received CAN message"""
        # If system is already shut down, ignore further messages
        if self.system_shutdown:
            print("[VCU] System SHUTDOWN - awaiting manual reset.")
            return

        if can_msg.arbitration_id == 0x203:  # Fault message
            faults = decode_faults(can_msg.data)

            # If no faults
            if not faults:
                print("[VCU] System normal.")
                return

            # If faults exist
            print(f"[VCU] Received Faults: {faults}")

            # Handle individual fault types
            if "Overcurrent" in faults:
                print("[VCU] Overcurrent detected — initiating PACK SHUTDOWN.")
                self.system_shutdown = True
                return  # Stop processing further

            if "Overtemperature" in faults:
                print("[VCU] Cooling system activated.")

            if "SOC Imbalance" in faults:
                print("[VCU] Balancing command issued.")

    def manual_reset(self):
        """Simulate manual reset after shutdown"""
        if self.system_shutdown:
            print("[VCU] Manual reset performed. System back to normal state.")
            self.system_shutdown = False
        else:
            print("[VCU] System already normal. No reset needed.")
