"""Local API surface for Buzz desktop/mobile clients."""
from __future__ import annotations
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from buzz.app import build_runtime
from buzz.core.request import BuzzRequest
from buzz.status import status_report
from buzz.config.settings import Settings

app=FastAPI(title="Buzz API",version="0.1.0")

def require_api_token(authorization: str | None = Header(default=None)) -> None:
    expected=Settings.load().api_token
    if not expected:
        return
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401,detail="Invalid or missing Buzz API token.")
_runtime=None

def runtime():
    global _runtime
    if _runtime is None: _runtime=build_runtime()
    return _runtime

class RequestBody(BaseModel):
    text: str
    source: str="api"

class ApprovalBody(BaseModel):
    skill: str
    arguments: dict
    approval_token: str

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/status",dependencies=[Depends(require_api_token)])
def status(): return status_report()

@app.post("/request",dependencies=[Depends(require_api_token)])
def request(body: RequestBody):
    if not body.text.strip(): raise HTTPException(400,"text is required")
    response=runtime().handle(BuzzRequest(text=body.text.strip(),source=body.source))
    return {"text":response.text,"request_id":response.request_id,"metadata":response.metadata}

@app.post("/approve",dependencies=[Depends(require_api_token)])
def approve(body: ApprovalBody):
    result=runtime().confirm(body.skill,body.arguments,body.approval_token)
    return {"success":result.success,"message":result.message,"data":result.data}
