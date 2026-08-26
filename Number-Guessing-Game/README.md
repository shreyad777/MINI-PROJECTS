# 🎯 Number Guessing Game

A Python-based number guessing game featuring a professional Tkinter graphical interface, multiple difficulty levels, scoring, player personalization, statistics, persistent game history, and data management.

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

### 📊 Professional Dashboard

The GUI provides:

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

### 💾 Persistent Storage

Game statistics and history are stored using JSON and remain available after restarting the application.

### 🗑️ Reset Game Data

Version 9 introduces a **Reset Game Data** feature.

The user can permanently clear:

- Games Played
- Games Won
- Games Lost
- Best Score
- Game History

A confirmation dialog prevents accidental deletion.

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

The dashboard automatically updates after every completed game.

📜 Game History

Example:

GAME 1

Player     : Shreya
Difficulty : Medium
Result     : Won
Attempts   : 3
Score      : 8

The newest completed game appears first.

🗑️ Reset Game Data

The RESET DATA button allows the user to clear all stored game information.

Before deletion, the application displays a confirmation dialog:

Are you sure you want to delete all game statistics and history?

This action cannot be undone.

If the user selects No, the data remains unchanged.

If the user selects Yes, the statistics and history are cleared and the JSON file is updated.

## 🌙 Dark Mode

Version 10 introduces a built-in dark mode for a more modern user experience.

The interface can be switched between:

- 🌙 Dark Mode
- ☀️ Light Mode

Clicking the theme button immediately changes the application's appearance.

### Dark Mode Features

- Dark background
- Light text
- Dark input fields
- Dark buttons
- Improved readability
- Theme-aware game history window

The theme can be changed at any time without restarting the application.

Save:

Ctrl + S
STEP 2 — Update Documentation

Open:

notepad Documentation\working.md

Add this section near the end:

## 23. Dark Mode

Version 10 introduces a theme-switching system.

The application supports two themes:

```text
🌙 Dark Mode
☀️ Light Mode

The user can switch between themes using the theme button.

24. Theme System

The application defines separate colors for light and dark themes.

Light Theme
LIGHT_BG = "#f4f6f8"
LIGHT_FG = "#1f2937"
LIGHT_FRAME = "#ffffff"
LIGHT_BUTTON = "#2563eb"
Dark Theme
DARK_BG = "#111827"
DARK_FG = "#f9fafb"
DARK_FRAME = "#1f2937"
DARK_BUTTON = "#374151"
25. Theme Switching

The theme is controlled using:

dark_mode = False

When the user clicks the theme button:

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

The value changes between:

False → Light Mode
True  → Dark Mode
26. Applying the Theme

The apply_theme() function updates:

Main window
Frames
Labels
Buttons
Input fields
Statistics
Game area
Footer

This allows the entire interface to change without restarting the application.

27. Theme-Aware History

The Game History window also uses the currently selected theme.

If Dark Mode is active, the history window uses dark colors.

If Light Mode is active, it uses light colors.

28. Version 10 Improvements

Version 10 adds:

🌙 Dark Mode
☀️ Light Mode
Theme switching
Theme-aware buttons
Theme-aware input fields
Theme-aware labels
Theme-aware history window
Improved visual customization
29. Updated Feature Flow
START
  |
  v
Load Data
  |
  v
Display Dashboard
  |
  v
Select Theme
  |
  +---- Light Mode
  |
  +---- Dark Mode
  |
  v
Enter Player Name
  |
  v
Select Difficulty
  |
  v
Play Game
  |
  v
Statistics
  |
  v
History
  |
  v
Reset Data

💾 Data Storage

The application uses:

game_data.json

Example:

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

The game_data.json file is included in .gitignore so personal game data is not uploaded to GitHub.

🖥️ Dashboard Layout

The application is organized into:

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

The action section provides:

🔄 NEW GAME
📜 GAME HISTORY
🗑️ RESET DATA
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
Open GAME HISTORY to view previous games.
Use NEW GAME to start another round.
Use RESET DATA when you want to clear stored statistics and history.
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
🌙 Dark mode
🎨 Custom themes
🔐 User authentication
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)