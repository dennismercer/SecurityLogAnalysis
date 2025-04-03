
# Synthetic Security Log Analysis and Data Integration

## Overview

This project simulates real-world system activity log analysis for security threat detection. It processes a synthetic dataset containing `process`, `network`, `file`, and `registry` event logs from a single machine and generates:

- A unified, cleaned event stream
- A process tree report focused on a malicious process (`process_id = 15150`)
- Documentation of data anomalies and resolutions
- Visualizations to highlight behavior and activity patterns

---

## Folder Structure

```
project_root/
├── config/           # Reserved for config files (currently empty)
├── data/             # Raw input event datasets (CSV format)
├── reports/          # Output reports and visualizations
├── schemas/          # Reserved for schema definitions (currently empty)
├── scripts/          # Utility scripts (e.g., prepare_data.py)
├── src/              # Source code (modular pipeline logic)
├── tests/            # Reserved for unit tests (currently empty)
├── main.py           # CLI entry point for the pipeline
├── requirements.txt  # Python dependencies
└── README.md         # Project instructions and documentation
```

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Input Data

Place the following CSV files into the `/data/` folder:

- `process_events.csv`
- `network_events.csv`
- `file_events.csv`
- `registry_events.csv`

Or use the prep script to copy them from root into `/data/`:

```bash
python scripts/prepare_data.py
```

---

## Running the Pipeline

```bash
python main.py --input_dir ./data --output_dir ./reports
```

This will:
- Clean and normalize the input logs
- Generate `cleaned_*.csv` and `unified_events.csv` inside `/reports/data/`
- Generate:
  - `process_tree.md` for malicious PID 15150
  - `errors.md` describing data anomalies
  - Three visualizations:
    - `event_type_distribution.png`
    - `event_timeline.png`
    - `top_talkers.png`

---

## Key Files and Outputs

| File                                 | Description                                                   |
|--------------------------------------|---------------------------------------------------------------|
| `main.py`                            | CLI script to run the full pipeline                           |
| `src/cleaning.py`                    | Cleans and standardizes `process_events.csv`                  |
| `src/integration.py`                 | Merges all event types into a unified stream                  |
| `src/process_tree.py`                | Builds and outputs a Markdown process tree                    |
| `src/visualizations.py`              | Creates timeline and behavioral charts                        |
| `reports/data/unified_events.csv`    | Unified event log sorted chronologically                      |
| `reports/process_tree.md`            | Detailed tree of PID 15150 and child process activity         |
| `reports/errors.md`                  | Data quality issues and cleaning methodology                  |
| `reports/event_type_distribution.png`| Bar chart of event type counts                                |
| `reports/event_timeline.png`         | Time-based volume of event activity                           |
| `reports/top_talkers.png`            | Top 10 `process_id`s by total event count                     |

---

## Design Considerations

- Modular pipeline built for clarity and maintainability
- Explicit handling of data anomalies (missing values, time drift, corruption)
- Cycle-safe process tree traversal
- UTF-8 support for cross-platform Markdown compatibility
- Bonus visualizations to provide operational insight

---

## Notes

- `schemas/` and `config/` folders are included for extensibility
- No external APIs or services are used
- Output is portable and reproducible across platforms

---

## Author

This submission was completed by **Dennis Mercer** as part of the **Senior Applied AI Engineer** technical interview assessment.
