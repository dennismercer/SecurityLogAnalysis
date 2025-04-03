
import sys
import os
import argparse
from pathlib import Path
import pandas as pd

# Ensure source modules in /src are discoverable during execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from cleaning import load_process_events, save_cleaned_process_events
from integration import load_cleaned_data, unify_event_stream, save_unified_stream
from process_tree import build_process_tree, write_process_tree_markdown_safe
from errors import write_error_report
from visualizations import (
    plot_event_type_distribution,
    plot_event_timeline,
    plot_top_talkers
)
from llm_summarizer import summarize_event
from mitre_lookup import enrich_with_mitre

def clean_and_save(df_loader, input_file, output_file):
    df = df_loader(input_file)
    df.to_csv(output_file, index=False)
    return df

def run_pipeline(input_dir: str, output_dir: str, test_mode: bool = False):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    data_path = output_path / "data"
    reports_path = output_path / "reports"

    data_path.mkdir(parents=True, exist_ok=True)
    reports_path.mkdir(parents=True, exist_ok=True)

    print("Cleaning all input datasets...")

    # Clean and normalize process event logs
    process_df = load_process_events(input_path / "process_events.csv")
    process_df.to_csv(data_path / "cleaned_process_events.csv", index=False)

    # Clean and normalize network events
    network_df = pd.read_csv(input_path / "network_events.csv")
    network_df.drop_duplicates(inplace=True)
    network_df.replace("###CORRUPT###", pd.NA, inplace=True)
    network_df['timestamp'] = pd.to_datetime(network_df['timestamp'], errors='coerce')
    network_df.dropna(subset=['timestamp', 'dst_ip', 'user'], inplace=True)
    network_df['src_ip'] = network_df['src_ip'].astype(str).str.strip()
    network_df['dst_ip'] = network_df['dst_ip'].astype(str).str.strip()
    network_df['user'] = network_df['user'].astype(str).str.strip()
    network_df = network_df[(network_df['timestamp'] - network_df['timestamp'].min() <= pd.Timedelta(days=366))]
    network_df.to_csv(data_path / "cleaned_network_events.csv", index=False)

    # Clean and normalize file events
    file_df = pd.read_csv(input_path / "file_events.csv")
    file_df.drop_duplicates(inplace=True)
    file_df.replace("###CORRUPT###", pd.NA, inplace=True)
    file_df['timestamp'] = pd.to_datetime(file_df['timestamp'], errors='coerce')
    file_df.dropna(subset=['timestamp', 'file_path', 'user'], inplace=True)
    file_df['file_path'] = file_df['file_path'].astype(str).str.strip()
    file_df['operation'] = file_df['operation'].astype(str).str.strip()
    file_df['user'] = file_df['user'].astype(str).str.strip()
    file_df = file_df[(file_df['timestamp'] - file_df['timestamp'].min() <= pd.Timedelta(days=366))]
    file_df.to_csv(data_path / "cleaned_file_events.csv", index=False)

    # Clean and normalize registry events
    reg_df = pd.read_csv(input_path / "registry_events.csv")
    reg_df.drop_duplicates(inplace=True)
    reg_df.replace("###CORRUPT###", pd.NA, inplace=True)
    reg_df['timestamp'] = pd.to_datetime(reg_df['timestamp'], errors='coerce')
    reg_df.dropna(subset=['timestamp', 'registry_key', 'operation', 'user'], inplace=True)
    reg_df['registry_key'] = reg_df['registry_key'].astype(str).str.strip()
    reg_df['operation'] = reg_df['operation'].astype(str).str.strip()
    reg_df['user'] = reg_df['user'].astype(str).str.strip()
    reg_df.to_csv(data_path / "cleaned_registry_events.csv", index=False)

    print("Loading cleaned datasets")
    process_df, network_df, file_df, registry_df = load_cleaned_data(data_path)

    print("Unifying event stream")
    unified_df = unify_event_stream(process_df, network_df, file_df, registry_df)

    if test_mode:
        print("Test mode enabled: limiting rows to 5 for LLM + MITRE enrichment")
        unified_df = unified_df.head(5).copy()

    unified_df.to_csv(data_path / "unified_events.csv", index=False)

    print("Summarizing events with LLM")
    unified_df["llm_summary"] = unified_df.apply(summarize_event, axis=1)

    print("Enriching with MITRE ATT&CK techniques")
    unified_df = enrich_with_mitre(unified_df)
    unified_df.to_csv(data_path / "unified_events_enriched.csv", index=False)

    print("Generating visualizations")
    plot_event_type_distribution(unified_df, reports_path / "event_type_distribution.png")
    plot_event_timeline(unified_df, reports_path / "event_timeline.png")
    plot_top_talkers(unified_df, reports_path / "top_talkers.png")

    print("Building process tree for PID 15150")
    graph = build_process_tree(process_df)
    write_process_tree_markdown_safe(graph, 15150, file_df, network_df, registry_df, reports_path / "process_tree.md")

    print("Writing error documentation")
    write_error_report(reports_path / "errors.md")

    print("All steps completed successfully.")
    print(f"  --> Enriched unified data: {data_path / 'unified_events_enriched.csv'}")
    print(f"  --> Process tree report:   {reports_path / 'process_tree.md'}")
    print(f"  --> Error documentation:   {reports_path / 'errors.md'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full synthetic log analysis pipeline.")
    parser.add_argument("--input_dir", required=True, help="Input directory with raw CSVs")
    parser.add_argument("--output_dir", required=True, help="Output directory for processed files and reports")
    parser.add_argument("--test_mode", action="store_true", help="Run in test mode with limited rows")
    args = parser.parse_args()

    run_pipeline(args.input_dir, args.output_dir, test_mode=args.test_mode)
