
import pandas as pd
from pathlib import Path

# Loads cleaned CSV files for all event types from the specified directory.
def load_cleaned_data(data_dir: Path):
    process_df = pd.read_csv(data_dir / "cleaned_process_events.csv", parse_dates=["start_time", "end_time"])
    network_df = pd.read_csv(data_dir / "cleaned_network_events.csv", parse_dates=["timestamp"])
    file_df = pd.read_csv(data_dir / "cleaned_file_events.csv", parse_dates=["timestamp"])
    registry_df = pd.read_csv(data_dir / "cleaned_registry_events.csv", parse_dates=["timestamp"])
    return process_df, network_df, file_df, registry_df

# Combines all event types into a single unified event stream based on process_id and timestamp.
# Each event includes a type label and descriptive metadata.#
def unify_event_stream(process_df, network_df, file_df, registry_df):
    unified_records = []

    for _, row in process_df.iterrows():
        unified_records.append({
            "timestamp": row["start_time"],
            "process_id": row["process_id"],
            "event_type": "process_start",
            "event_details": f"Executable: {row['executable_path']} | User: {row['user']}",
        })

    for _, row in network_df.iterrows():
        unified_records.append({
            "timestamp": row["timestamp"],
            "process_id": row["process_id"],
            "event_type": "network",
            "event_details": f"SrcIP: {row['src_ip']}:{row['src_port']} → DstIP: {row['dst_ip']}:{row['dst_port']} | User: {row['user']}",
        })

    for _, row in file_df.iterrows():
        unified_records.append({
            "timestamp": row["timestamp"],
            "process_id": row["process_id"],
            "event_type": "file",
            "event_details": f"Operation: {row['operation']} | File: {row['file_path']} | User: {row['user']}",
        })

    for _, row in registry_df.iterrows():
        val_str = f" | Value: {row['value_name']} = {row['value_data']}" if pd.notnull(row['value_name']) else ""
        unified_records.append({
            "timestamp": row["timestamp"],
            "process_id": row["process_id"],
            "event_type": "registry",
            "event_details": f"Operation: {row['operation']} | Key: {row['registry_key']}{val_str} | User: {row['user']}",
        })

    unified_df = pd.DataFrame(unified_records)
    unified_df.sort_values(by="timestamp", inplace=True)
    return unified_df

# Saves the unified event stream to a CSV file.
def save_unified_stream(unified_df: pd.DataFrame, output_path: Path):
    unified_df.to_csv(output_path, index=False)
