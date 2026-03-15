import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import numpy as np

# 1. Load the data
# prmon logs use whitespace separation and often have a header
def load_data(filename):
    try:
        # We use sep='\s+' because prmon uses varying spaces/tabs
        return pd.read_csv(filename, sep='\s+')
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

normal_df = load_data('normal_data.txt')
anomaly_df = load_data('anomaly_data.txt')

if normal_df is not None and anomaly_df is not None:
    # Combine datasets to simulate a continuous timeline
    df = pd.concat([normal_df, anomaly_df]).reset_index(drop=True)

    # 2. Anomaly Detection (Isolation Forest)
    # We target PSS (Proportional Set Size) as the primary RAM metric
    model = IsolationForest(contamination=0.1, random_state=42)
    df['is_anomaly'] = model.fit_predict(df[['pss']])

    # Map: -1 (anomaly) -> 1, 1 (normal) -> 0
    df['anomaly_flag'] = df['is_anomaly'].apply(lambda x: 1 if x == -1 else 0)

    # 3. Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['pss'], label='Memory Usage (PSS)', color='#1f77b4', linewidth=2)
    
    # Highlight the anomalies
    anomalies = df[df['anomaly_flag'] == 1]
    plt.scatter(anomalies.index, anomalies['pss'], color='red', label='Detected Anomaly', zorder=5)

    plt.title('CERN Warm-up: prmon Resource Monitoring & Anomaly Detection', fontsize=14)
    plt.xlabel('Time (Seconds)', fontsize=12)
    plt.ylabel('Memory Usage (KB)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save the result
    plt.savefig('anomaly_detection_report.png')
    print("✅ Success! Your analysis is complete.")
    print("📈 Plot saved as 'anomaly_detection_report.png'.")
else:
    print("❌ Critical Error: Data files not found or empty.")


