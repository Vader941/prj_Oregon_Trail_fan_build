"""
item.py - Defines the Item class and loads item types from a JSON file.

This module handles individual items that can be stored in inventory.
Each item has properties like weight, whether it can spoil, etc.
"""

# Import statements - bring in code from other modules
import json  # For reading JSON files
import os    # For file path operations

# === LOAD ITEM DATA ===
# Build the path to the items.json file
# This follows the same pattern as person.py - go up one directory, then into data/
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.json')

# Try to load the items file
try:
    # Open and read the JSON file
    with open(DATA_PATH, 'r') as f:
        # json.load() converts JSON data to a Python dictionary
        ITEM_TYPES = json.load(f)
except FileNotFoundError:
    # If file doesn't exist, print warning and use empty dictionary
    print("Warning: items.json not found. Defaulting to empty item type list.")
    ITEM_TYPES = {}  # Empty dictionary

class Item:
    """
    Represents a single type of item with its properties
    
    Items are defined in the items.json file and have properties like
    weight, whether they can spoil, if they're consumable, etc.
    """
    
    def __init__(self, name):
        """
        Create a new item based on its name
        
        Args:
            name: The name of the item type (must exist in items.json)
            
        Raises:
            ValueError: If the item type is not defined in items.json
        """
        # Check if this item type exists in our loaded data
        if name in ITEM_TYPES:
            # Get the properties for this item type
            props = ITEM_TYPES[name]
            
            # === BASIC PROPERTIES ===
            self.name = name
            # .get() safely gets a value from dictionary, with default if key missing
            self.weight = props.get("weight", 0)              # How much it weighs (default: 0)
            self.description = props.get("description", "")   # Description text (default: empty)
            
            # === BEHAVIOR FLAGS ===
            # These are boolean (True/False) properties that control how the item behaves
            self.can_spoil = props.get("can_spoil", False)     # Can this item go bad? (default: False)
            self.wears_out = props.get("wears_out", False)     # Does this item wear out with use? (default: False)
            self.usable = props.get("usable", False)           # Can this item be used/activated? (default: False)
            self.consumable = props.get("consumable", False)   # Is this item consumed when used? (default: False)
            self.spoiled = props.get("spoiled", False)         # Is this item currently spoiled? (default: False)
        else:
            # Item type not found - raise an error
            # ValueError is a type of exception (error) that indicates invalid input
            raise ValueError(f"Item type '{name}' is not defined.")

    def __str__(self):
        """
        String representation of this item
        
        __str__ defines what happens when you convert this object to a string.
        
        Returns:
            str: Formatted description of the item
        """
        # Return a formatted string with name, description, and weight
        return f"{self.name}: {self.description} (Weight: {self.weight} lbs)"
