#pip install pandas tqdm (dependencie)
 
import os
import pandas as pd
from tqdm import tqdm

def get_available_races(fastf1_dir='data/race_laps'):
    races = []
    for file in os.listdir(fastf1_dir):
        if file.endswith('.pkl'):
            race_id = file.replace('.pkl', '')
            races.append(race_id)
    return races

def load_race_lap_data(fastf1_dir='data/race_laps'):
    race_dfs = {}
    for file in tqdm(os.listdir(fastf1_dir), desc="Loading FastF1 races"):
        if not file.endswith('.pkl'):
            continue
        race_id = file.replace('.pkl', '')
        try:
            df = pd.read_pickle(os.path.join(fastf1_dir, file))
            race_dfs[race_id] = df
        except Exception as e:
            print(f"⚠️ Could not load {file}: {e}")
    return race_dfs

def filter_dry_podium_races(race_lap_dfs, podium_df, top_n=3):
    filtered_races = {}

    for race_id, lap_df in race_lap_dfs.items():
        # Extract race year and name
        try:
            year, event = race_id.split('_', 1)
            race_matches = podium_df[(podium_df['year'] == int(year)) & (podium_df['raceName'].str.contains(event.replace('_', ' '), case=False))]
        except:
            continue

        # Filter to top N drivers only
        allowed_drivers = race_matches[race_matches['position'] <= top_n]['driverId'].str.upper().unique()

        # Normalize FastF1 driver IDs (e.g., VER, PER) vs Ergast (max_verstappen, sergio_perez)
        # You may need to create a mapping dictionary later

        # Skip if no common drivers
        f1_drivers = lap_df['Driver'].unique()
        if len(set(allowed_drivers).intersection(set(f1_drivers))) == 0:
            continue

        # Simple wet race detection (you can refine this later)
        compounds = lap_df['Compound'].unique()
        if any(c in ['WET', 'INTERMEDIATE'] for c in compounds):
            continue

        # Filter to top drivers only
        filtered_df = lap_df[lap_df['Driver'].isin(allowed_drivers)].copy()
        filtered_races[race_id] = filtered_df

    return filtered_races

#example script
#from data.fetch_ergast import fetch_all_race_results
#from data.race_filter import load_race_lap_data, filter_dry_podium_races

# Step 1: Load all lap data from FastF1
#race_laps = load_race_lap_data()

# Step 2: Get Ergast metadata
#podium_df = fetch_all_race_results(top_n=3)

# Step 3: Filter dry podium races
#clean_race_dict = filter_dry_podium_races(race_laps, podium_df, top_n=3)
