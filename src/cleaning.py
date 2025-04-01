
import pandas as pd
import numpy as np

"""
    Cleans and normalizes the process_events dataset.

    - Removes duplicates and corrupted markers
    - Parses and validates timestamps
    - Strips extra whitespace from key fields
    - Filters invalid relationships and time drift
    """
def load_process_events(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    df.replace("###CORRUPT###", np.nan, inplace=True)
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
    df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    df.dropna(subset=['start_time', 'end_time'], inplace=True)
    df = df[df['end_time'] >= df['start_time']]
    min_time = df['start_time'].min()
    df = df[(df['start_time'] - min_time <= pd.Timedelta(days=366))]
    for col in ['executable_path', 'user', 'command_line']:
        df[col] = df[col].astype(str).str.strip()
    df = df[df['process_id'] != df['parent_id']]
    return df

def save_cleaned_process_events(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)
