# 🎯 Number Guessing Game

A Python-based number guessing game featuring a console version and a professional Tkinter graphical interface.

The application combines gameplay, difficulty levels, scoring, player personalization, statistics, permanent JSON storage, and game history in one project.

---

## ✨ Features

### 🎮 Game Features

- Random number generation
- Easy, Medium, and Hard difficulty levels
- High/low guessing hints
- Maximum attempt limit
- Automatic score calculation
- Input validation
- Win and loss detection

### 👤 Player Features

- Player name input
- Personalized game messages
- Player-specific game history

### 📊 Dashboard

The GUI provides a professional dashboard displaying:

- Games Played
- Games Won
- Games Lost
- Best Score
- Current Attempts
- Current Score

### 📜 Game History

Every completed game is stored and can be viewed through the **Game History** window.

Each record contains:

- Player name
- Difficulty
- Result
- Attempts
- Score

### 💾 Permanent Storage

Game statistics and history are stored using JSON.

Data remains available after closing and reopening the application.

---

## 🎚️ Difficulty Levels

| Difficulty | Number Range | Attempts |
|---|---:|---:|
| Easy | 1–50 | 10 |
| Medium | 1–100 | 10 |
| Hard | 1–200 | 10 |

---

## 🏆 Scoring

The score is calculated using:

```text
Score = Maximum Attempts - Attempts Used + 1

Example:

Maximum Attempts = 10
Attempts Used    = 3

Score = 10 - 3 + 1
Score = 8

A lost game receives a score of 0.

📊 Statistics

The application tracks:

Games Played
Games Won
Games Lost
Best Score

These statistics are automatically updated after every completed game.

📜 Game History

Example:

GAME 1

Player     : Shreya
Difficulty : Medium
Result     : Won
Attempts   : 3
Score      : 8

The newest completed game is displayed first.

💾 Data Storage

The application uses:

game_data.json

Example structure:

{
    "games_played": 2,
    "games_won": 1,
    "games_lost": 1,
    "best_score": 8,
    "game_history": [
        {
            "player": "Shreya",
            "difficulty": "Medium",
            "result": "Won",
            "attempts": 3,
            "score": 8
        }
    ]
}

The data file is included in .gitignore to prevent personal game statistics from being uploaded to GitHub.

🖥️ Professional Dashboard

Version 8 introduces a redesigned dashboard interface.

The interface is organized into:

Header
   ↓
Player Setup
   ↓
Statistics Dashboard
   ↓
Current Game
   ↓
Game Actions
   ↓
Footer

This makes the application easier to understand and use.

🛠️ Technologies
Python
Tkinter
JSON
Random module
File handling
Exception handling
Functions
Loops
Conditional statements
GUI programming
🚀 How to Run
Console Version
python number_guessing_game.py
GUI Version
python number_guessing_gui.py

No external Python packages are required.

🎮 How to Play
Run the GUI application.
Enter your player name.
Select a difficulty level.
Click START GAME.
Enter your guess.
Click GUESS.
Follow the hints.
Try to find the number within 10 attempts.
Check your score.
View your statistics.
Open GAME HISTORY to see previous games.
Use NEW GAME to start another round.
📂 Project Structure
Number-Guessing-Game/
│
├── number_guessing_game.py
├── number_guessing_gui.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── Documentation/
    └── working.md
🔮 Future Enhancements
🏆 Global leaderboard
⏱️ Timer-based scoring
🔊 Sound effects
🎮 Multiple rounds
👤 Player profiles
🗄️ SQLite database
🌐 Online leaderboard
📈 Advanced analytics
📤 Export game history
🗑️ Delete history
🌙 Dark mode
🎨 Custom themes
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)