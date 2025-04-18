import fastf1
import pandas as pd
import os
from tqdm import tqdm

fastf1.Cache.enable_cache('cache')  # Enables caching to avoid repeated downloads

def fetch_race_laps(race_name='Bahrain Grand Prix', years=[2019, 2020, 2021, 2022, 2023, 2024], session_type='R', save_dir='data/race_laps'):
    os.makedirs(save_dir, exist_ok=True)
    all_races = []

    for year in years:
        try:
            schedule = fastf1.get_event_schedule(year)
        except Exception as e:
            print(f"❌ Failed to fetch schedule for {year}: {e}")
            continue

        # Find the correct row for the target race
        match = schedule[schedule['EventName'].str.contains(race_name, case=False, regex=False)]
        if match.empty:
            print(f"⚠️ {race_name} not found in {year} schedule.")
            continue

        for _, row in match.iterrows():
            try:
                print(f"⏳ Loading {year} - {row['EventName']}")
                session = fastf1.get_session(year, row['EventName'], session_type)
                session.load()
                laps = session.laps

                if laps.empty:
                    print(f"⚠️ No data for {year} - {row['EventName']}")
                    continue

                race_id = f"{year}_{row['EventName'].replace(' ', '_')}"
                laps['Race'] = race_id
                all_races.append((race_id, laps))
                laps.to_pickle(f"{save_dir}/{race_id}.pkl")
                print(f"✅ Saved: {race_id}.pkl")

            except Exception as e:
                print(f"❌ Failed to load {year} - {row['EventName']}: {e}")

    return all_races


#example usage
#from fetch_fastf1 import fetch_race_laps
#race_laps = fetch_race_laps()
