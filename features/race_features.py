import pandas as pd

def summarize_stints_by_compound(lap_df: pd.DataFrame) -> pd.DataFrame:
    """Returns average stint lengths per compound."""
    stint_summary = lap_df.drop_duplicates(subset=['Driver', 'Stint']).groupby('Compound')['StintLength'].agg(['mean', 'std', 'count']).reset_index()
    stint_summary.columns = ['Compound', 'AvgStintLength', 'StintLengthStd', 'StintCount']
    return stint_summary

def average_pit_duration(lap_df: pd.DataFrame) -> float:
    """Returns average pit stop duration for the race."""
    pit_durations = lap_df[['Driver', 'Stint', 'PitDuration']].drop_duplicates().dropna()
    return pit_durations['PitDuration'].mean()

def compound_usage_distribution(lap_df: pd.DataFrame) -> pd.DataFrame:
    """Returns how many stints used each compound."""
    usage = lap_df.drop_duplicates(subset=['Driver', 'Stint']).groupby('Compound').size().reset_index(name='StintCount')
    return usage

def driver_strategy_summary(lap_df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes stint lengths and compounds per driver."""
    stints = lap_df.drop_duplicates(subset=['Driver', 'Stint'])[['Driver', 'Stint', 'Compound', 'StintLength']]
    return stints.sort_values(['Driver', 'Stint'])

def total_pit_stops(lap_df: pd.DataFrame) -> pd.DataFrame:
    """Returns number of pit stops per driver."""
    stops = lap_df[['Driver', 'Stint']].drop_duplicates().groupby('Driver').count().reset_index()
    stops.columns = ['Driver', 'NumStints']
    stops['PitStops'] = stops['NumStints'] - 1
    return stops

#example usage
#from features.race_features import summarize_stints_by_compound, average_pit_duration

#race_df = enriched_races['2024_Bahrain_Grand_Prix']

#print(summarize_stints_by_compound(race_df))
#print("Average Pit Duration:", average_pit_duration(race_df))
