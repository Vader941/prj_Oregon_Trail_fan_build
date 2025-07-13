"""
inventory.py - Defines the Inventory class for managing wagon supplies in the Oregon Trail parody game.

This module handles all inventory management including adding/removing items,
tracking weight, and simulating food spoilage based on weather and time.
"""

# Import statements - bring in code from other modules
import random      # For random number generation (used in spoilage simulation)
from datetime import datetime  # For date handling (used in spoilage calculations)

class Inventory:
    """
    Manages items and supplies for a wagon party
    
    The inventory system tracks quantities of items, calculates total weight,
    and simulates realistic food spoilage based on weather conditions.
    """
    
    def __init__(self):
        """
        Initialize an empty inventory
        
        __init__ is called when creating a new Inventory object.
        """
        # Dictionary to store items and their quantities
        # Key = item name (string), Value = quantity (integer)
        # Example: {"Food": 50, "Ammunition": 100, "Medicine": 10}
        self.items = {}

    def add_item(self, item_name, quantity=1):
        """
        Add items to the inventory
        
        Args:
            item_name: Name of the item to add (string)
            quantity: How many to add (integer, default: 1)
        """
        # Check if we already have this item
        if item_name in self.items:
            # Add to existing quantity using += (same as: self.items[item_name] = self.items[item_name] + quantity)
            self.items[item_name] += quantity
        else:
            # Create new entry for this item
            self.items[item_name] = quantity
        
        # Print confirmation message
        print(f"Added {quantity} x {item_name}")

    def remove_item(self, item_name, quantity=1):
        """
        Remove items from the inventory
        
        Args:
            item_name: Name of the item to remove (string)
            quantity: How many to remove (integer, default: 1)
            
        Returns:
            bool: True if removal was successful, False if not enough items
        """
        # Check if we have the item AND enough quantity
        # "and" means both conditions must be true
        if item_name in self.items and self.items[item_name] >= quantity:
            # Remove the requested quantity
            self.items[item_name] -= quantity
            
            # If quantity reaches 0, remove the item completely from the dictionary
            if self.items[item_name] == 0:
                # del removes a key-value pair from a dictionary
                del self.items[item_name]
            
            print(f"Removed {quantity} x {item_name}")
            return True  # Success
        
        # Not enough items to remove
        print(f"Failed to remove {quantity} x {item_name} (not enough in inventory)")
        return False  # Failure

    def check_item(self, item_name):
        """
        Check how many of an item we have
        
        Args:
            item_name: Name of the item to check (string)
            
        Returns:
            int: Quantity of the item (0 if we don't have any)
        """
        # .get() safely gets a value from a dictionary
        # If the key doesn't exist, it returns the default value (0)
        return self.items.get(item_name, 0)

    def list_inventory(self):
        """
        Display all items in the inventory
        
        This prints a formatted list of all items and their quantities.
        """
        # Check if inventory is empty
        # "not self.items" is True when the dictionary is empty
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Current Inventory:")
            # Loop through each item and quantity
            # .items() gets both key and value from each dictionary entry
            for item, quantity in self.items.items():
                print(f"- {item}: {quantity}")

    def total_weight(self, item_weights):
        """
        Calculate the total weight of all items in inventory
        
        Args:
            item_weights: Dictionary mapping item names to their weights
                         Example: {"Food": 2.5, "Ammunition": 0.1, "Medicine": 0.5}
            
        Returns:
            float: Total weight of all items
        """
        total = 0  # Start with 0 weight
        
        # Loop through each item in our inventory
        for item, qty in self.items.items():
            # Look up the weight of this item (default to 0 if not found)
            weight = item_weights.get(item, 0)
            # Add (weight per item × quantity) to the total
            total += weight * qty
        
        return total

    def spoil_food(self, quantity=1):
        """
        Convert fresh food to spoiled food
        
        This simulates food going bad during travel.
        
        Args:
            quantity: How many units of food to spoil (default: 1)
        """
        # Check if we have enough food to spoil
        if self.check_item("Food") >= quantity:
            # Remove fresh food
            self.remove_item("Food", quantity)
            # Add spoiled food (same quantity)
            self.add_item("Spoiled Food", quantity)
            print(f"⚠️ {quantity} units of food have spoiled.")
        else:
            print("⚠️ Not enough Food in inventory to spoil.")

    def simulate_spoilage(self, weather="clear", current_month=None):
        """
        Randomly spoil food based on weather and month conditions
        
        This simulates realistic food spoilage during travel. Hot weather
        and summer months increase spoilage rates.
        
        Args:
            weather: Current weather condition (string, default: "clear")
            current_month: Current month (1-12, default: current system month)
            
        Returns:
            int: Number of food units that spoiled
        """
        # === SPOILAGE RATES ===
        base_chance = 0.03    # 3% chance per food unit under normal conditions
        boosted_chance = 0.08 # 8% chance per food unit under harsh conditions
        
        # If no month is specified, use the current system month
        # datetime.now().month gets the current month (1-12)
        month = current_month if current_month else datetime.now().month

        # === DETERMINE SPOILAGE CHANCE ===
        # Check for conditions that increase spoilage
        # .lower() converts string to lowercase for consistent comparison
        # "in [7, 8]" checks if month is July (7) or August (8) - hot summer months
        if weather.lower() == "rain" or month in [7, 8]:
            chance = boosted_chance  # Use higher spoilage rate
        else:
            chance = base_chance     # Use normal spoilage rate

        # === SIMULATE SPOILAGE ===
        # Get current food amount
        food_amount = self.check_item("Food")
        spoiled_count = 0  # Counter for how much food spoils

        # Check each unit of food individually for spoilage
        # range(food_amount) creates a sequence: 0, 1, 2, ..., food_amount-1
        # The _ variable means we don't actually use the loop variable
        for _ in range(food_amount):
            # random.random() gives a number between 0.0 and 1.0
            # If it's less than our spoilage chance, this unit spoils
            if random.random() < chance:
                spoiled_count += 1

        # === APPLY SPOILAGE ===
        if spoiled_count > 0:
            # Actually spoil the food
            self.spoil_food(spoiled_count)
        else:
            # No spoilage occurred
            print("✅ No food spoiled this time.")

        # Return how much spoiled for other systems to use
        return spoiled_count
