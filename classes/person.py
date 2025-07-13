"""
person.py - Defines the Person class and loads available professions from a JSON file.

This module handles individual characters in the Oregon Trail game, including their
profession, health system, and daily updates.
"""

# Import statements - these bring in code from other files
import json  # For reading JSON files
import os    # For file path operations
from classes.health import Health, HealthStatus  # Our custom health system

# === LOAD PROFESSIONS DATA ===
# Build the path to the professions.json file
# __file__ is the current file (person.py)
# os.path.dirname() gets the directory containing this file (classes/)
# '..' means go up one directory level (to the main project folder)
# Then we go into the 'data' folder and get 'professions.json'
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'professions.json')

# Try to load the professions file
try:
    # 'with open()' safely opens and automatically closes files
    # 'r' means read mode (we're only reading, not writing)
    # 'as f' creates a variable called 'f' that represents the file
    with open(DATA_PATH, 'r') as f:
        # json.load() reads the JSON file and converts it to a Python dictionary
        PROFESSIONS = json.load(f)
except FileNotFoundError:
    # If the file doesn't exist, print a warning and use an empty dictionary
    print("Warning: professions.json not found. Defaulting to empty profession list.")
    PROFESSIONS = {}  # Empty dictionary

class Person:
    """
    Represents a single character/person in the Oregon Trail game
    
    Each person has a name, age, profession, and health system.
    They can be updated daily with food, rest, and other factors.
    """
    
    def __init__(self, name, age, profession):
        """
        Create a new person
        
        Args:
            name: The person's name (string)
            age: The person's age (integer)
            profession: The person's job/profession (string)
        """
        # Basic character information
        self.name = name
        self.age = age
        
        # Validate profession - if it's not in our PROFESSIONS list, default to "Farmer"
        # "in PROFESSIONS" checks if the profession exists as a key in the dictionary
        self.profession = profession if profession in PROFESSIONS else "Farmer"
        
        # === GET PROFESSION-SPECIFIC HEALTH MODIFIERS ===
        # Get the profession data from the PROFESSIONS dictionary
        # .get() safely gets a value, returning {} (empty dict) if profession not found
        profession_data = PROFESSIONS.get(self.profession, {})
        
        # Get the health bonus for this profession, defaulting to 0 if not specified
        constitution_bonus = profession_data.get("health_bonus", 0)
        
        # === INITIALIZE HEALTH SYSTEM ===
        # Create a new Health object with initial health and profession bonus
        self.health_system = Health(initial_health=100, constitution_bonus=constitution_bonus)
        
        # === LEGACY COMPATIBILITY ===
        # Keep a simple health property for backwards compatibility with older code
        self.health = self.health_system.current_health
        self.status = "Alive"  # Simple alive/dead status

        # === SPECIAL FLAGS ===
        # Check if this is a solo traveler (special profession with unique rules)
        # == checks if two things are equal
        self.is_solo = self.profession == "Solo Traveler"

    def apply_profession_effects(self):
        """
        Apply profession-specific effects and display them
        
        This is currently a placeholder that just prints the effects.
        In the future, this could actually apply gameplay bonuses/penalties.
        """
        print(f"Applying effects for profession: {self.profession}")
        
        # Get the effects data for this profession
        effects = PROFESSIONS.get(self.profession, {})
        
        # Print all advantages
        # .get() returns an empty list [] if "advantages" key doesn't exist
        for adv in effects.get("advantages", []):
            print(f"Advantage: {adv}")
            
        # Print all disadvantages
        for disadv in effects.get("disadvantages", []):
            print(f"Disadvantage: {disadv}")
    
    def daily_update(self, food_consumed=0, rest_hours=8, rest_quality=1.0):
        """
        Process daily health updates for this person
        
        This should be called once per game day to update the person's health
        based on their food consumption, rest, and other factors.
        
        Args:
            food_consumed: Pounds of food consumed today (default: 0)
            rest_hours: Hours of rest received (default: 8)
            rest_quality: Quality of rest multiplier (0.5-1.5, default: 1.0)
        """
        # === UPDATE DAILY NEEDS ===
        # Tell the health system about food and rest consumption
        self.health_system.consume_food(food_consumed)
        self.health_system.get_rest(rest_hours, rest_quality)
        
        # === PROCESS HEALTH CHANGES ===
        # Let the health system calculate and apply all daily health changes
        self.health_system.daily_health_update()
        
        # === UPDATE LEGACY PROPERTIES ===
        # Keep the simple properties in sync with the health system
        self.health = self.health_system.current_health
        
        # Update status based on whether the person is still alive
        self.status = "Dead" if not self.health_system.is_alive else "Alive"
    
    def get_health_status(self):
        """
        Get detailed health status description
        
        Returns:
            str: Detailed health description including status and conditions
        """
        return self.health_system.get_health_description()
    
    def is_alive(self):
        """
        Check if this person is alive
        
        Returns:
            bool: True if alive, False if dead
        """
        return self.health_system.is_alive
    
    def apply_medicine(self, medicine_type, effectiveness=0.8):
        """
        Apply medicine to this person
        
        Args:
            medicine_type: Type of medicine being used (for display/logging)
            effectiveness: How effective the medicine is (0.0-1.0, default: 0.8)
        """
        # Use the health system to apply medicine
        self.health_system.apply_medicine(medicine_type, effectiveness)
        
        # Update the legacy health property to stay in sync
        self.health = self.health_system.current_health
    
    def apply_weather_exposure(self, weather, protection=1.0):
        """
        Apply weather effects to this person
        
        Args:
            weather: Weather type (hot, cold, rain, snow, storm, etc.)
            protection: Protection level (0.0 = no protection, 1.0 = full protection)
        """
        # Use the health system to apply weather effects
        self.health_system.apply_weather_exposure(weather, protection)
        
        # Update the legacy health property to stay in sync
        self.health = self.health_system.current_health

    def __str__(self):
        """
        String representation of this person
        
        __str__ is a special method that defines what happens when you
        convert this object to a string (like when printing it).
        
        Returns:
            str: Formatted string with person's details
        """
        # Get detailed health description from the health system
        health_desc = self.health_system.get_health_description()
        
        # Return a formatted string with all the person's information
        # f"..." is an f-string that lets us put variables into the text
        return f"{self.name}, Age {self.age}, Profession: {self.profession}, Health: {health_desc}, Status: {self.status}"
