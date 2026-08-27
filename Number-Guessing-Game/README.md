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


## Version 11 — Real-Time Game Timer ⏱️

Version 11 introduces a real-time timer that tracks how long the player takes to complete each game.

### Timer Features

- ⏱️ Real-time elapsed-time counter
- ▶️ Automatically starts when a game begins
- 🔄 Resets when a new game starts
- ⏹️ Stops when the player wins
- ⏹️ Stops when the player loses
- 📜 Saves the completion time in game history
- 🌙 Compatible with Dark Mode

### Timer Display

```text
Attempts       Score       Time
0 / 10           0        00:00

During gameplay:

00:01
00:02
00:03
...

The timer uses Tkinter's after() method to update the display every second.

Game History

Completed games now store the time taken:

GAME 1

Player     : Shreya
Difficulty : Medium
Result     : Won
Attempts   : 3
Score      : 8
Time       : 00:14
Version History
Version	Feature
V1	Basic Number Guessing Game
V2	Difficulty + Score
V3	Tkinter GUI
V4	Statistics + Best Score
V5	JSON Persistence
V6	Player Personalization
V7	Game History
V8	Professional Dashboard
V9	Reset / Clear Data
V10	Dark / Light Mode
V11	Real-Time Game Timer

# Version 12 — Leaderboard System 🏆

Version 12 introduces a persistent leaderboard that ranks players based on their game performance.

## 🏆 Leaderboard Features

- 🥇 Automatic player ranking
- 📊 Score-based ranking
- ⏱️ Time used as a secondary ranking factor
- 👤 Player name tracking
- 🎯 Difficulty tracking
- 💾 Persistent leaderboard data
- 🔝 Top 10 scores displayed
- 🔄 Automatically updated after every winning game
- 🌙 Compatible with Dark Mode

## Leaderboard Ranking

Players are ranked using:

1. Highest score
2. Fastest completion time when scores are equal

Example:

```text
🏆 LEADERBOARD

Rank   Player       Score    Time      Difficulty
──────────────────────────────────────────────────
🥇 1   Shreya        10      00:12     Easy
🥈 2   Rahul          9      00:18     Medium
🥉 3   Ananya         8      00:21     Medium
   4   Arjun          7      00:25     Hard

Only the top 10 winning results are stored.

Version History
Version	Feature
V1	Basic Number Guessing Game
V2	Difficulty + Score
V3	Tkinter GUI
V4	Statistics + Best Score
V5	JSON Persistence
V6	Player Personalization
V7	Game History
V8	Professional Dashboard
V9	Reset / Clear Data
V10	Dark / Light Mode
V11	Real-Time Game Timer
V12	Leaderboard System 🏆


# Version 13 — Achievement & Badge System 🏅

Version 13 introduces a gamification system that rewards players for reaching specific milestones and completing gameplay challenges.

## 🏅 Achievement Features

- 🏆 First Victory
- 🔥 Winning Streak
- ⚡ Speed Demon
- 🎯 Perfect Guesser
- 💯 Score Master
- 🥇 Leaderboard Champion
- 💾 Persistent achievement data
- 🔓 Automatic achievement unlocking
- 🌙 Dark Mode compatibility
- 🗑️ Reset achievements with Reset Data

## Available Achievements

| Achievement | Requirement |
|---|---|
| 🏆 First Victory | Win your first game |
| 🔥 Winning Streak | Win 3 games consecutively |
| ⚡ Speed Demon | Win a game in under 15 seconds |
| 🎯 Perfect Guesser | Find the number in one attempt |
| 💯 Score Master | Achieve a score of 10 or higher |
| 🥇 Leaderboard Champion | Reach #1 on the leaderboard |

## Achievement Display

The application now includes an:

```text
🏅 ACHIEVEMENTS

button.

The achievement window displays the player's progress:

🏅 YOUR ACHIEVEMENTS

🏆 First Victory          ✅ UNLOCKED
🔥 Winning Streak         🔒 LOCKED
⚡ Speed Demon            🔒 LOCKED
🎯 Perfect Guesser        🔒 LOCKED
💯 Score Master            🔒 LOCKED
🥇 Leaderboard Champion  🔒 LOCKED

When an achievement is unlocked, the player receives a notification.

Persistent Achievement Data

Achievement progress is stored in:

game_data.json

This means unlocked badges remain available after restarting the application.

Version History
Version	Feature
V1	Basic Number Guessing Game
V2	Difficulty + Score
V3	Tkinter GUI
V4	Statistics + Best Score
V5	JSON Persistence
V6	Player Personalization
V7	Game History
V8	Professional Dashboard
V9	Reset / Clear Data
V10	Dark / Light Mode
V11	Real-Time Game Timer
V12	Leaderboard System
V13	Achievement & Badge System 🏅

# Version 14 — Sound Effects & Game Feedback 🔊

Version 14 adds an interactive sound system to the Number Guessing Game.

## 🔊 Sound Features

- ⬇️ Low-pitch feedback for guesses below the target
- ⬆️ High-pitch feedback for guesses above the target
- 🎉 Victory sound when the number is guessed
- ❌ Game-over sound when attempts are exhausted
- 🏅 Achievement-unlocked sound
- 🔊 Sound ON/OFF control
- 💾 Sound preference is saved automatically

## Sound Control

The main dashboard contains:

```text
🔊 SOUND ON

Clicking the button changes it to:

🔇 SOUND OFF

When sound is disabled, gameplay continues normally without audio feedback.

Sound Mapping
Event	Audio Feedback
Guess too low	Low beep
Guess too high	High beep
Correct guess	Victory melody
Game over	Game-over melody
Achievement unlocked	Achievement melody
Enable sound	Confirmation beep
Technology

V14 uses Python's built-in:

winsound

This provides lightweight audio feedback without requiring external audio files.

Persistent Sound Preference

The sound setting is stored in:

game_data.json

Example:

{
    "sound_enabled": true
}

Therefore, the user's sound preference remains available after restarting the application.

V14 Architecture
Player Action
      |
      v
Game Event
      |
      v
play_sound()
      |
      v
Sound Enabled?
   /       \
 YES        NO
  |          |
  v          v
winsound    No Audio
  |
  v
User Feedback
Version History
Version	Feature
V11	Real-Time Game Timer
V12	Leaderboard System
V13	Achievement & Badge System
V14	Sound Effects & Game Feedback 🔊


👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)