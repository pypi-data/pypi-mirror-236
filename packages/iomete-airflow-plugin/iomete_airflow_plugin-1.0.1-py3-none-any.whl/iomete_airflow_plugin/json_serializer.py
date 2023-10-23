import json

from typing import Dict, Optional, Union


def serialize_to_dict(config_override: Optional[Union[Dict, str]] = None) -> Dict:
    if config_override is None:
        return {}

    if isinstance(config_override, dict):
        return config_override

    # Try parsing the string as JSON
    try:
        return json.loads(config_override)
    except json.JSONDecodeError:
        pass

    # If not valid JSON, assume it's a Python dict string and try to convert to a dict
    try:
        # Convert string representation of dict to actual dict
        return eval(config_override)
    except:
        raise ValueError(f"Unsupported format for config_override: {config_override}")


# Test cases
print(serialize_to_dict())
print(serialize_to_dict({"envVars": {"hello": "world"}, "arguments": ["a", "b"]}))
print(serialize_to_dict('{"envVars": {"hello": "world"}}'))
print(serialize_to_dict("{'envVars': {'hello': 'wlds'}, 'arguments': ['a', 'b']}"))
