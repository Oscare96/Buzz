from buzz.core.arguments import validate_arguments

def test_missing_required_argument():
    schema={"type":"object","properties":{"url":{"type":"string"}},"required":["url"],"additionalProperties":False}
    assert "Missing required" in validate_arguments(schema,{})

def test_rejects_unexpected_argument():
    schema={"type":"object","properties":{},"additionalProperties":False}
    assert "Unexpected argument" in validate_arguments(schema,{"oops":1})

def test_accepts_valid_enum():
    schema={"type":"object","properties":{"side":{"type":"string","enum":["buy","sell"]}},"required":["side"],"additionalProperties":False}
    assert validate_arguments(schema,{"side":"buy"}) is None
    assert "one of" in validate_arguments(schema,{"side":"hold"})
