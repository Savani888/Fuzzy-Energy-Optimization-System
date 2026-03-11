import argparse
import sys
from src.data_processor import process_data

def main():
    parser = argparse.ArgumentParser(description="Fuzzy Energy Optimization System")
    parser.add_argument("--data", required=True, help="Path to household_power_consumption.csv")
    parser.add_argument("--sample", type=int, default=100, help="Number of rows to sample from the dataset (default: 100)")
    parser.add_argument("--plot", action="store_true", help="Generate and save membership function plots")
    
    args = parser.parse_args()
    
    print(f"[*] Starting Fuzzy Energy Optimization System...")
    print(f"[*] Loading data from: {args.data}")
    print(f"[*] Extracting a sample of {args.sample} records...")
    
    try:
        results = process_data(args.data, sample_size=args.sample)
    except FileNotFoundError:
        print(f"[!] Error: File not found at {args.data}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error processing data: {e}")
        sys.exit(1)
        
    # Drop failed computations (if any)
    valid_results = results.dropna(subset=['Energy_Efficiency'])
    
    if valid_results.empty:
        print("[!] No valid records were processed.")
        sys.exit(1)
        
    average_eff = valid_results['Energy_Efficiency'].mean()
    print(f"\n[+] Successfully processed {len(valid_results)} records.")
    print(f"[+] Average Energy Efficiency Level: {average_eff:.2f}%\n")
    
    print("[-] Sample Output:")
    print(valid_results[['Global_active_power', 'Global_intensity', 'Energy_Efficiency']].head(15).to_string(index=False))

    if args.plot:
        from src.visualizer import plot_membership_functions
        plot_membership_functions()

if __name__ == "__main__":
    main()
