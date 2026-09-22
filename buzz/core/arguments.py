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
        if expected=="string":
            if "minLength" in spec and len(value) < spec["minLength"]: return f"Argument {key} is too short."
            if "maxLength" in spec and len(value) > spec["maxLength"]: return f"Argument {key} is too long."
        if expected=="array":
            if "minItems" in spec and len(value) < spec["minItems"]: return f"Argument {key} has too few items."
            if "maxItems" in spec and len(value) > spec["maxItems"]: return f"Argument {key} has too many items."
            item_spec=spec.get("items")
            if isinstance(item_spec,dict):
                item_type=item_spec.get("type")
                for index,item in enumerate(value):
                    if item_type=="string" and not isinstance(item,str): return f"Argument {key}[{index}] must be string."
                    if item_type=="number" and (not isinstance(item,(int,float)) or isinstance(item,bool)): return f"Argument {key}[{index}] must be number."
        if "enum" in spec and value not in spec["enum"]: return f"Argument {key} must be one of: {', '.join(map(str,spec['enum']))}."
        if isinstance(value,(int,float)) and not isinstance(value,bool):
            if "exclusiveMinimum" in spec and value <= spec["exclusiveMinimum"]: return f"Argument {key} must be greater than {spec['exclusiveMinimum']}."
            if "minimum" in spec and value < spec["minimum"]: return f"Argument {key} must be at least {spec['minimum']}."
    return None
