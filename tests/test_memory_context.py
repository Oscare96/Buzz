from buzz.memory.context import ConversationContext,is_sensitive_text
from buzz.memory.store import InMemoryStore

def test_sensitive_text_is_not_remembered():
    memory=ConversationContext(InMemoryStore())
    assert memory.remember("my api key is abc","ok") is False
    assert memory.recent()==[]

def test_context_is_bounded():
    memory=ConversationContext(InMemoryStore(),max_exchanges=2)
    memory.remember("one","1"); memory.remember("two","2"); memory.remember("three","3")
    assert [x["user"] for x in memory.recent()]==["two","three"]

def test_long_token_like_value_is_sensitive():
    assert is_sensitive_text("value "+"a"*40)
