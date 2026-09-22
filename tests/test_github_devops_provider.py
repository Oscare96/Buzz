import pytest
from buzz.integrations.devops.github import GitHubDevOpsProvider

class Response:
    def __init__(self,payload=None): self.payload=payload or {}
    def raise_for_status(self): return None
    def json(self): return self.payload

def test_repository_status_validates_owner_repo(monkeypatch):
    provider=GitHubDevOpsProvider("token")
    with pytest.raises(ValueError): provider.repository_status("../bad")

def test_repository_status_maps_fields(monkeypatch):
    def fake_get(url,headers,timeout):
        assert url.endswith("/repos/Oscare96/Buzz")
        return Response({"full_name":"Oscare96/Buzz","default_branch":"main","private":False,"archived":False})
    monkeypatch.setattr("buzz.integrations.devops.github.requests.get",fake_get)
    data=GitHubDevOpsProvider("token").repository_status("Oscare96/Buzz")
    assert data["full_name"]=="Oscare96/Buzz"
    assert data["default_branch"]=="main"

def test_workflow_name_is_url_encoded(monkeypatch):
    captured={}
    def fake_post(url,headers,json,timeout):
        captured["url"]=url; captured["json"]=json; return Response()
    monkeypatch.setattr("buzz.integrations.devops.github.requests.post",fake_post)
    GitHubDevOpsProvider("token").run_pipeline("Oscare96/Buzz","CI workflow.yml","develop")
    assert "CI%20workflow.yml" in captured["url"]
    assert captured["json"]=={"ref":"develop"}
