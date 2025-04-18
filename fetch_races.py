from data.fetch_fastf1 import fetch_race_laps

print("🔥 Starting selective race fetch...")

# Only fetch Bahrain GP from multiple years
race_laps = fetch_race_laps(race_name='Bahrain Grand Prix', years=[2019, 2020, 2021, 2022, 2023, 2024])

print(f"✅ Total races fetched: {len(race_laps)}")
