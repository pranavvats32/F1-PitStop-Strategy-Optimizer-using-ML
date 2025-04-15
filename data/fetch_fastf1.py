import fastf1
import pandas as pd
import os
from tqdm import tqdm

fastf1.Cache.enable_cache('cache')  # Enables caching to avoid repeated downloads

def fetch_race_laps(years=[2019, 2020, 2021, 2022, 2023, 2024], session_type='R', save_dir='data/race_laps'):
    os.makedirs(save_dir, exist_ok=True)
    
    race_schedule = {
        year: fastf1.get_event_schedule(year) for year in years
    }

    all_races = []

    for year, schedule in race_schedule.items():
        for _, row in schedule.iterrows():
            if row['Session5'] != session_type:  # some races may lack full session data
                continue
            
            gp_name = row['EventName'].replace(' ', '_')
            race_id = f"{year}_{gp_name}"

            try:
                print(f"⏳ Loading {race_id}")
                session = fastf1.get_session(year, row['EventName'], session_type)
                session.load()
                laps = session.laps
                if laps.empty:
                    print(f"⚠️ No data for {race_id}")
                    continue

                laps['Race'] = race_id
                all_races.append((race_id, laps))
                
                # Save per race
                laps.to_pickle(f"{save_dir}/{race_id}.pkl")

            except Exception as e:
                print(f"❌ Failed to load {race_id}: {e}")
    
    return all_races

#example usage
#from fetch_fastf1 import fetch_race_laps
#race_laps = fetch_race_laps()
