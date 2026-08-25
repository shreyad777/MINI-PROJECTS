# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python application where the computer generates a random number and the player attempts to guess it.

The project contains:

- Console version
- Tkinter GUI version
- Game statistics
- Permanent JSON data storage

## 2. Random Number Generation

The `random` module generates the secret number:

```python
secret_number = random.randint(minimum, maximum)

The range depends on the selected difficulty.

3. Difficulty Levels

The player can select one of three difficulty levels.

Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10
4. Attempts

The attempts counter starts at zero:

attempts = 0

Every valid guess increases the counter:

attempts += 1

The maximum number of attempts is:

max_attempts = 10
5. Guess Comparison

The player's guess is compared with the secret number.

Too Low
guess < secret_number

The program displays:

Too low! Try again.
Too High
guess > secret_number

The program displays:

Too high! Try again.
Correct
guess == secret_number

The player wins and receives a score.

6. Score System

The score is calculated using:

score = max_attempts - attempts + 1

For example:

10 - 3 + 1 = 8

If the player wins in 3 attempts, the score is 8.

7. Game Statistics

The application tracks:

games_played
games_won
games_lost
best_score

These values are displayed in the GUI.

8. JSON Data Storage

Version 5 introduces permanent data storage using JSON.

The data file is:

game_data.json

Example data:

{
    "games_played": 5,
    "games_won": 4,
    "games_lost": 1,
    "best_score": 9
}
9. Loading Statistics

When the program starts, it checks whether game_data.json exists.

The load_statistics() function reads the saved information:

with open(DATA_FILE, "r") as file:
    data = json.load(file)

The stored values are then loaded into the program.

10. Saving Statistics

After a game is completed, the save_statistics() function stores the updated statistics:

with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)

This allows the statistics to remain available after the application is closed.

11. Error Handling

The application handles invalid JSON data and file errors:

except (json.JSONDecodeError, OSError):
    return 0, 0, 0, 0

This prevents the application from crashing because of a damaged or unavailable data file.

12. GUI Version

The graphical interface is created using Tkinter.

The GUI contains:

Difficulty selector
Start Game button
Guess input
Guess button
Result display
Attempts counter
Score display
Statistics display
New Game button
Error messages
13. Program Flow
START
  |
  v
Load Saved Statistics
  |
  v
Select Difficulty
  |
  v
Generate Random Number
  |
  v
Enter Guess
  |
  v
Validate Input
  |
  +---- Invalid ------> Show Error
  |
  v
Increase Attempts
  |
  v
Compare Guess
  |
  +---- Too Low ------> Try Again
  |
  +---- Too High -----> Try Again
  |
  +---- Correct
          |
          v
      Calculate Score
          |
          v
      Update Statistics
          |
          v
      Save JSON Data
          |
          v
      Display Result
          |
          v
         END

14. Git Security

The game_data.json file is included in .gitignore.

This prevents personal game statistics from being uploaded to GitHub.

15. Technologies
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
16. Future Improvements
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Advanced statistics
Player profiles
SQLite database
Online leaderboard