Simulate a 2s2p battery pack, estimate SOC(voltage + coulomb counting), detect faults, implement shutdown/cooling/balancing and encode telemetry oven CAN.
# BMS Simulation with CAN Communication

This repository contains a simulation of a 2s2p Battery Management System (BMS) with CAN communication.

## Project Structure

- `src/` : Source code for BMS simulation
- `tests/` : Unit tests
- `data/` : Input/output data files
- `plots/` : Generated plots from simulation
- `docs/` : Documentation and design notes

## Features

- Simulates cell voltage, SOC, and temperature
- Detects faults: over/undervoltage, over/undertemperature, SOC imbalance
- Implements pack-level actions: shutdown, cooling, balancing
- Real-time monitoring plots

The simulation also implements the following actions:

- **Shutdown:** disables the pack and cells when critical faults occur
- **Cooling:** reduces temperature if overtemperature is detected
- **Balancing:** corrects SOC imbalance near full charge

Visual plots are generated to show:

- Pack voltage vs time  
- Average SOC vs time  
- Event markers for shutdown, cooling, and balancing


## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt

2. Run the simulation:
python src/bms_sim.py

3. View the plots and console outputs for cell voltage, SOC, temperature, and events.

Notes:-
- Current is constant in the simulation for simplicity (1 A).
- SOC-based balancing occurs near full charge (>90%) only if the imbalance exceeds threshold (5%).

- Future improvements: add CAN communication, overcurrent handling, and more realistic dynamic loads.