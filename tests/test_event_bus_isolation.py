from buzz.events.bus import EventBus
from buzz.events.models import BuzzEvent

def test_handler_failure_is_isolated():
    bus=EventBus(); called=[]
    def bad(event): raise RuntimeError("boom")
    def good(event): called.append(event.kind)
    bus.subscribe("x",bad); bus.subscribe("x",good)
    errors=bus.publish(BuzzEvent(kind="x",source="test"))
    assert called==["x"]
    assert len(errors)==1 and isinstance(errors[0],RuntimeError)
