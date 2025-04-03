
import pandas as pd

# Static (proof-of-concept) MITRE ATT&CK mapping
MITRE_TECHNIQUES = [
    {
        "id": "T1059",
        "technique": "Command and Scripting Interpreter",
        "keywords": ["script", "cmd", "powershell", "bash", "terminal"],
        "tactic": "Execution"
    },
    {
        "id": "T1547",
        "technique": "Boot or Logon Autostart Execution",
        "keywords": ["registry", "run key", "autostart", "startup"],
        "tactic": "Persistence"
    },
    {
        "id": "T1566",
        "technique": "Phishing",
        "keywords": ["email", "credential", "malicious link", "spearphish"],
        "tactic": "Initial Access"
    },
    {
        "id": "T1041",
        "technique": "Exfiltration Over C2 Channel",
        "keywords": ["exfil", "data theft", "leak", "upload", "send to"],
        "tactic": "Exfiltration"
    },
    {
        "id": "T1218",
        "technique": "Signed Binary Proxy Execution",
        "keywords": ["signed binary", "bypass", "trusted process"],
        "tactic": "Defense Evasion"
    }
]

def match_mitre(summary: str):
    summary_lower = summary.lower()
    for entry in MITRE_TECHNIQUES:
        if any(keyword in summary_lower for keyword in entry["keywords"]):
            return pd.Series({
                "mitre_technique": entry["technique"],
                "mitre_id": entry["id"],
                "mitre_tactic": entry["tactic"]
            })
    return pd.Series({
        "mitre_technique": "Unknown",
        "mitre_id": "N/A",
        "mitre_tactic": "N/A"
    })

def enrich_with_mitre(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches a unified DataFrame with MITRE technique metadata
    based on the LLM-generated summaries.
    """
    return df.join(df["llm_summary"].apply(match_mitre))
