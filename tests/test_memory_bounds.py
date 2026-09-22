from buzz.memory.context import ConversationContext
from buzz.memory.store import InMemoryStore

def test_memory_truncates_large_exchange():
    store=InMemoryStore(); context=ConversationContext(store)
    assert context.remember(("user text "*500)[:5000],("assistant text "*700)[:9000])
    item=context.recent()[0]
    assert len(item["user"])==4000 and len(item["assistant"])==8000
