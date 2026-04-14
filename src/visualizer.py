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


def plot_rule_viewer(efficiency_sim, power_var, demand_var, efficiency_var, 
                     sample_power=6.0, sample_demand=25.0, save_path=None):
    """
    Visualizes the fuzzy rule activation for a sample input.
    Shows membership degrees, input activations, and inferred output.
    
    Args:
        efficiency_sim: ControlSystemSimulation object
        power_var, demand_var, efficiency_var: Fuzzy variable objects
        sample_power: Sample power value for visualization (kW)
        sample_demand: Sample demand value for visualization (A)
        save_path: Optional path to save figure (PNG)
    """
    import numpy as np
    
    # Compute output for the sample input
    efficiency_sim.input['power'] = sample_power
    efficiency_sim.input['demand'] = sample_demand
    efficiency_sim.compute()
    output_efficiency = efficiency_sim.output['efficiency']
    
    # Create figure with 6 subplots
    fig = plt.figure(figsize=(15, 10))
    
    # ========== SUBPLOT 1: Power Input Memberships ==========
    ax1 = plt.subplot(2, 3, 1)
    power_labels = ['low', 'medium', 'high']
    for label in power_labels:
        ax1.plot(power_var.universe, fuzz_membership_safe(power_var, label),
                linewidth=2, label=label)
    ax1.axvline(sample_power, color='red', linestyle='--', linewidth=2.5, 
               label=f'Input: {sample_power} kW')
    ax1.fill_between(power_var.universe, 0, 1, alpha=0.1, color='red')
    ax1.set_title('Power Input Memberships', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Power (kW)')
    ax1.set_ylabel('Membership Degree')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 2: Demand Input Memberships ==========
    ax2 = plt.subplot(2, 3, 2)
    demand_labels = ['low', 'medium', 'high']
    for label in demand_labels:
        ax2.plot(demand_var.universe, fuzz_membership_safe(demand_var, label),
                linewidth=2, label=label)
    ax2.axvline(sample_demand, color='red', linestyle='--', linewidth=2.5,
               label=f'Input: {sample_demand} A')
    ax2.fill_between(demand_var.universe, 0, 1, alpha=0.1, color='red')
    ax2.set_title('Demand Input Memberships', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Demand (A)')
    ax2.set_ylabel('Membership Degree')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 3: Output Efficiency ==========
    ax3 = plt.subplot(2, 3, 3)
    eff_labels = ['poor', 'average', 'good', 'excellent']
    for label in eff_labels:
        ax3.plot(efficiency_var.universe, fuzz_membership_safe(efficiency_var, label),
                linewidth=2, label=label)
    ax3.axvline(output_efficiency, color='green', linestyle='--', linewidth=2.5,
               label=f'Output: {output_efficiency:.2f}%')
    ax3.fill_between(efficiency_var.universe, 0, 1, alpha=0.1, color='green')
    ax3.set_title('Energy Efficiency Output', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Efficiency (%)')
    ax3.set_ylabel('Membership Degree')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 4: Power Membership Activation Bar Chart ==========
    ax4 = plt.subplot(2, 3, 4)
    # Extract membership values at the sample power point
    power_idx = np.argmin(np.abs(power_var.universe - sample_power))
    power_mf_values = {
        label: fuzz_membership_safe(power_var, label)[power_idx]
        for label in power_labels
    }
    bars = ax4.bar(power_mf_values.keys(), power_mf_values.values(),
                   color=['blue', 'green', 'red'], alpha=0.7, edgecolor='black')
    ax4.set_title(f'Power Activation at {sample_power} kW', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Membership Degree')
    ax4.set_ylim([0, 1.1])
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # ========== SUBPLOT 5: Demand Membership Activation Bar Chart ==========
    ax5 = plt.subplot(2, 3, 5)
    # Extract membership values at the sample demand point
    demand_idx = np.argmin(np.abs(demand_var.universe - sample_demand))
    demand_mf_values = {
        label: fuzz_membership_safe(demand_var, label)[demand_idx]
        for label in demand_labels
    }
    bars = ax5.bar(demand_mf_values.keys(), demand_mf_values.values(),
                   color=['blue', 'green', 'red'], alpha=0.7, edgecolor='black')
    ax5.set_title(f'Demand Activation at {sample_demand} A', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Membership Degree')
    ax5.set_ylim([0, 1.1])
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    
    # ========== SUBPLOT 6: Summary Information ==========
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    summary_text = f"""FUZZY INFERENCE SUMMARY

Sample Input Values:
  • Power: {sample_power} kW
  • Demand: {sample_demand} A

Computed Output:
  • Energy Efficiency: {output_efficiency:.2f}%

Membership Activations:

Power Domain:
  │ Low: {power_mf_values['low']:.3f}
  │ Medium: {power_mf_values['medium']:.3f}
  │ High: {power_mf_values['high']:.3f}

Demand Domain:
  │ Low: {demand_mf_values['low']:.3f}
  │ Medium: {demand_mf_values['medium']:.3f}
  │ High: {demand_mf_values['high']:.3f}

Interpretation:
  The input activates multiple fuzzy sets with
  different degrees. All activated rules fire and
  contribute to the final efficiency output via
  centroid defuzzification (center of gravity)."""
    
    ax6.text(0.05, 0.95, summary_text, fontsize=10, verticalalignment='top',
            family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle('Fuzzy Logic RULE VIEWER - Sample Input Analysis', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    # Save figure to file
    if not save_path:
        save_path = 'rule_viewer.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"[+] Rule viewer saved to {save_path}")
    plt.close()


def plot_surface_viewer(efficiency_sim, power_var, demand_var, efficiency_var,
                       resolution=30, save_path=None):
    """
    Generates a 3D surface plot and contour map showing the relationship 
    between power consumption, load demand, and energy efficiency.
    
    Args:
        efficiency_sim: ControlSystemSimulation object
        power_var, demand_var, efficiency_var: Fuzzy variable objects
        resolution: Grid resolution for evaluation (e.g., 30 = 30x30 grid)
        save_path: Optional path to save figure (PNG)
    """
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    
    # ========== GENERATE EVALUATION GRID ==========
    # Create evenly-spaced samples across input domains
    power_range = np.linspace(power_var.universe.min(), power_var.universe.max(), resolution)
    demand_range = np.linspace(demand_var.universe.min(), demand_var.universe.max(), resolution)
    power_mesh, demand_mesh = np.meshgrid(power_range, demand_range)
    
    # ========== EVALUATE FUZZY SYSTEM ACROSS GRID ==========
    # For each (power, demand) pair, compute the efficiency output
    efficiency_mesh = np.zeros_like(power_mesh, dtype=float)
    
    for i in range(resolution):
        for j in range(resolution):
            try:
                efficiency_sim.input['power'] = power_mesh[i, j]
                efficiency_sim.input['demand'] = demand_mesh[i, j]
                efficiency_sim.compute()
                efficiency_mesh[i, j] = efficiency_sim.output['efficiency']
            except Exception:
                # Handle out-of-range inputs gracefully
                efficiency_mesh[i, j] = np.nan
    
    # ========== CREATE VISUALIZATION ==========
    fig = plt.figure(figsize=(16, 6))
    
    # ========== SUBPLOT 1: 3D Surface Plot ==========
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Plot surface with gradient colormap (red=low efficiency, green=high efficiency)
    surf = ax1.plot_surface(power_mesh, demand_mesh, efficiency_mesh,
                           cmap=cm.RdYlGn, alpha=0.85, edgecolor='none', rstride=1, cstride=1)
    
    ax1.set_xlabel('Power Consumption (kW)', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Load Demand (A)', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_zlabel('Energy Efficiency (%)', fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_title('3D Input-Output Surface', fontsize=12, fontweight='bold', pad=20)
    
    # Set viewing angle for better visualization
    ax1.view_init(elev=25, azim=45)
    
    # Add colorbar for surface plot
    cbar1 = fig.colorbar(surf, ax=ax1, label='Efficiency (%)', shrink=0.6, aspect=8, pad=0.1)
    
    # ========== SUBPLOT 2: Contour Plot (Top View) ==========
    ax2 = fig.add_subplot(122)
    
    # Create filled contour plot with 15 levels
    contourf = ax2.contourf(power_mesh, demand_mesh, efficiency_mesh,
                            levels=15, cmap=cm.RdYlGn, alpha=0.85)
    
    # Add contour lines for reference
    contour_lines = ax2.contour(power_mesh, demand_mesh, efficiency_mesh,
                               levels=10, colors='black', alpha=0.4, linewidths=0.8)
    
    # Label contour lines with efficiency values
    ax2.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f%%')
    
    ax2.set_xlabel('Power Consumption (kW)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Load Demand (A)', fontsize=11, fontweight='bold')
    ax2.set_title('Efficiency Contour Map (Top View)', fontsize=12, fontweight='bold')
    
    # Add colorbar for contour plot
    cbar2 = fig.colorbar(contourf, ax=ax2, label='Efficiency (%)')
    
    plt.suptitle(f'Fuzzy Energy Optimization System - SURFACE VIEWER (Resolution: {resolution}×{resolution})',
                fontsize=13, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save figure to file
    if not save_path:
        save_path = 'surface_viewer.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"[+] Surface viewer saved to {save_path}")
    plt.close()
