# 🎯 Number Guessing Game

A Python-based number guessing game with a console version and a Tkinter graphical interface. The project includes difficulty levels, scoring, replay functionality, game statistics, permanent JSON storage, and personalized player names.

## ✨ Features

### Console Version

- Random number generation
- User input
- Too-high and too-low hints
- Attempts counter
- Input validation
- Easy, Medium, and Hard difficulty levels
- Score system
- Replay option
- Maximum attempt limit

### GUI Version

- Tkinter graphical interface
- Player name input
- Personalized welcome messages
- Difficulty selection
- Guess input
- High/low hints
- Score display
- Attempts display
- Games played counter
- Games won counter
- Games lost counter
- Best score tracking
- Permanent statistics storage using JSON
- New Game button
- Error and information popups

## 🎮 Difficulty Levels

| Difficulty | Number Range | Attempts |
|---|---:|---:|
| Easy | 1–50 | 10 |
| Medium | 1–100 | 10 |
| Hard | 1–200 | 10 |

## 🏆 Scoring System

The score depends on the number of attempts used.

```text
Score = Maximum Attempts - Attempts Used + 1
Using fewer attempts results in a higher score.

📊 Game Statistics

The GUI tracks:

Games Played
Games Won
Games Lost
Best Score

Statistics are saved using a JSON file and remain available when the application is reopened.

👤 Player Personalization

The player enters their name before starting a game.

The application then displays personalized messages such as:

Welcome, Shreya!
Guess a number between 1 and 100.

A player name is required before starting the game.

💾 Data Storage

Game statistics are stored in:

game_data.json

The stored information includes:

{
    "games_played": 0,
    "games_won": 0,
    "games_lost": 0,
    "best_score": 0
}

The game_data.json file is included in .gitignore so personal game statistics are not uploaded to GitHub.

🛠️ Technologies
Python
Tkinter
JSON
Random module
Functions
Loops
Conditional statements
Exception handling
File handling
GUI programming
🚀 How to Run
Console Version
python number_guessing_game.py
GUI Version
python number_guessing_gui.py

No external Python packages are required.

🎮 How to Play
Run the GUI version.
Enter your player name.
Select Easy, Medium, or Hard.
Click Start Game.
Enter your guess.
Click GUESS.
Follow the high/low hints.
Try to find the number within 10 attempts.
Check your score and statistics.
Click New Game to play again.
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
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Advanced statistics
Player profiles
SQLite database
Online leaderboard
Difficulty-based scoring
Improved GUI themes
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)