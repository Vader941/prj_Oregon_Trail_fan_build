"""
main.py - Simulates spoilage under specific weather and month conditions.
"""

import os
import sys

# Add classes directory to the module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))

from person import Person
from wagon import Wagon
from inventory import Inventory
from item import ITEM_TYPES

def main():
    print("🧪 Spoilage Simulation Test: Default setup with weather/month factors")

    # Setup default player and wagon
    player = Person(name="Bob", age=22, profession="Farmer")
    wagon = Wagon(wagon_type="Basic")
    inventory = Inventory()

    # Add items
    print("\n📦 Adding 20 units of food...")
    inventory.add_item("Food", 20)

    # Show inventory before spoilage
    print("\n📋 Inventory before spoilage:")
    inventory.list_inventory()

    # Simulate spoilage for rain in August
    print("\n🌧️ Simulating spoilage in August during rain...")
    spoiled = inventory.simulate_spoilage(weather="rain", current_month=8)

    print(f"🔥 Total spoiled: {spoiled} units")

    # Show inventory after spoilage
    print("\n📋 Inventory after spoilage:")
    inventory.list_inventory()

    # Load wagon and show status
    item_weights = {k: v["weight"] for k, v in ITEM_TYPES.items()}
    total_weight = inventory.total_weight(item_weights)
    wagon.add_cargo(total_weight)

    print(f"\n⚖️ Total Inventory Weight: {total_weight} lbs")
    print("\n🚚 Wagon Status:")
    print(wagon)

if __name__ == "__main__":
    main()
