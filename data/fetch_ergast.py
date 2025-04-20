import requests
import pandas as pd

ERGAST_BASE = "https://ergast.com/api/f1"

def get_race_results(year):
    url = f"{ERGAST_BASE}/{year}/results.json?limit=1000"
    res = requests.get(url)
    data = res.json()

    races = data['MRData']['RaceTable']['Races']
    all_results = []

    for race in races:
        round_num = int(race['round'])
        race_name = race['raceName']
        date = race['date']
        circuit = race['Circuit']['circuitName']

        for result in race['Results']:
            position = int(result['position'])
            driver = result['Driver']
            constructor = result['Constructor']

            all_results.append({
                'year': year,
                'round': round_num,
                'raceName': race_name,
                'date': date,
                'circuit': circuit,
                'position': position,
                'driverId': driver['driverId'],
                'constructorId': constructor['constructorId']
            })

    return pd.DataFrame(all_results)


def fetch_race_results_for_one_gp(race_name="Bahrain Grand Prix", start=2019, end=2024, top_n=5):
    filtered_years = []

    for year in range(start, end + 1):
        print(f"Fetching {year} race results from Ergast...")
        df = get_race_results(year)

        # 🛡️ Skip if race is missing or empty
        if df.empty or 'position' not in df.columns:
            print(f"⚠️ Skipping {year} — no valid race data found.")
            continue

        # Match only the desired GP name
        match = df[df['raceName'].str.contains(race_name, case=False, regex=False)]

        if match.empty:
            print(f"⚠️ {race_name} not found in {year}")
            continue

        top_finishers = match[match['position'] <= top_n]
        filtered_years.append(top_finishers)

    if not filtered_years:
        print("❌ No matching race data found across years.")
        return pd.DataFrame()

    result_df = pd.concat(filtered_years).reset_index(drop=True)
    return result_df



#example usage
#from data.fetch_ergast import fetch_race_results_for_one_gp

#podium_df = fetch_race_results_for_one_gp(race_name="Bahrain Grand Prix", start=2019, end=2024)

