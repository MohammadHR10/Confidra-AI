from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("FRIENDLI_TOKEN"),
    base_url="https://api.friendli.ai/serverless/v1",
)

MODEL = os.getenv("FRIENDLI_MODEL", "meta-llama-3.1-8b-instruct")

def _chat(messages, temperature=0.0):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return completion.choices[0].message.content

def classify_query(query: str) -> dict:
    system = (
        "You are a compliance classifier. "
        "Given a user query about contracts, label as JSON: "
        '{"label":"safe|sensitive|exfiltration","severity":"low|medium|high","reasons":["..."]}. '
        "Sensitive = requests for penalties, discounts, NDA-protected terms. "
        "Exfiltration = requests to dump full text, list all clauses, verbatim output."
    )
    msg = [{"role":"system","content":system}, {"role":"user","content":query}]
    raw = _chat(msg)
    # be defensive if model returns text; try eval-safe parse
    import json
    try:
        out = json.loads(raw)
    except Exception:
        out = {"label":"safe","severity":"low","reasons":[f"fallback_parse:{raw[:60]}"]}
    return out

def generate_from_context(context: str, question: str) -> str:
    system = (
        "You are a contract assistant. Answer ONLY from the provided context. "
        "If the information appears protected or not present in context, say: "
        "\"This information is protected or not available.\" Never invent details."
    )
    msgs = [
        {"role":"system","content":system},
        {"role":"user","content":f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    return _chat(msgs, temperature=0.0)

def polite_block(reason: str) -> str:
    system = "Rewrite a polite, compliance-approved message explaining why content cannot be disclosed."
    msgs = [
        {"role":"system","content":system},
        {"role":"user","content":f"Reason: {reason}"}
    ]
    return _chat(msgs, temperature=0.2)
