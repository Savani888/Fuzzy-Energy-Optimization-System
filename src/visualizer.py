import matplotlib.pyplot as plt
from src.fuzzy_model import create_fuzzy_system

def plot_membership_functions(save_path="membership_functions.png"):
    """
    Generates and saves a plot of the fuzzy membership functions.
    """
    _, power, demand, efficiency = create_fuzzy_system()
    
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 12))

    # Power Consumption
    ax0.plot(power.universe, fuzz_membership_safe(power, 'low'), 'b', linewidth=1.5, label='Low')
    ax0.plot(power.universe, fuzz_membership_safe(power, 'medium'), 'g', linewidth=1.5, label='Medium')
    ax0.plot(power.universe, fuzz_membership_safe(power, 'high'), 'r', linewidth=1.5, label='High')
    ax0.set_title('Power Consumption (kW)')
    ax0.legend()

    # Load Demand
    ax1.plot(demand.universe, fuzz_membership_safe(demand, 'low'), 'b', linewidth=1.5, label='Low')
    ax1.plot(demand.universe, fuzz_membership_safe(demand, 'medium'), 'g', linewidth=1.5, label='Medium')
    ax1.plot(demand.universe, fuzz_membership_safe(demand, 'high'), 'r', linewidth=1.5, label='High')
    ax1.set_title('Load Demand (A)')
    ax1.legend()

    # Energy Efficiency
    ax2.plot(efficiency.universe, fuzz_membership_safe(efficiency, 'poor'), 'r', linewidth=1.5, label='Poor')
    ax2.plot(efficiency.universe, fuzz_membership_safe(efficiency, 'average'), 'y', linewidth=1.5, label='Average')
    ax2.plot(efficiency.universe, fuzz_membership_safe(efficiency, 'good'), 'g', linewidth=1.5, label='Good')
    ax2.plot(efficiency.universe, fuzz_membership_safe(efficiency, 'excellent'), 'b', linewidth=1.5, label='Excellent')
    ax2.set_title('Energy Efficiency Level (%)')
    ax2.legend()

    # Hide top and right spines
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"[+] Membership function plots saved to {save_path}")

def fuzz_membership_safe(variable, label):
    # Internal helper to handle skfuzzy version differences
    return variable[label].mf
