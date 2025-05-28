"""
inventory.py - Defines the Inventory class for managing wagon supplies in the Oregon Trail parody game.
"""

import random
from datetime import datetime

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity=1):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        print(f"Added {quantity} x {item_name}")

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
            print(f"Removed {quantity} x {item_name}")
            return True
        print(f"Failed to remove {quantity} x {item_name} (not enough in inventory)")
        return False

    def check_item(self, item_name):
        return self.items.get(item_name, 0)

    def list_inventory(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Current Inventory:")
            for item, quantity in self.items.items():
                print(f"- {item}: {quantity}")

    def total_weight(self, item_weights):
        total = 0
        for item, qty in self.items.items():
            weight = item_weights.get(item, 0)
            total += weight * qty
        return total

    def spoil_food(self, quantity=1):
        if self.check_item("Food") >= quantity:
            self.remove_item("Food", quantity)
            self.add_item("Spoiled Food", quantity)
            print(f"⚠️ {quantity} units of food have spoiled.")
        else:
            print("⚠️ Not enough Food in inventory to spoil.")

    def simulate_spoilage(self, weather="clear", current_month=None):
        """Randomly spoils food based on weather and month conditions."""
        base_chance = 0.03  # 3%
        boosted_chance = 0.08  # 8%
        month = current_month if current_month else datetime.now().month

        # Check for boosted spoilage conditions
        if weather.lower() == "rain" or month in [7, 8]:  # July or August
            chance = boosted_chance
        else:
            chance = base_chance

        food_amount = self.check_item("Food")
        spoiled_count = 0

        for _ in range(food_amount):
            if random.random() < chance:
                spoiled_count += 1

        if spoiled_count > 0:
            self.spoil_food(spoiled_count)
        else:
            print("✅ No food spoiled this time.")

        return spoiled_count
