def write_error_report(output_path):
    # Write summary of data quality issues and fixes
    content = """\
# Data Quality Issues and Resolutions

This report documents the anomalies encountered during the cleaning and normalization process.

---

## Common Fixes Applied Across All Datasets

- Duplicate Entries: Removed using `drop_duplicates()`.
- Corrupted Data: Replaced `###CORRUPT###` markers with `NaN` and dropped where necessary.
- Missing Timestamps: Dropped rows where key datetime fields could not be parsed or were missing.
- Time Drift: Removed events more than 1 year beyond the earliest timestamp.
- Whitespace: Trimmed from all string fields.

---

## Process Events
- Dropped inverted or corrupt timestamps
- Removed self-referential rows
- Cycle-safe DFS to prevent infinite loops

## Network Events
- Retained rows with missing `src_ip` if `dst_ip` and `user` present
- Dropped rows missing `dst_ip`, `user`, or `timestamp`

## File Events
- Retained rows with missing `operation`
- Cleaned timestamps and file path strings

## Registry Events
- Retained sparse `value_name` and `value_data`
- Cleaned `registry_key`, `operation`, and `user` fields

---

## Summary

All datasets were cleaned and normalized using consistent rules. The pipeline handles anomalies gracefully and ensures high-integrity output for analysis.
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
