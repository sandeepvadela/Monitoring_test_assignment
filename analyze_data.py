#  Data Analysis for Transaction Monitoring
import pandas as pd
import json

def analyze_transaction_data():
    """Analyze CSV data and set up monitoring thresholds"""
    
    print("📊 Analyzing transaction data...")
    
    try:
        # Load the transaction data
        transactions = pd.read_csv('../transactions.csv')
        transactions_auth = pd.read_csv('../transactions_auth_codes.csv')
        
        print(f"Loaded {len(transactions)} transactions")
        print(f"Loaded {len(transactions_auth)} auth codes")
        
        # Basic analysis
        print("\n=== TRANSACTION STATUS ANALYSIS ===")
        status_counts = transactions['status'].value_counts()
        print(status_counts)
        
        print("\n=== AUTH CODE ANALYSIS ===")
        auth_counts = transactions_auth['auth_code'].value_counts()
        print(auth_counts)
        
        # basic statistics by status
        print("\n=== STATISTICS BY STATUS ===")
        stats_by_status = transactions.groupby('status')['count'].agg(['mean', 'std', 'min', 'max'])
        print(stats_by_status)
        
        # thresholds based on data
        thresholds = {
            'failed_high': int(stats_by_status.loc['failed', 'mean'] + 2 * stats_by_status.loc['failed', 'std']),
            'denied_high': int(stats_by_status.loc['denied', 'mean'] + 2 * stats_by_status.loc['denied', 'std']),
            'reversed_high': int(stats_by_status.loc['reversed', 'mean'] + 2 * stats_by_status.loc['reversed', 'std']),
            'approved_low': int(stats_by_status.loc['approved', 'mean'] - 2 * stats_by_status.loc['approved', 'std']),
            'approved_high': int(stats_by_status.loc['approved', 'mean'] + 2 * stats_by_status.loc['approved', 'std'])
        }
        
        # Ensure minimum thresholds
        thresholds['failed_high'] = max(thresholds['failed_high'], 5)
        thresholds['denied_high'] = max(thresholds['denied_high'], 10)
        thresholds['reversed_high'] = max(thresholds['reversed_high'], 5)
        thresholds['approved_low'] = max(thresholds['approved_low'], 90)
        thresholds['approved_high'] = max(thresholds['approved_high'], 150)
        
        print("\n=== RECOMMENDED THRESHOLDS ===")
        for key, value in thresholds.items():
            print(f"{key}: {value}")
        
        # Save thresholds to file
        with open('recommended_thresholds.json', 'w') as f:
            json.dump(thresholds, f, indent=2)
        
        print(f"\n✅ Thresholds saved to 'recommended_thresholds.json'")
        print("\n=== NEXT STEPS ===")
        print("1. Copy these thresholds to app.py")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
        print("4. Test with the dashboard buttons!")
        
        return thresholds
        
    except FileNotFoundError:
        print(" Error: CSV files not found!")
        print("Make sure transactions.csv and transactions_auth_codes.csv are in the parent directory")
        return None
    except Exception as e:
        print(f" Error: {str(e)}")
        return None

if __name__ == '__main__':
    analyze_transaction_data() 