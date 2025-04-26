import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("🛠️ Starting to build the model dataset...\n")

# Paths
LAPS_DIR = "data/race_laps"
ERGAST_CSV = "data/ergast/bahrain_top5_finishers.csv"
OUTPUT_FILE = "data/model_input/bahrain_top5_laps_2019_2024.pkl"
os.makedirs("data/model_input", exist_ok=True)

# Ergast driverId → FastF1 Driver code
driver_id_to_code = {
    'max_verstappen': 'VER',
    'leclerc': 'LEC',
    'hamilton': 'HAM',
    'perez': 'PER',
    'sainz': 'SAI',
    'norris': 'NOR',
    'russell': 'RUS',
    'bottas': 'BOT',
    'gasly': 'GAS',
    'ocon': 'OCO',
    'ricciardo': 'RIC',
    'stroll': 'STR',
    'alonso': 'ALO',
    'albon': 'ALB',
    'zhou': 'ZHO',
    'tsunoda': 'TSU',
    'hulk': 'HUL',
    'magnussen': 'MAG',
    'piastri': 'PIA',
    'sargeant': 'SAR'
}

# Load top-5 finishers from Ergast
top5_df = pd.read_csv(ERGAST_CSV)
print(f"✅ Loaded top 5 drivers: {len(top5_df)} rows")

# Group by year for mapping
top5_by_year = top5_df.groupby("year")["driverId"].apply(set).to_dict()

# Collect all matching laps
all_filtered_laps = []

for file in os.listdir(LAPS_DIR):
    if not file.endswith(".pkl"):
        continue

    year = int(file.split("_")[0])
    if year not in top5_by_year:
        print(f"⏭️ Skipping {file} — no top drivers found for this year")
        continue

    path = os.path.join(LAPS_DIR, file)
    df = pd.read_pickle(path)

    # Map Ergast IDs to FastF1 codes
    top_driver_codes = {
        driver_id_to_code.get(d) for d in top5_by_year[year] if driver_id_to_code.get(d)
    }

    filtered = df[df['Driver'].isin(top_driver_codes)]
    print(f"✅ {file}: {len(filtered)} matching laps")
    all_filtered_laps.append(filtered)

# Combine and save
if all_filtered_laps:
    final_df = pd.concat(all_filtered_laps).reset_index(drop=True)
    final_df.to_pickle(OUTPUT_FILE)
    print(f"\n✅ Final dataset saved: {OUTPUT_FILE} ({len(final_df)} rows)")
else:
    print("⚠️ No matching lap data found!")
