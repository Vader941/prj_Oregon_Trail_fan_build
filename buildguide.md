# 🛠️ Oregon Trail Fan Build – Development Guide

This `buildguide.md` file documents the ongoing development process, goals, architecture, and working conventions for the Oregon Trail Fan Build project. It's designed to assist both GitHub Copilot and human collaborators by providing clear structure and intention behind the codebase.

---

## 🎯 Project Overview

A parody-style remake of the classic *Oregon Trail* built in Python. This project aims to:
- Rebuild core mechanics (travel, inventory, resource management)
- Add modular and scalable features (professions, events, wagons)
- Practice clean architecture and Python fundamentals
- Explore how game mechanics can support educational accessibility

---

## 📌 Core Features (with status)

- [x] Wagon selection system (types, capacities, cost, repair chances)
- [x] Profession system (advantages/disadvantages)
- [x] Inventory system with weight limits
- [x] Food spoilage logic (weather/month-based)
- [x] Health system (sickness, injuries, healing over time)
- [ ] Event system (modular event handlers for things like injury, theft, river crossing)
- [ ] Travel simulation (distance, date tracking, weather impacts)
- [ ] UI enhancements (better interaction flow, styling)
- [ ] Accessibility features (neurodivergent-friendly pacing, color choices, input simplicity)

---

## 🧱 File Structure

```
.
├── main.py                  # Launches the game
├── data/
│   ├── wagons.json          # Defines all wagon types
│   ├── professions.json     # Defines professions with health bonuses
│   └── items.json           # List of inventory items and weights
├── classes/
│   ├── wagon.py             # Wagon class and logic
│   ├── person.py            # Person class with profession and health logic
│   ├── inventory.py         # Handles inventory and weight
│   ├── health.py            # Individual health tracking and conditions
│   ├── party.py             # Party management and group health updates
│   ├── events.py            # In-progress event system
│   └── ...
```

---

## 🤖 Copilot Instructions

Copilot should follow these guidelines:
- Prioritize modular, class-based design (`Wagon`, `Person`, `Inventory`, `Event`)
- Use `try/except` for any user input or file reads
- Favor readability over brevity (assume this is for beginners)
- Functions should be short and single-purpose
- Keep any random logic (e.g. spoilage or events) inside their own helper classes or modules
- Avoid unnecessary third-party libraries

---

## 🧠 Architecture Planning

### Event System (Planned)
Each event will be a subclass of a base `Event` class. Event triggers may depend on:
- Current day
- Weather
- Random chance
- Party state (food, health, supplies)

Output should include:
- Event description
- Player choice (if applicable)
- Consequences (update to game state)

---

## 🔄 Development Cycle

1. Plan next feature or bug fix (log it in `devlog.md`)
2. Work within a branch or local environment
3. Test core logic in isolation
4. Refactor for clarity if needed
5. Commit with a meaningful message

---

## 📌 Notes for Future Me

- Weather, date, and event managers should eventually be central controllers
- Inventory needs to support different types of food for better spoilage realism
- Solo Traveler profession is a good test case for edge conditions (no companions, healing penalties)
- Consider converting all game state into a central class or dict for easier saving/loading

---

## ✅ Final Notes

This file is a living document and should be updated regularly as the project evolves. 
Keep things clean, modular, and well-documented for future collaboration or reuse.
