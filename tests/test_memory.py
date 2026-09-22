from buzz.memory.store import InMemoryStore


def test_memory_namespaces_values():
    store = InMemoryStore()
    store.put("user", "name", "Buzz")
    assert store.get("user", "name") == "Buzz"
    assert store.get("other", "name") is None
