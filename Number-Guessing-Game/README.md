# 🎯 Number Guessing Game

A Python-based number guessing game with a console version and a Tkinter graphical interface. The project includes difficulty levels, scoring, player personalization, game statistics, permanent JSON storage, and game history.

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
- Permanent statistics storage
- Complete game history
- History viewer
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

For a lost game, the score is recorded as:

0
📊 Game Statistics

The GUI tracks:

Games Played
Games Won
Games Lost
Best Score

Statistics remain available after restarting the application.

📜 Game History

Every completed game is stored in the game history.

Each record contains:

Player name
Difficulty level
Game result
Number of attempts
Score

The History button opens a separate window where previous games can be viewed.

Example:

Game 1
Player     : Shreya
Difficulty : Medium
Result     : Won
Attempts   : 3
Score      : 8

The newest game is displayed first.

👤 Player Personalization

The player enters their name before starting a game.

Example:

Welcome, Shreya!
Guess a number between 1 and 100.

A player name is required before starting a game.

💾 Data Storage

Game information is stored using:

game_data.json

The file contains statistics and game history.

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
Click History to view previous games.
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
Player profiles
SQLite database
Online leaderboard
Advanced statistics
Improved GUI themes
Export game history
Delete history option
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)