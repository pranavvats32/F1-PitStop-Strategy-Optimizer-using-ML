import pandas as pd
import numpy as np

def extract_lap_features(lap_df: pd.DataFrame) -> pd.DataFrame:
    df = lap_df.copy()

    # ✅ Lap time in seconds
    df['LapTime_sec'] = df['LapTime'].dt.total_seconds()

    # ✅ Tyre warmup — fresh tyre flag
    df['IsFreshTyre'] = df['FreshTyre'].fillna(False)

    # ✅ Tyre degradation — delta between consecutive laps in same stint
    df['DegradationPerLap'] = df.groupby(['Driver', 'Stint'])['LapTime_sec'].diff().fillna(0)

    # ✅ Performance life — average compound pace per tyre life
    compound_perf = df.groupby(['Compound', 'TyreLife'])['LapTime_sec'].mean().reset_index()
    compound_perf.columns = ['Compound', 'TyreLife', 'AvgCompoundPace']
    df = df.merge(compound_perf, on=['Compound', 'TyreLife'], how='left')

    # ✅ Wear life — total stint length
    stint_len = df.groupby(['Driver', 'Stint'])['LapNumber'].count().reset_index()
    stint_len.columns = ['Driver', 'Stint', 'StintLength']
    df = df.merge(stint_len, on=['Driver', 'Stint'], how='left')

    # ✅ Pit stop duration — calculated from PitIn and PitOut
    df = df.sort_values(by=['Driver', 'LapNumber']).reset_index(drop=True)
    df['NextPitOutTime'] = df.groupby('Driver')['PitOutTime'].shift(-1)
    df['PitDuration'] = (df['NextPitOutTime'] - df['PitInTime']).dt.total_seconds()
    df.loc[df['PitDuration'] <= 0, 'PitDuration'] = np.nan

    return df
