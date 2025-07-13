"""
wagon.py - Defines the Wagon class and loads wagon types from a JSON file.

This module handles different types of wagons that can be used for the journey.
Each wagon type has different capacities, costs, and breakdown chances.
"""

# Import statements - bring in code from other modules
import json  # For reading JSON files
import os    # For file path operations

# === LOAD WAGON DATA ===
# Build the path to the wagons.json file
# Same pattern as other classes - go up one directory, then into data/
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'wagons.json')

# Try to load the wagons file
try:
    # Open and read the JSON file
    with open(DATA_PATH, 'r') as f:
        # json.load() converts JSON data to a Python dictionary
        WAGON_TYPES = json.load(f)
except FileNotFoundError:
    # If file doesn't exist, print warning and use empty dictionary
    print("Warning: wagons.json not found. Defaulting to empty wagon list.")
    WAGON_TYPES = {}  # Empty dictionary

class Wagon:
    """
    Represents a wagon used for the Oregon Trail journey
    
    Different wagon types have different carrying capacities, costs,
    and chances of breaking down during travel.
    """
    
    def __init__(self, wagon_type):
        """
        Create a new wagon of the specified type
        
        Args:
            wagon_type: Type of wagon (must exist in wagons.json, defaults to "Standard")
        """
        # Validate wagon type - use "Standard" if the requested type doesn't exist
        self.wagon_type = wagon_type if wagon_type in WAGON_TYPES else "Standard"
        
        # Get the statistics for this wagon type
        # .get() returns an empty dictionary {} if the wagon type isn't found
        wagon_stats = WAGON_TYPES.get(self.wagon_type, {})

        # === WAGON PROPERTIES ===
        # Load properties from the wagon data, with sensible defaults
        self.cost = wagon_stats.get("cost", 0)                           # How much the wagon costs (default: 0)
        self.capacity = wagon_stats.get("capacity", 0)                   # Maximum weight it can carry (default: 0)
        self.breakdown_chance = wagon_stats.get("breakdown_chance", 0.2) # Probability of breakdown (default: 0.2 = 20%)
        self.repair_difficulty = wagon_stats.get("repair_difficulty", "Medium")  # How hard to repair (default: "Medium")
        
        # === CURRENT STATE ===
        self.current_load = 0  # How much weight is currently loaded (starts at 0)

    def can_add_cargo(self, weight):
        """
        Check if we can add more cargo without exceeding capacity
        
        Args:
            weight: Weight of cargo to add (float or int)
            
        Returns:
            bool: True if cargo can be added, False if it would exceed capacity
        """
        # Check if current load + new weight is less than or equal to capacity
        # <= means "less than or equal to"
        return (self.current_load + weight) <= self.capacity

    def add_cargo(self, weight):
        """
        Add cargo to the wagon if there's room
        
        Args:
            weight: Weight of cargo to add (float or int)
            
        Returns:
            bool: True if cargo was added successfully, False if there wasn't room
        """
        # First check if we can add this cargo
        if self.can_add_cargo(weight):
            # Add the weight to our current load
            self.current_load += weight
            return True  # Success
        
        # Not enough room
        return False  # Failure

    def __str__(self):
        """
        String representation of this wagon
        
        __str__ defines what happens when you convert this object to a string.
        
        Returns:
            str: Formatted description of the wagon and its status
        """
        # Return a detailed string with all important wagon information
        # Multiply breakdown_chance by 100 to show as percentage
        return (
            f"{self.wagon_type} Wagon | Capacity: {self.capacity} lbs | "
            f"Current Load: {self.current_load} lbs | Breakdown Chance: {self.breakdown_chance * 100}% | "
            f"Repair Difficulty: {self.repair_difficulty}"
        )
