import json,pytest
from buzz.core.planner import parse_plan,PlanError

def test_planner_rejects_too_many_actions():
    raw=json.dumps({"reply":"","actions":[{"skill":"x","arguments":{}} for _ in range(17)]})
    with pytest.raises(PlanError): parse_plan(raw)

def test_planner_rejects_empty_skill_name():
    with pytest.raises(PlanError): parse_plan('{"reply":"","actions":[{"skill":"","arguments":{}}]}')
