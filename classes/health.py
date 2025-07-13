"""
Health system for Oregon Trail Fan Build

This module handles individual health tracking, status effects, and death mechanics.
Health is tracked on a 0-100 scale with status flags every 20 points.
"""

import random
from enum import Enum
from typing import Dict, List, Optional


class HealthStatus(Enum):
    """
    Health status categories based on 20% increments
    
    Enum is a special class that creates named constants.
    Instead of using numbers like 1, 2, 3, we use meaningful names.
    This makes code more readable and prevents errors.
    """
    # Each status represents a health range - comments show the numeric ranges
    EXCELLENT = "Excellent"      # 81-100 health points
    GOOD = "Good"               # 61-80 health points
    FAIR = "Fair"               # 41-60 health points
    POOR = "Poor"               # 21-40 health points
    CRITICAL = "Critical"       # 1-20 health points
    DEAD = "Dead"               # 0 health points


class HealthCondition(Enum):
    """
    Specific health conditions that can affect party members
    
    These represent different medical conditions or states that characters
    can have. Each condition affects health differently and may require
    different treatments.
    """
    # Base condition - when nothing is wrong
    HEALTHY = "Healthy"
    
    # Fatigue-related conditions
    EXHAUSTED = "Exhausted"          # From lack of sleep or overwork
    
    # Nutrition-related conditions  
    MALNOURISHED = "Malnourished"    # From lack of food over time
    
    # Illness conditions
    SICK = "Sick"                    # General illness (cold, flu, etc.)
    FEVERISH = "Feverish"           # High temperature, more serious than sick
    DYSENTERY = "Dysentery"         # Serious intestinal disease (common on trail)
    
    # Injury conditions
    INJURED = "Injured"             # General wounds or trauma
    BROKEN_BONE = "Broken Bone"     # Serious injury requiring long recovery


