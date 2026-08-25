# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python application where the computer generates a random number and the player attempts to guess it.

The project contains:

- Console version
- Tkinter GUI version
- Difficulty levels
- Score calculation
- Game statistics
- Permanent JSON storage
- Player personalization

## 2. Player Name

Before starting a game, the player enters their name.

The program reads the name using:

```python
player_name = name_entry.get().strip()
If no name is entered, the application displays a warning:

Name Required

Please enter your name before starting the game.
3. Random Number Generation

The random module generates the secret number:

secret_number = random.randint(minimum, maximum)

The range depends on the selected difficulty.

4. Difficulty Levels
Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10

The set_difficulty() function determines the selected range.

5. Attempts

The attempts counter starts at zero:

attempts = 0

Every valid guess increases the counter:

attempts += 1

The maximum number of attempts is:

max_attempts = 10
6. Guess Comparison

The player's guess is compared with the secret number.

Too Low
guess < secret_number

Output:

Too low! Try again.
Too High
guess > secret_number

Output:

Too high! Try again.
Correct
guess == secret_number

The player wins and receives a score.

7. Score System

The score is calculated using:

score = max_attempts - attempts + 1

For example:

10 - 3 + 1 = 8

Therefore, winning in 3 attempts gives a score of 8.

8. Game Statistics

The application tracks:

games_played
games_won
games_lost
best_score

These values are displayed in the GUI.

9. JSON Data Storage

The game uses JSON for permanent statistics storage.

The data file is:

game_data.json

Example:

{
    "games_played": 5,
    "games_won": 4,
    "games_lost": 1,
    "best_score": 9
}
10. Loading Statistics

When the application starts, it checks whether the JSON file exists.

The load_statistics() function reads the saved information:

with open(DATA_FILE, "r") as file:
    data = json.load(file)

The stored values are loaded into the program.

11. Saving Statistics

After a game is completed, the save_statistics() function stores the updated information:

with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)

This allows statistics to remain available after the program is closed.

12. Personalized Messages

The player's name is used in game messages.

Example:

Welcome, Shreya!
Guess a number between 1 and 100.

After winning:

Congratulations, Shreya!

This provides a more personalized user experience.

13. GUI Components

The Tkinter interface contains:

Application title
Player name field
Difficulty selector
Start Game button
Guess input field
Guess button
Result display
Attempts counter
Score display
Statistics display
New Game button
14. Program Flow
START
  |
  v
Load Saved Statistics
  |
  v
Enter Player Name
  |
  +---- Empty ------> Show Warning
  |
  v
Select Difficulty
  |
  v
Start Game
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
15. Error Handling

The program handles:

Empty player name
Invalid numeric input
Numbers outside the selected range
Invalid JSON data
File access errors

This prevents common input and file-related errors from crashing the application.

16. Git Security

The game_data.json file is included in .gitignore.

Therefore, personal game statistics are not uploaded to GitHub.

17. Technologies
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
18. Future Improvements
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Player profiles
SQLite database
Online leaderboard
Advanced statistics
Improved GUI themes