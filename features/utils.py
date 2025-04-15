import pandas as pd

def convert_time_to_seconds(time_obj):
    """Convert timedelta or pandas Timestamp to seconds."""
    if pd.isnull(time_obj):
        return None
    return time_obj.total_seconds()

def is_dry_race(compounds_used) -> bool:
    """Returns True if a race is dry based on compound data."""
    wet_compounds = {'WET', 'INTERMEDIATE'}
    return not any(comp in wet_compounds for comp in compounds_used)

def filter_clean_laps(df: pd.DataFrame) -> pd.DataFrame:
    """Removes in-laps, out-laps, and laps with missing or deleted lap times."""
    return df[
        (df['LapTime'].notna()) &
        (~df['IsInlap']) &
        (~df['IsOutlap']) &
        (~df['Deleted']) &
        (df['LapTime_sec'].notna())
    ].copy()

def normalize_driver_name(driver_id: str) -> str:
    """Normalize driver ID for comparison between sources (optional placeholder)."""
    return driver_id.strip().upper()

def get_stint_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Returns one row per stint with compound, driver, length."""
    return df.drop_duplicates(subset=['Driver', 'Stint'])[['Driver', 'Stint', 'Compound', 'StintLength']]

#example usage
#from features.utils import filter_clean_laps, convert_time_to_seconds

# Clean before training model
#clean_df = filter_clean_laps(enriched_races['2023_Bahrain_Grand_Prix'])
