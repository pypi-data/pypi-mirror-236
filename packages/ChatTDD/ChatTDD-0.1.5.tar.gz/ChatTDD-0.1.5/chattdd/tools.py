import re
import json

def extract_json(s):
    match = re.search(r'{\s*.*\s*}', s, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            # Optionally, check if it's valid JSON
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            print("Matched string is not valid JSON")
            return None
    else:
        print("No JSON found")
        return None
