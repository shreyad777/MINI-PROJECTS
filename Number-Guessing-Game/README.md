# 🎯 Number Guessing Game

A Python-based number guessing game with a console version and a Tkinter graphical interface. The project includes difficulty levels, scoring, replay functionality, game statistics, and permanent statistics storage using JSON.

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

Statistics are stored permanently using a JSON file.

This means the statistics remain available even after the application is closed.

💾 Data Storage

The project uses:

game_data.json

to store:

Number of games played
Number of games won
Number of games lost
Best score

The file is excluded from Git using .gitignore so personal game statistics are not uploaded to GitHub.

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
Select Easy, Medium, or Hard.
Click Start Game.
Enter your guess.
Click GUESS.
Follow the high/low hints.
Try to find the number within 10 attempts.
Your score is displayed when you win.
Game statistics are updated automatically.
Close and reopen the application to see that your statistics are preserved.
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
Improved GUI themes
Difficulty-based scoring
SQLite database for detailed game history
Player profiles
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)
