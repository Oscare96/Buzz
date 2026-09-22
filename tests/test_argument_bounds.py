from buzz.core.arguments import validate_arguments

def test_string_length_bounds():
    schema={"type":"object","properties":{"name":{"type":"string","minLength":2,"maxLength":4}},"additionalProperties":False}
    assert validate_arguments(schema,{"name":"a"})
    assert validate_arguments(schema,{"name":"abc"}) is None
    assert validate_arguments(schema,{"name":"abcde"})

def test_array_item_bounds():
    schema={"type":"object","properties":{"argv":{"type":"array","minItems":1,"maxItems":3}},"additionalProperties":False}
    assert validate_arguments(schema,{"argv":[]})
    assert validate_arguments(schema,{"argv":["echo"]}) is None
