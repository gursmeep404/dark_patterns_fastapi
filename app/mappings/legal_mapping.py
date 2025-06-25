import json
import os

with open(os.path.join(os.path.dirname(__file__), "legal_mapping.json"), "r") as f:
    law_map = json.load(f)

def map_laws(pattern_type):
    return law_map.get(pattern_type.lower(), [])