class Health:
    """
    Manages health for an individual party member
    
    Health factors:
    - Food consumption (daily requirement)
    - Rest quality and quantity
    - Weather exposure
    - Disease/injury events
    - Medicine and treatment
    - Base constitution from profession
    """
    
    def __init__(self, initial_health: int = 100, constitution_bonus: int = 0):
        """
        Initialize health system for an individual
        
        __init__ is a special method called when creating a new Health object.
        The parameters have default values (= 100, = 0) so they're optional.
        
        Args:
            initial_health: Starting health (0-100), defaults to 100
            constitution_bonus: Profession-based health modifier, defaults to 0
        """
        # max() and min() ensure health stays within valid bounds (0-100)
        # max(0, ...) prevents negative health
        # min(100, ...) prevents health over the base maximum
        self.current_health = max(0, min(100, initial_health + constitution_bonus))
        
        # Maximum health this character can have (base 100 + profession bonus)
        self.max_health = 100 + constitution_bonus
        
        # Store the bonus for reference (used in healing calculations)
        self.constitution_bonus = constitution_bonus
        
        # Tracking factors - these count consecutive days of problems
        self.days_without_food = 0    # Counter: days with insufficient food
        self.days_without_rest = 0    # Counter: days with insufficient sleep
        
        # List to track current health conditions
        # Starts with [HealthCondition.HEALTHY] - a list with one item
        self.conditions: List[HealthCondition] = [HealthCondition.HEALTHY]
        
        # Daily requirements - these are the minimum needed per day
        self.daily_food_requirement = 2.0  # pounds of food per day
        self.daily_rest_requirement = 8    # hours of sleep per day
        
        # Dictionary to track how long temporary conditions last
        # Key = condition, Value = days remaining
        # Dict[HealthCondition, int] means "dictionary with HealthCondition keys and int values"
        self.condition_timers: Dict[HealthCondition, int] = {}
        
        # Boolean flag - True means alive, False means dead
        self.is_alive = True
    
    def get_status(self) -> HealthStatus:
        """
        Get current health status category
        
        -> HealthStatus means this function returns a HealthStatus enum value
        This uses if/elif/else to check health ranges and return appropriate status.
        """
        # Check death first - if not alive OR health is 0 or below
        if not self.is_alive or self.current_health <= 0:
            return HealthStatus.DEAD
        # elif means "else if" - only check this if the previous condition was false
        elif self.current_health <= 20:
            return HealthStatus.CRITICAL
        elif self.current_health <= 40:
            return HealthStatus.POOR
        elif self.current_health <= 60:
            return HealthStatus.FAIR
        elif self.current_health <= 80:
            return HealthStatus.GOOD
        else:  # If none of the above conditions are true, health must be > 80
            return HealthStatus.EXCELLENT
    
    def get_health_description(self) -> str:
        """
        Get detailed health description including conditions
        
        -> str means this function returns a string (text)
        This builds a descriptive text showing health status and any conditions.
        """
        # Get the basic status (Excellent, Good, etc.)
        status = self.get_status()
        
        # Special case: if dead, just return "Dead"
        if status == HealthStatus.DEAD:
            return "Dead"
        
        # Build description string: "Status (current/max)"
        # .value gets the string value from the enum (e.g., "Excellent")
        # f"..." is an f-string - puts variable values into the text
        description = f"{status.value} ({self.current_health}/100)"
        
        # Add active conditions (excluding healthy)
        # List comprehension: [item for item in list if condition]
        # This creates a new list with only conditions that aren't HEALTHY
        active_conditions = [c for c in self.conditions if c != HealthCondition.HEALTHY]
        
        # if active_conditions: checks if the list has any items
        if active_conditions:
            # Get the string names of all conditions
            condition_names = [c.value for c in active_conditions]
            # ', '.join() combines list items with commas: ["A", "B"] becomes "A, B"
            description += f" - {', '.join(condition_names)}"
        
        return description
    
    def consume_food(self, food_amount: float) -> bool:
        """
        Daily food consumption tracking
        
        Args:
            food_amount: Pounds of food consumed today
            
        Returns:
            bool: True if daily requirement met, False otherwise
        """
        # Check if enough food was consumed
        if food_amount >= self.daily_food_requirement:
            # Requirement met - reset the counter to 0
            self.days_without_food = 0
            return True  # Return True to indicate success
        else:
            # Not enough food - increment the counter
            # += means "add to the current value" (same as: self.days_without_food = self.days_without_food + 1)
            self.days_without_food += 1
            return False  # Return False to indicate problem
    
    def get_rest(self, hours: int, quality_modifier: float = 1.0) -> bool:
        """
        Daily rest tracking
        
        Args:
            hours: Hours of rest received
            quality_modifier: Quality of rest (0.5 = poor, 1.0 = normal, 1.5 = excellent)
            
        Returns:
            bool: True if daily requirement met, False otherwise
        """
        # Calculate effective rest by multiplying hours by quality
        # Poor conditions (0.5) make rest less effective
        # Good conditions (1.5) make rest more effective
        effective_rest = hours * quality_modifier
        
        # Check if effective rest meets the daily requirement
        if effective_rest >= self.daily_rest_requirement:
            # Requirement met - reset the counter
            self.days_without_rest = 0
            return True
        else:
            # Not enough rest - increment the counter
            self.days_without_rest += 1
            return False
    
    def add_condition(self, condition: HealthCondition, duration_days: int = 0):
        """
        Add a health condition to this character
        
        Args:
            condition: The condition to add (e.g., HealthCondition.SICK)
            duration_days: Days until condition resolves (0 = permanent until treated)
        """
        # Only add the condition if it's not already in the list
        # "not in" checks if something is NOT in a list
        if condition not in self.conditions:
            # .append() adds an item to the end of a list
            self.conditions.append(condition)
            
        # Remove healthy status if adding a negative condition
        # If we're adding something other than HEALTHY, and HEALTHY is in the list
        if condition != HealthCondition.HEALTHY and HealthCondition.HEALTHY in self.conditions:
            # .remove() takes an item out of a list
            self.conditions.remove(HealthCondition.HEALTHY)
        
        # Set timer for temporary conditions
        # If duration_days is greater than 0, this condition will automatically go away
        if duration_days > 0:
            # Add to the dictionary: condition_timers[condition] = duration_days
            self.condition_timers[condition] = duration_days
    
    def remove_condition(self, condition: HealthCondition):
        """
        Remove a health condition from this character
        
        Args:
            condition: The condition to remove
        """
        # Remove from conditions list if it exists
        if condition in self.conditions:
            self.conditions.remove(condition)
            
        # Remove from timers dictionary if it exists
        # "in" works with dictionaries too - it checks the keys
        if condition in self.condition_timers:
            # del removes a key-value pair from a dictionary
            del self.condition_timers[condition]
        
        # If no negative conditions remain, set character back to healthy
        # len() gets the length/size of a list
        if len(self.conditions) == 0:
            self.conditions.append(HealthCondition.HEALTHY)
    
    def apply_medicine(self, medicine_type: str, effectiveness: float = 0.8):
        """
        Apply medicine or treatment to this character
        
        Args:
            medicine_type: Type of medicine used (for logging/display)
            effectiveness: How effective the treatment is (0.0-1.0, where 1.0 = 100% effective)
        """
        # Calculate healing amount using random number generation
        # random.randint(5, 15) gives a random integer between 5 and 15 (inclusive)
        # Multiply by effectiveness to reduce healing if medicine isn't fully effective
        healing = random.randint(5, 15) * effectiveness
        
        # Apply the healing using our modify_health method
        self.modify_health(healing, f"Medicine: {medicine_type}")
        
        # Chance to cure specific conditions
        # random.random() gives a decimal between 0.0 and 1.0
        # If it's less than effectiveness, the medicine successfully cures a condition
        if random.random() < effectiveness:
            # List of conditions that medicine can cure
            curable_conditions = [
                HealthCondition.SICK, 
                HealthCondition.FEVERISH,
                HealthCondition.DYSENTERY
            ]
            
            # Try to cure one condition
            # Loop through each curable condition
            for condition in curable_conditions:
                # If the character has this condition
                if condition in self.conditions:
                    # Remove it and stop looking (break exits the loop)
                    self.remove_condition(condition)
                    break  # Only cure one condition per medicine use
    
    def apply_weather_exposure(self, weather: str, protection_level: float = 1.0):
        """
        Apply weather effects to this character
        
        Args:
            weather: Weather type (hot, cold, rain, etc.)
            protection_level: How well protected (0.0 = no protection, 1.0 = full protection)
        """
        exposure_damage = 0  # Start with no damage
        
        # Dictionary mapping weather types to base damage amounts
        # Dictionaries use {key: value} syntax
        weather_effects = {
            "hot": 3,      # Hot weather causes moderate damage
            "cold": 4,     # Cold weather causes more damage
            "rain": 2,     # Rain causes mild damage
            "snow": 6,     # Snow causes significant damage
            "storm": 8     # Storms cause the most damage
        }
        
        # Look up the base damage for this weather type
        # .get() safely gets a value from a dictionary, with a default if key doesn't exist
        # .lower() converts the string to lowercase to handle "Rain", "RAIN", "rain" all the same
        base_damage = weather_effects.get(weather.lower(), 1)  # Default to 1 if weather not found
        
        # Calculate actual damage based on protection level
        # (1.0 - protection_level) gives the exposure amount
        # Full protection (1.0) means no exposure: (1.0 - 1.0) = 0
        # No protection (0.0) means full exposure: (1.0 - 0.0) = 1.0
        exposure_damage = base_damage * (1.0 - protection_level)
        
        # Only apply damage if there's actual exposure
        if exposure_damage > 0:
            # Apply negative health change (- makes it negative)
            self.modify_health(-exposure_damage, f"Weather exposure: {weather}")
            
            # Chance of getting sick from exposure
            # Higher exposure damage = higher chance of getting sick
            # exposure_damage / 20 converts damage to a probability (0.0 to 1.0)
            if random.random() < (exposure_damage / 20):
                # Add sick condition for 3-7 days
                # random.randint(3, 7) gives a random number between 3 and 7
                self.add_condition(HealthCondition.SICK, duration_days=random.randint(3, 7))
    
    def daily_health_update(self):
        """
        Process daily health changes based on current conditions
        This should be called once per game day to update the character's health.
        """
        # Don't process updates for dead characters
        if not self.is_alive:
            return  # return exits the function early
        
        health_change = 0  # Track total health change for the day
        reasons = []       # List to store reasons for health changes (for logging)
        
        # === FOOD EFFECTS ===
        # Check if character has gone days without enough food
        if self.days_without_food > 0:
            # Damage increases each day: day 1 = -2, day 2 = -4, day 3 = -6, etc.
            malnutrition_damage = self.days_without_food * 2
            health_change -= malnutrition_damage  # -= means "subtract from"
            reasons.append(f"Lack of food: -{malnutrition_damage}")
            
            # Add malnourished condition after 2 days without food
            if self.days_without_food >= 2:
                self.add_condition(HealthCondition.MALNOURISHED)
        
        # === REST EFFECTS ===
        # Check if character has gone days without enough rest
        if self.days_without_rest > 0:
            # Exhaustion damage: 1.5 points per day without rest
            exhaustion_damage = self.days_without_rest * 1.5
            health_change -= exhaustion_damage
            reasons.append(f"Lack of rest: -{exhaustion_damage}")
            
            # Add exhausted condition after just 1 day without rest
            if self.days_without_rest >= 1:
                self.add_condition(HealthCondition.EXHAUSTED)
        
        # === CONDITION EFFECTS ===
        # Dictionary showing how much damage each condition does per day
        condition_effects = {
            HealthCondition.SICK: -3,           # Mild illness
            HealthCondition.INJURED: -2,        # Physical injury
            HealthCondition.FEVERISH: -4,       # More serious illness
            HealthCondition.BROKEN_BONE: -1,    # Slow healing injury
            HealthCondition.DYSENTERY: -5,      # Serious disease
            HealthCondition.MALNOURISHED: -2,   # Ongoing nutrition problems
            HealthCondition.EXHAUSTED: -1       # Fatigue effects
        }
        
        # Loop through each condition the character currently has
        for condition in self.conditions:
            # Check if this condition causes damage
            if condition in condition_effects:
                # Get the damage amount (negative number)
                damage = condition_effects[condition]
                health_change += damage  # Add the damage (which is negative)
                reasons.append(f"{condition.value}: {damage}")
        
        # === NATURAL HEALING ===
        # Healthy characters slowly recover on their own
        # Check if character is healthy AND below maximum health
        if HealthCondition.HEALTHY in self.conditions and self.current_health < self.max_health:
            # Random healing between 1-3 points per day
            healing = random.randint(1, 3)
            health_change += healing  # Add positive healing
            reasons.append(f"Natural healing: +{healing}")
        
        # === APPLY ALL CHANGES ===
        # Only modify health if there was some change
        if health_change != 0:
            # Join all reasons with commas: ["reason1", "reason2"] becomes "reason1, reason2"
            self.modify_health(health_change, ", ".join(reasons))
        
        # === UPDATE TIMERS ===
        # Handle temporary conditions (reduce their remaining time)
        self._update_condition_timers()
        
        # === CHECK FOR DEATH ===
        # If health dropped to 0 or below, handle death
        if self.current_health <= 0:
            self._handle_death()
    
    def modify_health(self, amount: int, reason: str = ""):
        """
        Modify health by a specific amount
        
        Args:
            amount: Health change (positive = heal, negative = damage)
            reason: Reason for the change (for logging/debugging)
        """
        # Don't modify health of dead characters
        if not self.is_alive:
            return
        
        # Store old health for logging
        old_health = self.current_health
        
        # Calculate new health, keeping it within valid bounds
        # max(0, ...) prevents health from going below 0
        # min(self.max_health, ...) prevents health from going above maximum
        self.current_health = max(0, min(self.max_health, self.current_health + amount))
        
        # Log significant changes for debugging/information
        # abs() gets the absolute value (removes negative sign)
        # Only log changes of 5 or more points to avoid spam
        if abs(amount) >= 5:
            print(f"Health change: {old_health} -> {self.current_health} ({reason})")
    
    def _update_condition_timers(self):
        """
        Update and remove expired temporary conditions
        
        Methods starting with _ are "private" - meant for internal use only.
        This is called automatically by daily_health_update().
        """
        expired_conditions = []  # List to store conditions that have expired
        
        # Loop through each condition that has a timer
        # .items() gets both the key and value from a dictionary
        for condition, days_remaining in self.condition_timers.items():
            # Reduce the timer by 1 day
            days_remaining -= 1
            
            # Check if the condition has expired (timer reached 0)
            if days_remaining <= 0:
                # Add to expired list (we'll remove these after the loop)
                expired_conditions.append(condition)
            else:
                # Update the timer with the new value
                self.condition_timers[condition] = days_remaining
        
        # Remove all expired conditions
        # We do this in a separate loop to avoid changing the dictionary while iterating
        for condition in expired_conditions:
            self.remove_condition(condition)
    
    def _handle_death(self):
        """
        Handle character death
        
        This is a private method (starts with _) called when health reaches 0.
        """
        self.is_alive = False        # Set alive flag to False
        self.current_health = 0      # Ensure health is exactly 0
        self.conditions = []         # Clear all conditions (dead people have no conditions)
        print(f"Character has died.")  # Print death message
    
    def get_survival_chance(self) -> float:
        """
        Calculate daily survival chance based on current health
        Used for random death events in critical condition
        
        Returns:
            float: Probability of surviving the day (0.0 to 1.0)
                  0.0 = 0% chance (certain death)
                  1.0 = 100% chance (certain survival)
        """
        # Dead characters have no survival chance
        if self.current_health <= 0:
            return 0.0
        # Very low health: 30% chance of death per day
        elif self.current_health <= 10:
            return 0.7  # 70% survival chance
        # Critical health: 10% chance of death per day  
        elif self.current_health <= 20:
            return 0.9  # 90% survival chance
        else:
            # Above critical: very low chance of random death
            return 0.99  # 99% survival chance
    
    def __str__(self):
        """
        String representation of health status
        
        __str__ is a special method that defines what happens when you
        convert this object to a string (like when printing it).
        """
        return self.get_health_description()
