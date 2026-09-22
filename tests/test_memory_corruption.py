import pytest
from buzz.memory.json_store import JsonMemoryStore

def test_corrupt_memory_is_not_silently_overwritten(tmp_path):
    path=tmp_path/"memory.json"; path.write_text("{broken",encoding="utf-8")
    store=JsonMemoryStore(path)
    with pytest.raises(RuntimeError): store.put("conversation","recent",[])
    assert path.read_text(encoding="utf-8")=="{broken"
