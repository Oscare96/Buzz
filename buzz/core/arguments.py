"""Minimal JSON-schema-style validation for Buzz skill arguments."""
from __future__ import annotations
from typing import Any

def validate_arguments(schema:dict[str,Any],arguments:dict[str,Any])->str|None:
    if schema.get("type")!="object": return "Skill schema must describe an object."
    props=schema.get("properties",{})
    required=schema.get("required",[])
    for key in required:
        if key not in arguments: return f"Missing required argument: {key}."
    if schema.get("additionalProperties") is False:
        extra=set(arguments)-set(props)
        if extra: return f"Unexpected argument: {sorted(extra)[0]}."
    for key,value in arguments.items():
        spec=props.get(key)
        if not spec: continue
        expected=spec.get("type")
        valid=(expected=="string" and isinstance(value,str)) or (expected=="boolean" and isinstance(value,bool)) or (expected=="number" and isinstance(value,(int,float)) and not isinstance(value,bool)) or (expected=="integer" and isinstance(value,int) and not isinstance(value,bool)) or (expected=="object" and isinstance(value,dict)) or (expected=="array" and isinstance(value,list)) or expected is None
        if not valid: return f"Argument {key} must be {expected}."
        if "enum" in spec and value not in spec["enum"]: return f"Argument {key} must be one of: {', '.join(map(str,spec['enum']))}."
        if isinstance(value,(int,float)) and not isinstance(value,bool):
            if "exclusiveMinimum" in spec and value <= spec["exclusiveMinimum"]: return f"Argument {key} must be greater than {spec['exclusiveMinimum']}."
            if "minimum" in spec and value < spec["minimum"]: return f"Argument {key} must be at least {spec['minimum']}."
    return None
