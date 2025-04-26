import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.fetch_fastf1 import fetch_race_laps

# Only fetch Bahrain GP from 2019–2024
if __name__ == "__main__":
    print("🔥 Starting race fetch...")
    fetch_race_laps(
        race_name="Bahrain Grand Prix",
        years=[2019, 2021, 2023, 2024],  # 2020 (Grosjean crash), 2022 (FastF1 error) excluded
        session_type='R',
        save_dir="data/race_laps"
    )
    print("\n✅ FastF1 race data fetching complete!")
