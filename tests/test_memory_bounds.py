from buzz.memory.context import ConversationContext
from buzz.memory.store import InMemoryStore

def test_memory_truncates_large_exchange():
    store=InMemoryStore(); context=ConversationContext(store)
    user=("user text. "*600)[:5000]
    assistant=("assistant response. "*600)[:9000]
    assert context.remember(user,assistant)
    item=context.recent()[0]
    assert len(item["user"])==4000 and len(item["assistant"])==8000
