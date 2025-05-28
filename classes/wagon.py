"""
wagon.py - Defines the Wagon class and loads wagon types from a JSON file.
"""

import json
import os

# Load wagon types from JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'wagons.json')
try:
    with open(DATA_PATH, 'r') as f:
        WAGON_TYPES = json.load(f)
except FileNotFoundError:
    print("Warning: wagons.json not found. Defaulting to empty wagon list.")
    WAGON_TYPES = {}

class Wagon:
    def __init__(self, wagon_type):
        self.wagon_type = wagon_type if wagon_type in WAGON_TYPES else "Standard"
        wagon_stats = WAGON_TYPES.get(self.wagon_type, {})

        self.cost = wagon_stats.get("cost", 0)
        self.capacity = wagon_stats.get("capacity", 0)
        self.breakdown_chance = wagon_stats.get("breakdown_chance", 0.2)
        self.repair_difficulty = wagon_stats.get("repair_difficulty", "Medium")
        self.current_load = 0

    def can_add_cargo(self, weight):
        return (self.current_load + weight) <= self.capacity

    def add_cargo(self, weight):
        if self.can_add_cargo(weight):
            self.current_load += weight
            return True
        return False

    def __str__(self):
        return (
            f"{self.wagon_type} Wagon | Capacity: {self.capacity} lbs | "
            f"Current Load: {self.current_load} lbs | Breakdown Chance: {self.breakdown_chance * 100}% | "
            f"Repair Difficulty: {self.repair_difficulty}"
        )
