

🔋 BMS Simulation with CAN Communication

This repository simulates a **2s2p Battery Management System (BMS)** featuring CAN communication, real-time fault detection, pack-level actions, and a simple integrated **VCU (Vehicle Control Unit) receiver**.

---

📁 Project Structure

* `models.py` — Battery cell and pack models
* `can_utils.py` — CAN message encoding/decoding utilities
* `bms_sim.py` — Main simulation script (entry point)
* `vcu_receiver.py` — Simulated VCU receiver logic
* `tests/` — Unit tests
* `data/` — Input/output data files
* `plots/` — Simulation plots (voltage, SOC, temperature, events)
* `docs/` — Documentation and design notes

---

⚙️ Features

* Simulates **cell voltage**, **SOC**, and **temperature**
* Detects faults:

  * Overvoltage / Undervoltage
  * Overtemperature / Undertemperature
  * SOC imbalance
  * Overcurrent
* Performs **pack-level actions:**

  * **Shutdown** when critical fault occurs
  * **Cooling** during overtemperature
  * **Balancing** near full charge
* Encodes and decodes telemetry over CAN
* Integrated **VCU Receiver** prints system responses to detected faults

---

📈 Visual Outputs

The simulation generates live or saved plots showing:

* Pack voltage vs. time
* Average SOC vs. time
* Event markers for **shutdown**, **cooling**, and **balancing**

---

🚀 How to Run

1. **Install dependencies:**

   pip install -r requirements.txt


2. **Run the main simulation:**

   python bms_sim.py

3. **Observe console output:**

   * BMS fault detection logs
   * CAN message transmission
   * VCU responses (e.g., shutdown, cooling, balancing)

4. **View generated plots** after simulation is run to understand various aspects of the specific system.


✅ Notes

* Constant discharge current (1 A) is used for simplicity.
* SOC-based balancing triggers near 90% charge if imbalance > 5%.
* Overcurrent detection now triggers **pack shutdown via VCU**.
* **No separate execution of `vcu_receiver.py` is required** — it runs automatically through the main simulation.

---

🧠 AI Tools & Assistance

Tools Used: ChatGPT (OpenAI GPT-5)
How it Helped:

- Suggested improvements for simulation structure and CAN message formatting.

- Assisted in debugging logic for fault handling.

- Helped refine documentation language and organize the README/report.

---

🧾 License

This project is for educational and assignment purposes (Arys Garage, Oct 2025).

---

🔮 Future Improvements

* Add dynamic current profiles and regenerative charging
* Implement detailed thermal modeling
* Expand CAN message set with diagnostic PIDs
* Add GUI dashboard for visualization

---

💡 Repository Description (for GitHub top bar)

> Simulation of a 2s2p Battery Management System (BMS) with CAN communication, fault handling, and VCU integration.

---

🧩 Author

Atharva Damarkar
Embedded Systems & IoT Engineer | AI/ML Enthusiast
📧 atharva.damarkar80@gmail.com

📍 Pune, India
---