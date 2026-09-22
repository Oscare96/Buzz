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

@app.get("/",response_class=HTMLResponse)
def dashboard():
    return """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Buzz Control Center</title><style>body{margin:0;background:#090b10;color:#f5f7fb;font-family:system-ui,-apple-system,Segoe UI,sans-serif}.wrap{max-width:980px;margin:auto;padding:48px 24px}.top{display:flex;justify-content:space-between;align-items:center;gap:20px}.brand{font-size:42px;font-weight:800}.pill{padding:8px 12px;border:1px solid #2d3544;border-radius:999px;color:#9ee6b0}.hero{margin-top:52px;padding:32px;border:1px solid #252b36;border-radius:24px;background:#11151d}.hero h1{font-size:34px;margin:0 0 10px}.muted{color:#9aa4b5}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-top:20px}.card{padding:18px;border:1px solid #252b36;border-radius:16px;background:#0d1118}.card b{display:block;margin-bottom:7px}.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#63d887;margin-right:8px}.foot{margin-top:28px;color:#768196;font-size:13px}</style></head><body><main class="wrap"><div class="top"><div class="brand">BUZZ</div><div class="pill"><span class="dot"></span>Local server online</div></div><section class="hero"><h1>Buzz Control Center</h1><p class="muted">Your personal AI automation platform is running locally.</p><div class="grid"><div class="card"><b>AI Core</b><span class="muted">Structured planning + tool routing</span></div><div class="card"><b>Security</b><span class="muted">Approvals + audit protection</span></div><div class="card"><b>Computer</b><span class="muted">Apps, files and commands</span></div><div class="card"><b>Integrations</b><span class="muted">Trading, DevOps and Home</span></div></div><div class="foot">Buzz v0.1 • Local control center • Port 8787</div></section></main></body></html>"""

@app.get("/health")
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

@app.get("/runtime-status",dependencies=[Depends(require_api_token)])
def runtime_status():
    rt=runtime()
    return {"pending_approvals":rt.approvals.pending_count() if rt.approvals else 0,"skills":rt.router.registry.names()}
