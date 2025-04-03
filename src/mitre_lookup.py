
import json
import pandas as pd
from pathlib import Path

MITRE_PATH = Path("data/enterprise-attack.json")

def load_attack_techniques():
    with open(MITRE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    techniques = []
    for obj in data["objects"]:
        if obj.get("type") == "attack-pattern" and "external_references" in obj:
            attack_id = next(
                (ref["external_id"] for ref in obj["external_references"] if ref.get("source_name") == "mitre-attack"),
                None
            )
            name = obj.get("name", "Unknown")
            description = obj.get("description", "").lower()
            techniques.append({
                "id": attack_id,
                "name": name,
                "description": description
            })
    return techniques

def match_mitre_dynamic(summary, techniques):
    if not isinstance(summary, str):
        summary = str(summary)
    summary = summary.lower()
    
    for tech in techniques:
        if tech["id"] is None:
            continue
        if tech["name"].lower() in summary or tech["description"][:300] in summary:
            return pd.Series({
                "mitre_technique": tech["name"],
                "mitre_id": tech["id"],
                "mitre_tactic": "TBD"
            })

    return pd.Series({
        "mitre_technique": "Unknown",
        "mitre_id": "N/A",
        "mitre_tactic": "N/A"
    })

def enrich_with_mitre(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches unified_df with MITRE technique information from enterprise-attack.json
    """
    print("Loading MITRE ATT&CK techniques...")
    techniques = load_attack_techniques()
    print(f"Loaded {len(techniques)} techniques.")

    print("Matching summaries to MITRE techniques...")
    return df.join(df["llm_summary"].apply(lambda x: match_mitre_dynamic(x, techniques)))
