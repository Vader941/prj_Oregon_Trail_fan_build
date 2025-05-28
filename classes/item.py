"""
item.py - Defines the Item class and loads item types from a JSON file.
"""

import json
import os

# Load item types from JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.json')
try:
    with open(DATA_PATH, 'r') as f:
        ITEM_TYPES = json.load(f)
except FileNotFoundError:
    print("Warning: items.json not found. Defaulting to empty item type list.")
    ITEM_TYPES = {}

class Item:
    def __init__(self, name):
        if name in ITEM_TYPES:
            props = ITEM_TYPES[name]
            self.name = name
            self.weight = props.get("weight", 0)
            self.description = props.get("description", "")
            self.can_spoil = props.get("can_spoil", False)
            self.wears_out = props.get("wears_out", False)
            self.usable = props.get("usable", False)
            self.consumable = props.get("consumable", False)
            self.spoiled = props.get("spoiled", False)
        else:
            raise ValueError(f"Item type '{name}' is not defined.")

    def __str__(self):
        return f"{self.name}: {self.description} (Weight: {self.weight} lbs)"
