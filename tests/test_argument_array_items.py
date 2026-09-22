from buzz.core.arguments import validate_arguments

def test_array_string_items_are_validated():
    schema={"type":"object","properties":{"argv":{"type":"array","items":{"type":"string"}}},"required":["argv"],"additionalProperties":False}
    assert validate_arguments(schema,{"argv":["python","--version"]}) is None
    assert "argv[1]" in validate_arguments(schema,{"argv":["python",3]})


def test_array_string_item_length_is_bounded():
    schema={"type":"object","properties":{"argv":{"type":"array","items":{"type":"string","maxLength":4}}},"required":["argv"],"additionalProperties":False}
    assert validate_arguments(schema,{"argv":["12345"]})
