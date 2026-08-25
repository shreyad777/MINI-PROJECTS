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
- Game history

## 2. Player Name

Before starting a game, the player enters their name.

The program reads the name using:

```python
player_name = name_entry.get().strip()

If no name is entered, the program displays a warning.

3. Difficulty Levels

The player can select:

Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10

The selected difficulty determines the range of the random number.

4. Random Number Generation

The secret number is generated using Python's random module:

secret_number = random.randint(minimum, maximum)
5. Guessing Process

The player enters a number into the GUI.

The program compares the guess with the secret number.

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

The player wins and the score is calculated.

6. Attempts

Each valid guess increases the attempts counter:

attempts += 1

The maximum number of attempts is:

max_attempts = 10
7. Score Calculation

The score is calculated as:

score = max_attempts - attempts + 1

For example:

Maximum attempts = 10
Attempts used    = 3

Score = 10 - 3 + 1
Score = 8

A lost game receives a score of 0.

8. Game Statistics

The application tracks:

games_played
games_won
games_lost
best_score

These values are displayed in the main GUI.

9. Game History

Version 7 introduces individual game history.

Each completed game is stored as a dictionary:

game_record = {
    "player": player_name,
    "difficulty": difficulty,
    "result": result,
    "attempts": attempts,
    "score": final_score
}

The record is added to:

game_history
10. Example Game History

A history record may look like:

{
    "player": "Shreya",
    "difficulty": "Medium",
    "result": "Won",
    "attempts": 3,
    "score": 8
}
11. Saving History

The statistics and history are saved using JSON:

with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)

The data is stored in:

game_data.json
12. Loading History

When the program starts, it reads the JSON file:

with open(DATA_FILE, "r") as file:
    data = json.load(file)

The previous statistics and game history are restored.

Therefore, the information remains available after restarting the application.

13. History Window

The History button opens a separate Tkinter window.

The window displays:

Player name
Difficulty
Result
Attempts
Score

The newest game is displayed first.

A scrollbar is provided when many games are stored.

14. GUI Components

The application contains:

Application title
Player name input
Difficulty selector
Start Game button
Guess input
Guess button
Result display
Attempts counter
Score display
Statistics display
New Game button
History button
History window
15. Program Flow
START
  |
  v
Load Statistics and History
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
  |       |
  |       v
  |   Calculate Score
  |       |
  |       v
  |   Update Statistics
  |       |
  |       v
  |   Add History
  |
  +---- Maximum Attempts
          |
          v
       Record Loss
          |
          v
       Add History
          |
          v
       Save JSON
          |
          v
         END
16. Error Handling

The program handles:

Empty player names
Invalid numeric input
Numbers outside the selected range
Invalid JSON files
File access errors
17. Data Security

The file:

game_data.json

is included in .gitignore.

This prevents personal game statistics and history from being uploaded to GitHub.

18. Technologies
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
19. Future Improvements

Possible future features include:

Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Player profiles
SQLite database
Online leaderboard
Advanced statistics
Export history
Delete history option
Improved GUI themes