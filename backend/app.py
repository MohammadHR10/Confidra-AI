# app.py
from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from dotenv import load_dotenv

from models import AskRequest, AskResponse
from friendli_client import classify_query, generate_from_context, polite_block
from guards import scan_text, public_context
from store import log_event

load_dotenv()

app = FastAPI(
    title="Contract Compliance Sentinel",
    version="0.1.0",
    description="Pre- and post-guard rails to prevent NDA/regulated clause leakage.",
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """
    Flow:
      1) Pre-guard classification → block if sensitive/exfiltration
      2) Generate strictly from PUBLIC context (no private corp data)
      3) Post-guard scan (protected overlap + rules) → block/redact/pass
      4) Log all outcomes
    """
    try:
        # ---------- 1) Pre-guard classify ----------
        decision = classify_query(req.query)
        label = decision.get("label", "safe")

        if label in ("sensitive", "exfiltration"):
            msg = polite_block(f"Query classified as {label}")
            log_event("blocked_pre", {
                "user": req.user_id,
                "query": req.query,
                "decision": decision
            })
            return AskResponse(
                action="blocked",
                reason=f"Pre-guard: {label}",
                safe_output=msg,
                evidence={"decision": decision},
            )

        # ---------- 2) RAG from PUBLIC context only ----------
        ctx = public_context()
        answer = generate_from_context(ctx, req.query)

        # ---------- 3) Post-guard scan ----------
        scan = scan_text(answer)

        if scan["action"] == "blocked":
            msg = polite_block(scan["reason"])
            log_event("blocked_post", {
                "user": req.user_id,
                "query": req.query,
                "reason": scan["reason"],
                "raw_answer": answer,
            })
            return AskResponse(
                action="blocked",
                reason=scan["reason"],
                safe_output=msg,
                evidence={"raw": answer},
            )

        if scan["action"] == "redacted":
            log_event("redacted", {
                "user": req.user_id,
                "query": req.query,
                "reason": scan["reason"],
            })
            return AskResponse(
                action="redacted",
                reason=scan["reason"],
                safe_output=scan["safe_output"],
                evidence={},
            )

        # ---------- 4) Pass ----------
        log_event("pass", {"user": req.user_id, "query": req.query})
        return AskResponse(
            action="pass",
            reason="OK",
            safe_output=answer,
            evidence={},
        )

    except HTTPException:
        # Let FastAPI handle explicit HTTPExceptions
        raise
    except Exception as e:
        # Hard fail: log and return a safe, generic message
        log_event("error", {
            "user": req.user_id,
            "query": req.query,
            "error": repr(e),
        })
        raise HTTPException(status_code=500, detail="Internal error")

@app.post("/upload-document")
async def upload_document(
    filename: str = Form(...),
    content: str = Form(...),
    sensitivity: str = Form(default="public"),
    timestamp: str = Form(...)
):
    """
    Upload and process a document for contract compliance
    """
    try:
        # Here you would typically:
        # 1. Parse the document content into clauses
        # 2. Classify each clause by sensitivity
        # 3. Store in the database/file system
        
        # For now, we'll just log the upload
        log_event("document_upload", {
            "filename": filename,
            "sensitivity": sensitivity,
            "content_length": len(content),
            "timestamp": timestamp
        })
        
        # TODO: Implement actual document processing
        # - Extract clauses from content
        # - Classify sensitivity of each clause
        # - Update the contract.json file
        
        return {
            "success": True,
            "message": f"Document '{filename}' uploaded successfully",
            "clauses_extracted": 0,  # Placeholder
            "sensitivity": sensitivity
        }
        
    except Exception as e:
        log_event("error", {
            "action": "document_upload",
            "filename": filename,
            "error": repr(e)
        })
        raise HTTPException(status_code=500, detail="Document upload failed")

@app.get("/documents")
async def list_documents():
    """
    List all uploaded documents
    """
    try:
        # This would typically query a database
        # For now, return a sample response
        return {
            "documents": [
                {
                    "filename": "contract_v1.pdf",
                    "upload_date": "2024-01-15",
                    "sensitivity": "protected",
                    "clauses_count": 45,
                    "status": "active"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list documents")
