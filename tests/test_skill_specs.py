from buzz.skills.defaults import build_default_registry


def test_registry_exposes_skill_specs():
    specs = {item["name"]: item for item in build_default_registry().planner_specs()}
    assert specs["computer.open_url"]["arguments"]["required"] == ["url"]
    assert specs["filesystem.write"]["arguments"]["required"] == ["path", "content"]
    assert specs["system.info"]["arguments"]["type"] == "object"
