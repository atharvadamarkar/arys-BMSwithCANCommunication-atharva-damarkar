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
