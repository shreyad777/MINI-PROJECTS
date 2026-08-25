# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game is a Python console application where the computer generates a random number and the player attempts to guess it.

Version 2 introduces:

- Difficulty levels
- Maximum attempts
- Score calculation
- Replay functionality

## 2. Random Number Generation

The `random` module generates the secret number.

```python
number = random.randint(minimum, maximum)
The range depends on the selected difficulty.

3. Difficulty Levels

The player can select one of three difficulty levels.

Easy
Range: 1 - 50
Attempts: 10
Medium
Range: 1 - 100
Attempts: 10
Hard
Range: 1 - 200
Attempts: 10

The choose_difficulty() function returns the selected range.

4. Attempts

Each valid guess increases the attempts counter:

attempts += 1

The player has a maximum of 10 attempts.

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

The score is calculated based on the number of attempts used.

score = max_attempts - attempts + 1

For example, if the player wins in 3 attempts:

10 - 3 + 1 = 8

Therefore, the score is:

8
7. Input Validation

The program handles non-numeric input using exception handling.

try:
    guess = int(input())
except ValueError:
    print("Please enter a valid number.")

The program also checks whether the entered number is within the selected range.

8. Replay System

After each game, the player is asked:

Do you want to play again? (y/n):

If the player enters y, a new game starts.

If the player enters n, the program exits.

9. Program Flow
START
  |
  v
Choose Difficulty
  |
  v
Generate Random Number
  |
  v
Set Attempts = 0
  |
  v
Ask for Guess
  |
  v
Validate Input
  |
  +---- Invalid ------> Ask Again
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
      Play Again?
       /       \
      Yes       No
       |         |
       v         v
   New Game     END
10. Technologies
Python
Random module
Functions
Loops
Conditional statements
Exception handling
User input
11. Future Improvements
Tkinter graphical interface
High-score tracking
Leaderboard
Timer-based scoring
Sound effects
Multiple rounds
Game statistics
