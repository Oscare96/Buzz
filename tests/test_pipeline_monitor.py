from buzz.events.bus import EventBus
from buzz.events.monitor import PipelineMonitor

class Provider:
    def pipeline_status(self, repository): return {"id":42,"conclusion":"failure"}
    def pipeline_failure(self, repository): return {"run_id":42,"failed_jobs":[{"name":"tests"}]}

def test_pipeline_failure_emitted_once_per_run():
    bus=EventBus(); events=[]; bus.subscribe("devops.pipeline_failed",events.append)
    monitor=PipelineMonitor(Provider(),bus)
    monitor.check("owner/repo"); monitor.check("owner/repo")
    assert len(events)==1
    assert events[0].payload["repository"]=="owner/repo"
    assert events[0].payload["failure"]["run_id"]==42
