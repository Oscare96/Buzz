"""GitHub REST provider for Buzz DevOps capabilities."""
from __future__ import annotations
from typing import Any
import requests
from buzz.integrations.devops.base import DevOpsProvider

class GitHubDevOpsProvider(DevOpsProvider):
    def __init__(self, token: str) -> None:
        self.headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
        self.base="https://api.github.com"
    def _get(self,path:str)->dict[str,Any]:
        r=requests.get(self.base+path,headers=self.headers,timeout=15); r.raise_for_status(); return r.json()
    def repository_status(self,repository:str)->dict[str,Any]:
        d=self._get(f"/repos/{repository}"); return {"full_name":d.get("full_name"),"default_branch":d.get("default_branch"),"private":d.get("private"),"archived":d.get("archived")}
    def pipeline_status(self,repository:str)->dict[str,Any]:
        d=self._get(f"/repos/{repository}/actions/runs?per_page=1"); runs=d.get("workflow_runs",[])
        if not runs:return {"status":"none"}
        r=runs[0]; return {"id":r.get("id"),"name":r.get("name"),"status":r.get("status"),"conclusion":r.get("conclusion"),"head_branch":r.get("head_branch")}
    def run_pipeline(self,repository:str,workflow:str,ref:str)->dict[str,Any]:
        r=requests.post(f"{self.base}/repos/{repository}/actions/workflows/{workflow}/dispatches",headers=self.headers,json={"ref":ref},timeout=15); r.raise_for_status(); return {"dispatched":True,"workflow":workflow,"ref":ref}
    def deploy(self,application:str,environment:str,version:str)->dict[str,Any]:
        raise NotImplementedError("GitHub deployment adapter is not configured for this application.")
    def run_command(self,target:str,command:str)->dict[str,Any]:
        raise NotImplementedError("Remote command targets require a separately configured executor.")
