# Fuzzy Energy Optimization System

A fuzzy logic-based system designed to compute the "Energy Efficiency Level" of a household based on its power consumption and load demand.

## Overview
Using the [Household Power Consumption](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption) dataset, this system maps:
- `Global_active_power` -> Power Consumption (Input 1)
- `Global_intensity` -> Load Demand (Input 2)
To compute:
- Energy Efficiency Level (Output) [0-100%]

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd fuzzy-energy-optimization
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python main.py --data "path/to/household_power_consumption.csv" --sample 100 --plot
```

The `--plot` flag generates a `membership_functions.png` file visualizing the fuzzy logic variables.

## Testing

Run tests using pytest:
```bash
pytest tests/
```
