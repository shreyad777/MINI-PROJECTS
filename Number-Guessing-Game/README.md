# 🎯 Number Guessing Game

A Python-based number guessing game with difficulty levels, scoring, replay functionality, and a graphical user interface built using Tkinter.

## ✨ Features

### Console Version

- 🎲 Random number generation
- 🔢 User input
- ⬆️ Too-high hints
- ⬇️ Too-low hints
- 🎯 Attempts counter
- ⚠️ Invalid input handling
- 🟢 Easy, Medium, and Hard difficulty levels
- 🏆 Score system
- 🔄 Replay option
- 🔒 Maximum attempt limit

### GUI Version

- 🖥️ Tkinter graphical interface
- 🎚️ Difficulty selection
- 🔢 Guess input
- ⬆️ High/low hints
- 🏆 Score display
- 🎯 Attempts display
- ⚠️ Input validation
- 🔄 New Game button
- 🎉 Win and Game Over messages

## 🎮 Difficulty Levels

| Difficulty | Number Range | Attempts |
|---|---:|---:|
| Easy | 1–50 | 10 |
| Medium | 1–100 | 10 |
| Hard | 1–200 | 10 |

## 🏆 Scoring System

The score depends on the number of attempts used.

The fewer attempts used, the higher the score.

```text
Score = Maximum Attempts - Attempts Used + 1
🛠️ Technologies
Python
Tkinter
Random module
Functions
Loops
Conditional statements
Exception handling
🚀 How to Run
Console Version
python number_guessing_game.py
GUI Version
python number_guessing_gui.py

Tkinter is included with most standard Python installations, so no external packages are required.

🎮 How to Play
Console Version
Run the Python program.
Select a difficulty level.
Enter your guess.
Use the hints to adjust your next guess.
Try to find the number within 10 attempts.
Your score is displayed when you win.
Choose whether to play again.
GUI Version
Run number_guessing_gui.py.
Select Easy, Medium, or Hard.
Click Start Game.
Enter your guess.
Click GUESS.
Follow the hints.
Try to guess the number before reaching the attempt limit.
📋 Example
==============================
      NUMBER GUESSING GAME
==============================

Select a difficulty level.

Choose Difficulty
1. Easy
2. Medium
3. Hard

Enter your choice: 1

I have selected a number between 1 and 50.
You have 10 attempts.

Attempt 1: 25
Too high! Try again.

Attempt 2: 12
Too low! Try again.

Attempt 3: 18

🎉 Congratulations!

You guessed the number in 3 attempts.
Your score: 8
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
High-score tracking
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Advanced game statistics
Improved GUI themes
Difficulty-based scoring
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)