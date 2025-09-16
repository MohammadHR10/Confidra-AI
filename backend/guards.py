import os, json, re, yaml
DATA = json.load(open(os.path.join("data","contract.json")))
RULES = yaml.safe_load(open(os.path.join("rules","contract_policies.yaml")))

PROTECTED = [d["clause"] for d in DATA if d["sensitivity"]=="protected"]
PUBLIC    = [d["clause"] for d in DATA if d["sensitivity"]=="public"]

def public_context():
    return "\n- " + "\n- ".join(PUBLIC)

def scan_text(output: str):
    # 1) direct protected overlap
    for clause in PROTECTED:
        if clause.lower() in output.lower():
            return {"action":"blocked","reason":f"NDA overlap: {clause}"}

    # 2) rule keywords
    for rule in RULES.get("redactions", []):
        for key in rule["match"]:
            if re.search(re.escape(key), output, flags=re.I):
                if rule["action"] == "block":
                    return {"action":"blocked","reason":f"Policy {rule['name']} matched"}
                if rule["action"] == "redact":
                    redacted = re.sub(re.escape(key), "[REDACTED]", output, flags=re.I)
                    return {"action":"redacted","reason":f"Redacted {rule['name']}", "safe_output": redacted}
    return {"action":"pass","reason":"No violation"}
