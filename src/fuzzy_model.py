import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_system():
    # New Antecedents/Consequents
    power = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'power')
    demand = ctrl.Antecedent(np.arange(0, 50.1, 0.1), 'demand')
    efficiency = ctrl.Consequent(np.arange(0, 101, 1), 'efficiency')

    # Membership functions for Power Consumption (kW)
    power['low'] = fuzz.trimf(power.universe, [0, 0, 5])
    power['medium'] = fuzz.trimf(power.universe, [2, 6, 10])
    power['high'] = fuzz.trimf(power.universe, [6, 12, 12])

    # Membership functions for Load Demand (A)
    demand['low'] = fuzz.trimf(demand.universe, [0, 0, 20])
    demand['medium'] = fuzz.trimf(demand.universe, [10, 25, 40])
    demand['high'] = fuzz.trimf(demand.universe, [30, 50, 50])

    # Membership functions for Efficiency (%)
    efficiency['poor'] = fuzz.trimf(efficiency.universe, [0, 0, 40])
    efficiency['average'] = fuzz.trimf(efficiency.universe, [20, 50, 80])
    efficiency['good'] = fuzz.trimf(efficiency.universe, [60, 80, 100])
    efficiency['excellent'] = fuzz.trimf(efficiency.universe, [80, 100, 100])

    # Rules
    # If Power is Low, Efficiency is generally High/Excellent (varies by demand)
    rule1 = ctrl.Rule(power['low'] & demand['low'], efficiency['excellent'])
    rule2 = ctrl.Rule(power['low'] & demand['medium'], efficiency['excellent'])
    rule3 = ctrl.Rule(power['low'] & demand['high'], efficiency['good'])

    # If Power is Medium, Efficiency is Average to Good
    rule4 = ctrl.Rule(power['medium'] & demand['low'], efficiency['average'])
    rule5 = ctrl.Rule(power['medium'] & demand['medium'], efficiency['average'])
    rule6 = ctrl.Rule(power['medium'] & demand['high'], efficiency['good'])

    # If Power is High, Efficiency is Poor to Average
    rule7 = ctrl.Rule(power['high'] & demand['low'], efficiency['poor'])
    rule8 = ctrl.Rule(power['high'] & demand['medium'], efficiency['poor'])
    rule9 = ctrl.Rule(power['high'] & demand['high'], efficiency['average'])

    efficiency_ctrl = ctrl.ControlSystem([
        rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9
    ])
    
    efficiency_sim = ctrl.ControlSystemSimulation(efficiency_ctrl)
    return efficiency_sim, power, demand, efficiency

def compute_efficiency(efficiency_sim, power_val, demand_val):
    try:
        efficiency_sim.input['power'] = power_val
        efficiency_sim.input['demand'] = demand_val
        efficiency_sim.compute()
        return efficiency_sim.output['efficiency']
    except Exception as e:
        # Handle outliers gracefully (e.g. power > 12)
        return None
