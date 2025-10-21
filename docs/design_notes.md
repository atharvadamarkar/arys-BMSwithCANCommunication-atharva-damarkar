# Design Notes

## Project Scope

- Simulate a 2s2p BMS pack with:
  - Cell voltage, SOC, temperature tracking
  - Fault detection: over/undervoltage, over/undertemp, SOC imbalance
  - Pack-level actions: shutdown, cooling, balancing
  - CAN message simulation for VCU communication

## Project Structure

- `src/` : BMS source code
- `tests/` : Unit tests
- `data/` : Input/output data
- `plots/` : Simulation outputs
- `docs/` : Documentation
