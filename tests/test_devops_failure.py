from buzz.skills.devops import PipelineFailureSkill

class FakeDevOps:
    def pipeline_failure(self, repository): return {"run_id":7,"failed_jobs":[{"name":"test"}]}

def test_pipeline_failure_skill_reports_provider_data():
    result=PipelineFailureSkill(FakeDevOps()).execute(repository="owner/repo")
    assert result.success
    assert result.data["run_id"]==7
