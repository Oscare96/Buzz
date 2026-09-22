from buzz.integrations.devops.base import DevOpsProvider
from buzz.proactive import ProactiveService

class Provider(DevOpsProvider):
    def repository_status(self,repository): return {}
    def pipeline_status(self,repository): return {"id":7,"conclusion":"failure","path":".github/workflows/ci.yml","head_branch":"develop"}
    def pipeline_failure(self,repository): return {"run_id":7,"failed_jobs":[{"name":"test"}]}
    def run_pipeline(self,repository,workflow,ref): return {}
    def deploy(self,application,environment,version): return {}
    def run_command(self,target,command): return {}

def test_proactive_service_proposes_but_does_not_execute():
    provider=Provider(); service=ProactiveService(provider)
    result=service.check_pipeline("Oscare96/Buzz")
    assert result["status"]["conclusion"]=="failure"
    assert len(result["proposals"])==1
    assert result["proposals"][0]["skill"]=="devops.run_pipeline"
