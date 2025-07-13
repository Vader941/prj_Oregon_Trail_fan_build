"""
Health System Demo - Oregon Trail Fan Build

Demonstrates the new health system with multiple scenarios:
- Daily survival with adequate resources
- Starvation effects
- Weather exposure
- Disease and medicine
- Death mechanics
"""

import sys
import os

# Add the classes directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))

# Import classes
from classes.party import Party
from classes.health import HealthCondition


def demo_basic_survival():
    """Demo basic daily survival with good conditions"""
    print("=== BASIC SURVIVAL DEMO ===")
    party = Party("John", 35, "Farmer")
    party.add_member("Mary", 32, "Doctor")
    party.add_member("Tommy", 12, "Farmer")
    
    print("Initial party status:")
    print(party.get_detailed_party_report())
    print()
    
    # Simulate 5 days of good conditions
    for day in range(1, 6):
        print(f"--- Day {day} ---")
        daily_report = party.daily_party_update(
            food_available=8.0,  # Plenty of food (4 pounds per person)
            rationing_level=1.0,
            rest_hours=8,
            rest_quality=1.0,
            weather="fair",
            shelter_quality=1.0,
            medicine_used=0
        )
        
        print(f"Food: {daily_report['food_distribution']['food_used']:.1f} lbs used")
        print(f"Average Health: {daily_report['party_status']['average_health']}")
        print()
    
    print("Final status after good conditions:")
    print(party.get_detailed_party_report())
    print("\n" + "="*50 + "\n")


def demo_starvation():
    """Demo starvation effects"""
    print("=== STARVATION DEMO ===")
    party = Party("Bob", 40, "Banker")
    party.add_member("Alice", 38, "Carpenter")
    
    print("Starting starvation scenario...")
    print(party.get_detailed_party_report())
    print()
    
    # Simulate 10 days of starvation
    for day in range(1, 11):
        print(f"--- Day {day} ---")
        daily_report = party.daily_party_update(
            food_available=1.0,  # Very little food
            rationing_level=0.5,  # Half rations
            rest_hours=6,  # Poor rest
            rest_quality=0.8,
            weather="fair",
            shelter_quality=1.0,
            medicine_used=0
        )
        
        print(f"Food per person: {daily_report['food_distribution'].get('food_per_person', 0):.2f} lbs")
        print(f"Average Health: {daily_report['party_status']['average_health']}")
        
        if daily_report['deaths_today']:
            print(f"Deaths today: {', '.join(daily_report['deaths_today'])}")
        
        if daily_report['game_over']:
            print("GAME OVER!")
            break
        print()
    
    print("Final status after starvation:")
    print(party.get_detailed_party_report())
    print("\n" + "="*50 + "\n")


def demo_weather_exposure():
    """Demo weather exposure effects"""
    print("=== WEATHER EXPOSURE DEMO ===")
    party = Party("Sarah", 28, "Solo Traveler")  # Solo traveler has health penalty
    
    print("Starting weather exposure scenario...")
    print(party.get_detailed_party_report())
    print()
    
    weather_sequence = ["rain", "cold", "storm", "snow", "hot", "fair"]
    
    for day, weather in enumerate(weather_sequence, 1):
        print(f"--- Day {day} - Weather: {weather} ---")
        daily_report = party.daily_party_update(
            food_available=2.5,  # Adequate food
            rationing_level=1.0,
            rest_hours=8,
            rest_quality=1.0,
            weather=weather,
            shelter_quality=0.3 if weather in ["storm", "snow"] else 0.7,  # Poor shelter
            medicine_used=0
        )
        
        print(f"Health: {daily_report['party_status']['average_health']}")
        
        # Show member conditions
        for member in party.get_living_members():
            conditions = [c.value for c in member.health_system.conditions if c != HealthCondition.HEALTHY]
            if conditions:
                print(f"  {member.name}: {', '.join(conditions)}")
        
        if daily_report['game_over']:
            print("GAME OVER!")
            break
        print()
    
    print("Final status after weather exposure:")
    print(party.get_detailed_party_report())
    print("\n" + "="*50 + "\n")


def demo_medicine_treatment():
    """Demo disease and medicine treatment"""
    print("=== MEDICINE TREATMENT DEMO ===")
    party = Party("Doc", 45, "Doctor")  # Doctor has health bonus
    party.add_member("Patient", 30, "Farmer")
    
    print("Starting medicine treatment scenario...")
    
    # Manually add some conditions to demonstrate treatment
    party.members[1].health_system.add_condition(HealthCondition.SICK, 5)
    party.members[1].health_system.add_condition(HealthCondition.FEVERISH, 3)
    party.members[1].health_system.modify_health(-30, "Initial sickness")
    party.members[1].health = party.members[1].health_system.current_health
    
    print(party.get_detailed_party_report())
    print()
    
    # Simulate treatment over several days
    for day in range(1, 8):
        print(f"--- Day {day} ---")
        medicine_to_use = 1 if day <= 3 else 0  # Use medicine first 3 days
        
        daily_report = party.daily_party_update(
            food_available=6.0,  # Good food
            rationing_level=1.2,  # Extra rations for recovery
            rest_hours=10,  # Extra rest
            rest_quality=1.2,
            weather="fair",
            shelter_quality=1.0,
            medicine_used=medicine_to_use
        )
        
        print(f"Medicine used: {daily_report['treatment']['medicine_used']}")
        print(f"Members treated: {daily_report['treatment']['members_treated']}")
        
        for member in party.get_living_members():
            conditions = [c.value for c in member.health_system.conditions if c != HealthCondition.HEALTHY]
            condition_str = f" ({', '.join(conditions)})" if conditions else " (Healthy)"
            print(f"  {member.name}: {member.health}/100{condition_str}")
        print()
    
    print("Final status after treatment:")
    print(party.get_detailed_party_report())
    print("\n" + "="*50 + "\n")


def demo_profession_differences():
    """Demo how different professions handle health differently"""
    print("=== PROFESSION DIFFERENCES DEMO ===")
    
    # Create parties with different professions
    parties = {
        "Doctor": Party("Dr. Smith", 40, "Doctor"),
        "Banker": Party("Mr. Rich", 35, "Banker"),
        "Solo Traveler": Party("Lone Wolf", 30, "Solo Traveler")
    }
    
    print("Initial health values by profession:")
    for prof, party in parties.items():
        member = party.members[0]
        print(f"{prof}: {member.health}/100 (max: {member.health_system.max_health})")
    print()
    
    # Simulate harsh conditions for all
    for day in range(1, 6):
        print(f"--- Day {day} ---")
        for prof, party in parties.items():
            daily_report = party.daily_party_update(
                food_available=1.5,  # Limited food
                rationing_level=0.8,
                rest_hours=6,
                rest_quality=0.7,
                weather="cold",
                shelter_quality=0.6,
                medicine_used=0
            )
            
            member = party.members[0]
            print(f"{prof}: {member.health}/100")
        print()
    
    print("Final health comparison:")
    for prof, party in parties.items():
        member = party.members[0]
        print(f"{prof}: {member.health}/100 - {member.health_system.get_status().value}")
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("OREGON TRAIL HEALTH SYSTEM DEMONSTRATION")
    print("="*50)
    print()
    
    try:
        demo_basic_survival()
        demo_starvation()
        demo_weather_exposure()
        demo_medicine_treatment()
        demo_profession_differences()
        
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
