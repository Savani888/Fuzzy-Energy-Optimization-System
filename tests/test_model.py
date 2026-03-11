import pytest
from src.fuzzy_model import create_fuzzy_system, compute_efficiency

def test_fuzzy_system_creation():
    sim, _, _, _ = create_fuzzy_system()
    assert sim is not None

def test_efficiency_computation_low_power_low_demand():
    sim, _, _, _ = create_fuzzy_system()
    eff = compute_efficiency(sim, 1.0, 5.0)
    # Expected excellent efficiency (> 80)
    assert eff is not None
    assert eff > 80.0

def test_efficiency_computation_high_power_low_demand():
    sim, _, _, _ = create_fuzzy_system()
    eff = compute_efficiency(sim, 10.0, 5.0)
    # Expected poor efficiency (< 40)
    assert eff is not None
    assert eff < 40.0

def test_efficiency_computation_medium_power_medium_demand():
    sim, _, _, _ = create_fuzzy_system()
    eff = compute_efficiency(sim, 6.0, 25.0)
    # Expected average efficiency (~50)
    assert eff is not None
    assert 40.0 <= eff <= 60.0
