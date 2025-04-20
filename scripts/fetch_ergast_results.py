import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from data.fetch_ergast import fetch_race_results_for_one_gp
except ImportError as e:
    print("🚨 Import failed:", e)
    sys.exit(1)

print("📡 Starting fetch_ergast_results.py...")

# Ensure directory
save_dir = "data/ergast"
os.makedirs(save_dir, exist_ok=True)

# Fetch data
top5_df = fetch_race_results_for_one_gp(
    race_name="Bahrain Grand Prix",
    start=2019,
    end=2024,
    top_n=5
)

if top5_df.empty:
    print("⚠️ No data was returned.")
else:
    print(f"✅ Retrieved {len(top5_df)} rows")
    print(top5_df.head())
    output_path = os.path.join(save_dir, "bahrain_top5_finishers.csv")
    top5_df.to_csv(output_path, index=False)
    print(f"✅ Saved CSV to: {output_path}")
