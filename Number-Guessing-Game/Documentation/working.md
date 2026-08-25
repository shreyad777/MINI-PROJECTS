# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python application where the computer generates a random number and the player attempts to guess it.

The project contains:

- Console version
- Tkinter GUI version

The application supports difficulty levels, scoring, attempt limits, input validation, and replay functionality.

## 2. Random Number Generation

The `random` module generates the secret number:

```python
number = random.randint(minimum, maximum)
The minimum and maximum values depend on the selected difficulty.

3. Difficulty Levels

The game provides three difficulty levels.

Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10

The choose_difficulty() function is responsible for selecting the appropriate range.

4. Attempts

The attempts counter begins at zero:

attempts = 0

Each valid guess increases the counter:

attempts += 1

The maximum number of attempts is:

max_attempts = 10
5. Guess Comparison

The player's guess is compared with the generated number.

Too Low
guess < number

Output:

Too low! Try again.
Too High
guess > number

Output:

Too high! Try again.
Correct
guess == number

The player wins and receives a score.

6. Score System

The score is calculated using:

score = max_attempts - attempts + 1

For example, if the player wins in 3 attempts:

10 - 3 + 1 = 8

The score is therefore 8.

7. Input Validation

The application handles invalid input using try-except.

try:
    guess = int(input())
except ValueError:
    print("Please enter a valid number.")

The program also checks whether the guess is within the selected range.

8. Replay System

After completing a game, the console version asks:

Do you want to play again? (y/n):

Entering y starts another game.

Entering n exits the application.

9. GUI Version

The GUI is built using Python's Tkinter library.

The GUI contains:

Difficulty selector
Start Game button
Guess input field
Guess button
Result display
Attempts counter
Score display
New Game button
Error and information popups
10. GUI Game Flow
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
      Display Result
          |
          v
         END
11. Error Handling

The GUI displays an error message when the user enters invalid input.

Example:

Invalid Input

Please enter a valid number.

It also displays a warning if the number is outside the selected range.

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
High-score tracking
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Advanced statistics
Improved GUI themes