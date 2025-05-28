"""
person.py - Defines the Person class and loads available professions from a JSON file.
"""

import json
import os

# Load professions from JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'professions.json')
try:
    with open(DATA_PATH, 'r') as f:
        PROFESSIONS = json.load(f)
except FileNotFoundError:
    print("Warning: professions.json not found. Defaulting to empty profession list.")
    PROFESSIONS = {}

class Person:
    def __init__(self, name, age, profession):
        self.name = name
        self.age = age
        self.profession = profession if profession in PROFESSIONS else "Farmer"
        self.health = 100  # out of 100
        self.status = "Alive"

        # Solo traveler flag
        self.is_solo = self.profession == "Solo Traveler"

    def apply_profession_effects(self):
        """Applies profession-specific effects. Placeholder for now."""
        print(f"Applying effects for profession: {self.profession}")
        effects = PROFESSIONS.get(self.profession, {})
        for adv in effects.get("advantages", []):
            print(f"Advantage: {adv}")
        for disadv in effects.get("disadvantages", []):
            print(f"Disadvantage: {disadv}")

    def __str__(self):
        return f"{self.name}, Age {self.age}, Profession: {self.profession}, Health: {self.health}, Status: {self.status}"
