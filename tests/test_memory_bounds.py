from buzz.memory.context import ConversationContext
from buzz.memory.store import InMemoryStore

def test_memory_truncates_large_exchange():
    store=InMemoryStore(); context=ConversationContext(store)
    assert context.remember("u"*5000,"a"*9000)
    item=context.recent()[0]
    assert len(item["user"])==4000 and len(item["assistant"])==8000
