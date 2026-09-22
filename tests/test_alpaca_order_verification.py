import types
from buzz.integrations.trading.alpaca import AlpacaTradingProvider

def test_place_order_verifies_broker_order(monkeypatch):
    provider=AlpacaTradingProvider("key","secret")
    posted=[]
    class Response:
        def raise_for_status(self): pass
        def json(self): return {"id":"broker-1","status":"accepted"}
    monkeypatch.setattr("buzz.integrations.trading.alpaca.requests.post",lambda *a,**k:(posted.append(k["json"]) or Response()))
    monkeypatch.setattr(provider,"_get",lambda path:{"id":"broker-1","status":"accepted","path":path})
    result=provider.place_order("AAPL","buy",1,"stable-key")
    assert posted[0]["client_order_id"]=="stable-key"
    assert result["verified"]["id"]=="broker-1"
    assert result["idempotency_key"]=="stable-key"
