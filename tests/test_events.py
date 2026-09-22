from buzz.events.bus import EventBus
from buzz.events.models import BuzzEvent


def test_event_bus_delivers_matching_event():
    bus = EventBus()
    received = []
    bus.subscribe("test", received.append)
    event = BuzzEvent(kind="test", source="unit")
    bus.publish(event)
    assert received == [event]
