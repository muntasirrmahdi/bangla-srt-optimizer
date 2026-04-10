import re
import json
import os

def load_rules(rules_path):
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
    else:
        # Fallback to sample if primary missing (for portability)
        sample_path = rules_path.replace("rules.json", "rules_sample.json")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                rules = json.load(f)
        else:
            rules = []
    
    rules.sort(key=lambda x: len(x[0]), reverse=True)
    return rules

def apply_hardcoded_fixes(text: str, rules: list) -> str:
    """Applies specific hardcoded Bengali corrections."""
    for wrong, correct in rules:
        text = text.replace(wrong, correct)

    text = re.sub(r"  +", " ", text)
    text = re.sub(r" [,।]", lambda m: m.group(0).strip(), text)
    return text.strip()

def validate_srt(subs):
    """Basic validation for SRT blocks."""
    if not subs:
        return False, "Empty SRT file."
    return True, ""
