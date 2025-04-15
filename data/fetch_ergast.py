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

def fetch_all_race_results(start=2019, end=2024, top_n=3):
    all_years = []

    for year in range(start, end + 1):
        print(f"Fetching {year} race results from Ergast...")
        df = get_race_results(year)
        top_finishers = df[df['position'] <= top_n]
        all_years.append(top_finishers)

    result_df = pd.concat(all_years).reset_index(drop=True)
    return result_df


#usage example
#from data.fetch_ergast import fetch_all_race_results
# Get podium finishers from 2019 to 2024
#podium_df = fetch_all_race_results(top_n=3)
