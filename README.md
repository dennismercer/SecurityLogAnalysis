
# Synthetic Security Log Analysis and Data Integration

## Overview

This project simulates real-world system activity log analysis for security threat detection. It processes a synthetic dataset containing `process`, `network`, `file`, and `registry` event logs from a single machine and generates:

- A unified, cleaned event stream
- LLM-generated behavioral summaries for each event
- MITRE ATT&CK enrichment for context on adversarial techniques
- A process tree report focused on a malicious process (`process_id = 15150`)
- Documentation of data anomalies and resolutions
- Visualizations to highlight behavioral trends

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

Also place:
- `enterprise-attack.json` from MITRE CTI repo into `/data/`

Or use the prep script to copy raw files from root:

```bash
python scripts/prepare_data.py
```

---

## Running the Pipeline

```bash
python main.py --input_dir ./data --output_dir ./reports
```

Optional test mode (limits LLM/MITRE processing to 5 rows):

```bash
python main.py --input_dir ./data --output_dir ./reports --test_mode
```

---

## Key Outputs

| File                                  | Description                                                      |
|---------------------------------------|------------------------------------------------------------------|
| `unified_events.csv`                  | Unified cleaned event stream                                     |
| `unified_events_enriched.csv`         | Unified log with LLM summaries and MITRE ATT&CK mappings         |
| `process_tree.md`                     | Markdown tree of PID 15150 and child activity                    |
| `errors.md`                           | Data anomalies and resolution documentation                      |
| `event_type_distribution.png`         | Bar chart showing event type frequencies                         |
| `event_timeline.png`                  | Time series of event frequency                                   |
| `top_talkers.png`                     | Top processes by number of events                                |

---

## LLM Integration

Events are summarized using OpenAI's GPT-3.5 to generate concise, security-focused behavioral interpretations. Results are stored in the `llm_summary` column of the unified output.

---

## MITRE ATT&CK Integration

LLM summaries are scanned for behavior keywords and mapped to official MITRE ATT&CK techniques from the `enterprise-attack.json` dataset. Enrichment adds:

- `mitre_technique`
- `mitre_id` (e.g., `T1059`)
- `mitre_tactic` (placeholder or extended via future release)

---

## Design Considerations

- Modular pipeline for flexibility and future expansion
- Cycle-safe graph traversal in process tree generation
- Visualizations to support quick pattern recognition
- Support for `.env`-based API key management
- Ready for async or batch LLM enhancement

---

## Notes

- `schemas/` and `config/` folders are placeholders for future expansion
- LLM model can be configured in `llm_summarizer.py`
- Test mode avoids full OpenAI billing during development

---

## Author

This submission was completed by **Dennis Mercer** as part of the **Senior Applied AI Engineer** technical interview assessment.
