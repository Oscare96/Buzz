import pytest
from fastapi import HTTPException
from buzz.api import require_api_token
from buzz.config.settings import Settings

def test_api_auth_fails_closed_without_configured_token(monkeypatch):
    monkeypatch.setattr(Settings,"load",classmethod(lambda cls: Settings("","","")))
    with pytest.raises(HTTPException) as exc:
        require_api_token(None)
    assert exc.value.status_code==503
