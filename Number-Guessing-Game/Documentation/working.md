# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python application that generates a random number and challenges the player to identify it.

Version 8 introduces a professional dashboard interface while maintaining all previous functionality.

The application includes:

- Console gameplay
- Tkinter GUI
- Difficulty levels
- Player personalization
- Score calculation
- Statistics
- Game history
- JSON persistence
- Professional dashboard layout

---

## 2. Application Architecture

The application follows this general flow:

```text
User
 ↓
Player Setup
 ↓
Difficulty Selection
 ↓
Game Initialization
 ↓
Random Number Generation
 ↓
Player Guess
 ↓
Input Validation
 ↓
Guess Comparison
 ↓
Win / Loss
 ↓
Score Calculation
 ↓
Statistics Update
 ↓
Game History
 ↓
JSON Storage
3. Player Setup

The player enters their name.

The program obtains the name using:

player_name = name_entry.get().strip()

If the field is empty, a warning is displayed.

4. Difficulty Selection

The player selects one of three difficulty levels.

Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10

The selected difficulty determines the random number range.

5. Random Number Generation

The program generates the secret number using Python's random module:

secret_number = random.randint(minimum, maximum)

For example, in Medium mode:

Minimum = 1
Maximum = 100

The computer then generates a number between 1 and 100.

6. Guess Validation

The player's input is converted into an integer:

guess = int(guess_entry.get())

Invalid input is handled using exception handling.

Numbers outside the selected range are also rejected.

7. Guess Comparison

The player's guess is compared with the secret number.

Guess Too Low
guess < secret_number

The application displays:

⬇️ Too low! Try again.
Guess Too High
guess > secret_number

The application displays:

⬆️ Too high! Try again.
Correct Guess
guess == secret_number

The player wins and receives a score.

8. Attempt Tracking

Every valid guess increases the attempt counter:

attempts += 1

The maximum number of attempts is:

max_attempts = 10

The dashboard displays the current value as:

Attempts: 3 / 10
9. Score Calculation

The score is calculated using:

score = max_attempts - attempts + 1

For example:

Maximum attempts = 10
Attempts used    = 3

Score = 10 - 3 + 1
Score = 8

If the player loses, the recorded score is:

0
10. Statistics System

The application maintains four main statistics:

games_played
games_won
games_lost
best_score

After every completed game, the dashboard is updated.

11. Professional Dashboard

Version 8 reorganizes the GUI into several sections.

Header

Displays:

🎯 Number Guessing Game
Player Setup

Contains:

Player name
Difficulty selector
Start Game button
Statistics Dashboard

Displays:

Games Played
Games Won
Games Lost
Best Score
Current Game

Contains:

Game message
Guess input
Guess button
Attempts
Score
Action Section

Contains:

New Game
Game History
12. Game History

Every completed game is converted into a dictionary:

game_record = {
    "player": player_name,
    "difficulty": difficulty,
    "result": result,
    "attempts": attempts,
    "score": final_score
}

The dictionary is added to:

game_history
13. JSON Storage

The application stores its data in:

game_data.json

The data contains:

Games Played
Games Won
Games Lost
Best Score
Game History

Data is saved using:

with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)
14. Loading Previous Data

When the application starts, it checks whether the JSON file exists.

If the file exists, the saved data is loaded:

with open(DATA_FILE, "r") as file:
    data = json.load(file)

This provides persistent statistics and history.

15. History Window

Clicking:

📜 GAME HISTORY

opens a separate Tkinter window.

The window displays previous games.

Games are displayed in reverse order so the newest game appears first.

A scrollbar allows the user to navigate through a large number of records.

16. Error Handling

The application handles:

Empty player names
Invalid numbers
Out-of-range guesses
Invalid JSON data
File access problems

This improves reliability and prevents common user-input errors from crashing the application.

17. Complete Program Flow
START
  |
  v
Load JSON Data
  |
  v
Display Dashboard
  |
  v
Enter Player Name
  |
  +---- Empty
  |      |
  |      v
  |   Warning
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
  +---- Invalid
  |      |
  |      v
  |   Error Message
  |
  v
Increase Attempts
  |
  v
Compare Guess
  |
  +---- Too Low
  |       |
  |       └──> Try Again
  |
  +---- Too High
  |       |
  |       └──> Try Again
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
  +---- 10 Attempts
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
18. Technologies Used
Python

Used for the application logic.

Tkinter

Used to create the graphical interface.

JSON

Used for persistent game statistics and history.

Random

Used to generate the secret number.

File Handling

Used to save and load game data.

Exception Handling

Used to handle invalid input and file-related errors.

19. Security and Git

The following file contains personal game data:

game_data.json

It is included in .gitignore.

Therefore, personal game history and statistics are not intended to be committed to the Git repository.

20. Version 8 Improvements

Version 8 introduces:

Professional dashboard layout
Better UI organization
Statistics cards
Improved player setup section
Dedicated current-game section
Cleaner action buttons
Improved visual hierarchy
Better portfolio presentation
21. Future Enhancements

Future versions could include:

Global leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Player profiles
SQLite database
Online leaderboard
Advanced analytics
Export history
Delete history
Dark mode
Custom themes