
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_event_type_distribution(df: pd.DataFrame, output_path: Path):
    event_counts = df["event_type"].value_counts()
    plt.figure(figsize=(8, 5))
    event_counts.plot(kind="bar", color="#4A90E2", edgecolor="black")
    plt.title("Event Type Distribution")
    plt.xlabel("Event Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    print(f"Saved: {output_path}")

def plot_event_timeline(df: pd.DataFrame, output_path: Path):
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df.set_index('timestamp', inplace=True)
    timeline = df.resample('1Min').size()

    plt.figure(figsize=(10, 4))
    timeline.plot()
    plt.title("Event Volume Over Time")
    plt.xlabel("Time")
    plt.ylabel("Event Count")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved: {output_path}")

def plot_top_talkers(df: pd.DataFrame, output_path: Path):
    top_processes = df["process_id"].value_counts().head(10)
    plt.figure(figsize=(8, 5))
    top_processes.plot(kind="bar", color="#7B68EE", edgecolor="black")
    plt.title("Top 10 Processes by Event Count")
    plt.xlabel("Process ID")
    plt.ylabel("Event Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize unified event data")
    parser.add_argument("--input_csv", required=True, help="Path to unified_events.csv")
    parser.add_argument("--output_dir", required=True, help="Directory to save all charts")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    output_dir = Path(args.output_dir)
    plot_event_type_distribution(df, output_dir / "event_type_distribution.png")
    plot_event_timeline(df, output_dir / "event_timeline.png")
    plot_top_talkers(df, output_dir / "top_talkers.png")
