from buzz.memory.json_store import JsonMemoryStore

def test_json_memory_persists(tmp_path):
    path=tmp_path/"memory.json"; first=JsonMemoryStore(path); first.put("prefs","name","Buzz")
    second=JsonMemoryStore(path)
    assert second.get("prefs","name")=="Buzz"
