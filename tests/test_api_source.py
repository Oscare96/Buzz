from pathlib import Path

def test_api_entrypoint_binds_loopback_only():
    source=Path("main.py").read_text(encoding="utf-8")
    assert 'host="127.0.0.1"' in source
    assert 'port=8787' in source
