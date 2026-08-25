# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python application where the computer generates a random number and the player attempts to guess it.

The project contains both a console version and a graphical version built using Tkinter.

The application supports:

- Difficulty levels
- Score calculation
- Attempt limits
- Input validation
- Replay functionality
- Game statistics

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

The set_difficulty() function determines the selected range.

4. Attempts

The attempts counter begins at zero:

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

For example, if the player wins in 3 attempts:

10 - 3 + 1 = 8

Therefore, the score is 8.

7. Input Validation

The application uses exception handling to prevent invalid input from crashing the program.

try:
    guess = int(guess_entry.get())
except ValueError:
    messagebox.showerror(
        "Invalid Input",
        "Please enter a valid number."
    )

The program also checks whether the entered number is inside the selected range.

8. Game Statistics

Version 4 introduces game statistics.

The following variables track the player's performance:

best_score = 0
games_played = 0
games_won = 0
games_lost = 0
Games Played

Increases whenever a game is completed.

Games Won

Increases when the player correctly guesses the number.

Games Lost

Increases when the player reaches the maximum number of attempts.

Best Score

Stores the highest score achieved during the current program session.

The best score is updated using:

if score > best_score:
    best_score = score
9. Statistics Display

The GUI displays:

Games Played: 0
Games Won: 0
Games Lost: 0
Best Score: 0

The values are updated after each completed game.

10. GUI Version

The graphical interface is created using Python's Tkinter library.

The GUI contains:

Title
Difficulty selector
Start Game button
Guess input field
Guess button
Result display
Attempts counter
Score display
Statistics section
New Game button
11. GUI Game Flow
START
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
      Display Result
          |
          v
      Start New Game
12. Technologies
Python
Tkinter
Random module
Functions
Loops
Conditional statements
Exception handling
GUI programming
13. Future Improvements
Permanent high-score storage
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Advanced statistics
Improved GUI themes
SQLite database for game history
