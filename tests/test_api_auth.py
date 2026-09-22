import pytest
from fastapi import HTTPException
from buzz.api import require_api_token
from buzz.config.settings import Settings

def test_api_auth_rejects_wrong_token(monkeypatch):
    monkeypatch.setattr(Settings,"load",classmethod(lambda cls: Settings("","","",api_token="secret")))
    with pytest.raises(HTTPException) as exc:
        require_api_token("Bearer wrong")
    assert exc.value.status_code==401

def test_api_auth_accepts_correct_token(monkeypatch):
    monkeypatch.setattr(Settings,"load",classmethod(lambda cls: Settings("","","",api_token="secret")))
    assert require_api_token("Bearer secret") is None
