"""Small stoppable scheduler for proactive Buzz monitors."""
from __future__ import annotations
from threading import Event,Thread
from collections.abc import Callable

class PollingScheduler:
    def __init__(self,task:Callable[[],None],interval_seconds:float=60.0)->None:
        if interval_seconds < 1:
            raise ValueError("interval_seconds must be at least 1")
        self.task=task
        self.interval_seconds=interval_seconds
        self._stop=Event()
        self._thread:Thread|None=None

    @property
    def running(self)->bool:
        return bool(self._thread and self._thread.is_alive())

    def start(self)->None:
        if self.running:
            return
        self._stop.clear()
        self._thread=Thread(target=self._run,name="buzz-proactive",daemon=True)
        self._thread.start()

    def stop(self,timeout:float=5.0)->None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout)

    def _run(self)->None:
        while not self._stop.is_set():
            try:
                self.task()
            except Exception:
                pass
            if self._stop.wait(self.interval_seconds):
                break
