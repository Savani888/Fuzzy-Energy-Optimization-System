import pandas as pd
from src.fuzzy_model import create_fuzzy_system, compute_efficiency

def process_data(file_path, sample_size=100):
    """
    Reads the household power consumption dataset, cleans it, and applies 
    the fuzzy logic model to compute Energy Efficiency.
    """
    # Read the dataset
    df = pd.read_csv(file_path, low_memory=False)
    
    # The dataset uses '?' for missing values
    df.replace('?', pd.NA, inplace=True)
    
    # Drop rows with missing values in the columns we care about
    df.dropna(subset=['Global_active_power', 'Global_intensity'], inplace=True)
    
    # Convert string columns to float
    df['Global_active_power'] = df['Global_active_power'].astype(float)
    df['Global_intensity'] = df['Global_intensity'].astype(float)
    
    # Sample the data to avoid extremely long computation times
    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42).copy()
        
    sim, _, _, _ = create_fuzzy_system()
    
    efficiencies = []
    for _, row in df.iterrows():
        power = row['Global_active_power']
        demand = row['Global_intensity']
        eff = compute_efficiency(sim, power, demand)
        efficiencies.append(eff)
        
    df['Energy_Efficiency'] = efficiencies
    return df
