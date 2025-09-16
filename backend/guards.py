import os, json, re, yaml
from document_processor import doc_processor

RULES = yaml.safe_load(open(os.path.join("rules","contract_policies.yaml")))

def get_protected_clauses():
    return doc_processor.get_protected_clauses()

def get_public_clauses():
    return doc_processor.get_public_clauses()

def public_context():
    public_clauses = get_public_clauses()
    if public_clauses:
        return "\n- " + "\n- ".join(public_clauses)
    else:
        return "\n- No public contract information available yet. Please upload documents first."

def scan_text(output: str):
    # 1) direct protected overlap
    protected_clauses = get_protected_clauses()
    for clause in protected_clauses:
        if clause.lower() in output.lower():
            return {"action":"blocked","reason":f"Protected information overlap: {clause[:50]}..."}

    # 2) rule keywords
    for rule in RULES.get("redactions", []):
        for key in rule["match"]:
            if re.search(re.escape(key), output, flags=re.I):
                if rule.get("action") == "block":
                    return {"action":"blocked","reason":f"Policy {rule['name']} matched"}
                if rule.get("action") == "redact":
                    redacted = re.sub(re.escape(key), "[REDACTED]", output, flags=re.I)
                    return {"action":"redacted","reason":f"Redacted {rule['name']}", "safe_output": redacted}
    return {"action":"pass","reason":"No violation"}
