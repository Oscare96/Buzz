"""Local API surface for Buzz desktop/mobile clients."""
from __future__ import annotations
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from secrets import compare_digest
from pathlib import Path
from buzz.app import build_runtime
from buzz.core.request import BuzzRequest
from buzz.status import status_report
from buzz.config.settings import Settings
from buzz.security.audit_log import AuditLog
from buzz.dashboard import dashboard_html

app=FastAPI(title="Buzz API",version="0.1.0")

def require_api_token(authorization: str | None = Header(default=None)) -> None:
    expected=Settings.load().api_token
    if not expected:
        raise HTTPException(status_code=503,detail="BUZZ_API_TOKEN is required before using Buzz control API endpoints.")
    supplied = authorization or ""
    if not compare_digest(supplied, f"Bearer {expected}"):
        raise HTTPException(status_code=401,detail="Invalid or missing Buzz API token.")
_runtime=None

def runtime():
    global _runtime
    if _runtime is None: _runtime=build_runtime()
    return _runtime

class RequestBody(BaseModel):
    text: str = Field(min_length=1,max_length=4000)
    source: str = Field(default="api",min_length=1,max_length=64)

class ApprovalBody(BaseModel):
    skill: str = Field(min_length=1,max_length=128)
    arguments: dict
    approval_token: str = Field(min_length=1,max_length=128)

@app.get("/",response_class=HTMLResponse)\ndef dashboard():\n    return dashboard_html()\n\n@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/status",dependencies=[Depends(require_api_token)])
def status(): return status_report()

@app.post("/request",dependencies=[Depends(require_api_token)])
def request(body: RequestBody):
    text=body.text.strip()
    if not text: raise HTTPException(400,"text is required")
    response=runtime().handle(BuzzRequest(text=text,source=body.source))
    return {"text":response.text,"request_id":response.request_id,"metadata":response.metadata}

@app.post("/approve",dependencies=[Depends(require_api_token)])
def approve(body: ApprovalBody):
    result=runtime().confirm(body.skill,body.arguments,body.approval_token)
    return {"success":result.success,"message":result.message,"data":result.data}

@app.get("/audit",dependencies=[Depends(require_api_token)])
def audit(limit: int = 50):
    limit=max(1,min(limit,200))
    return {"events":AuditLog(Path(".cache/buzz/audit.jsonl")).read_recent(limit)}

@app.get("/pending-approvals",dependencies=[Depends(require_api_token)])
def pending_approvals():
    rt=runtime()
    return {"count":rt.approvals.pending_count() if rt.approvals else 0}

@app.get("/runtime-status",dependencies=[Depends(require_api_token)])
def runtime_status():
    rt=runtime()
    return {"pending_approvals":rt.approvals.pending_count() if rt.approvals else 0,"skills":rt.router.registry.names()}
