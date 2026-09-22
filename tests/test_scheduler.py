import time
from buzz.events.scheduler import PollingScheduler

def test_scheduler_runs_and_stops():
    calls=[]
    scheduler=PollingScheduler(lambda:calls.append(1),1)
    scheduler.start()
    for _ in range(20):
        if calls: break
        time.sleep(.01)
    scheduler.stop()
    assert calls
    assert scheduler.running is False
