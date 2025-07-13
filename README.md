# Oregon Trail Fan Build

A modern, Python-based fan remake of the classic *Oregon Trail* game with a humorous and accessible twist. This solo project serves both as a learning exercise and a foundation for building more advanced educational games — especially those designed with accessibility in mind.

## 🎯 Project Goals

- Recreate and expand on the mechanics of the original Oregon Trail game
- Introduce dynamic features like professions, wagon types, health management, and inventory weight
- Use event-based logic for game progression
- Design with accessibility and educational value in mind

## 🚀 Features So Far

- ✅ Dynamic wagon system with types (Basic, Standard, Deluxe) loaded from `wagons.json`
- ✅ Professions with gameplay advantages/disadvantages (Banker, Farmer, Doctor, Carpenter, Solo Traveler)
- ✅ Inventory system with item weight, capacity limits, and food spoilage
- ✅ Spoilage logic influenced by weather and calendar month (rain, summer heat)
- ✅ Dynamic item and profession loading from JSON for modular expansion

## 🔨 In Progress

- ⏳ Event system (randomized events like river crossings, injuries, supply theft)
- ⏳ Health system influenced by food, rest, and environment
- ⏳ Game UI improvements (Tkinter polish or possible transition to web or Pygame)

## 🛠️ Tech Stack

- **Language:** Python 3
- **UI:** Tkinter (initially)
- **Data Storage:** JSON files for wagons, professions, and items
- **Planned Tools:** Event manager, possibly custom AI-like decision trees for event consequences

## 💡 Planned Features

- Procedural travel events (weather, attacks, repairs)
- Companion mechanics (AI-controlled family members)
- Map navigation or day-counter for progress tracking
- Accessibility-focused options (colorblind-safe UI, input pacing for neurodivergent players)
- Possible classroom mode or simplified version for children

## 🧠 Inspiration & Purpose

This project is part of a broader goal to explore how AI and game development can be used to create engaging, accessible experiences — particularly for children with autism and learning differences.

It also serves as a stepping stone toward developing professionally polished games for educational nonprofits and real-world classroom deployment.

## ▶️ How to Run the Game

```bash
python main.py
```

Ensure you have Python 3 installed. No external libraries are required at this stage.

## 📁 Project Structure

```
.
├── data/
│   ├── wagons.json
│   ├── professions.json
│   └── items.json
├── main.py
├── game/
│   ├── inventory.py
│   ├── wagon.py
│   ├── person.py
│   ├── events.py
│   └── ...
├── README.md
└── buildguide.md  ← [coming soon]
```

## 🤝 Contributions

While this is currently a solo learning project, contributions and suggestions are welcome! If you’re passionate about educational games or inclusive design, feel free to fork and collaborate.

## 📜 License

This is a fan-made project intended for educational purposes. No commercial use is intended.
