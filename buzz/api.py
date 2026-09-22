"""Local API surface for Buzz desktop/mobile clients."""
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from buzz.app import build_runtime
from buzz.core.request import BuzzRequest
from buzz.status import status_report

app=FastAPI(title="Buzz API",version="0.1.0")
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

@app.get("/status")
def status(): return status_report()

@app.post("/request")
def request(body: RequestBody):
    if not body.text.strip(): raise HTTPException(400,"text is required")
    response=runtime().handle(BuzzRequest(text=body.text.strip(),source=body.source))
    return {"text":response.text,"request_id":response.request_id,"metadata":response.metadata}

@app.post("/approve")
def approve(body: ApprovalBody):
    result=runtime().confirm(body.skill,body.arguments,body.approval_token)
    return {"success":result.success,"message":result.message,"data":result.data}
