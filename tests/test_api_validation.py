import pytest
from pydantic import ValidationError
from buzz.api import RequestBody

def test_request_body_rejects_oversized_text():
    with pytest.raises(ValidationError):
        RequestBody(text="x"*4001)

def test_request_body_accepts_normal_text():
    body=RequestBody(text="Open Notepad")
    assert body.source=="api"
