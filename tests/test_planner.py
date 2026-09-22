import pytest

from buzz.core.planner import PlanError, parse_plan


def test_parse_plan():
    plan = parse_plan('{"reply":"Done","actions":[{"skill":"system.info","arguments":{},"reason":"status"}]}')
    assert plan.reply == "Done"
    assert plan.actions[0].skill == "system.info"


def test_parse_plan_rejects_invalid_json():
    with pytest.raises(PlanError):
        parse_plan("not json")
