# Number Guessing Game - Working Principle

## 1. Overview

The Number Guessing Game generates a random number and challenges the player to identify it.

The application includes:

- Console gameplay
- Tkinter GUI
- Difficulty levels
- Player personalization
- Score calculation
- Statistics
- Game history
- JSON persistence
- Professional dashboard
- Reset data functionality

---

## 2. Application Flow

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

The player enters their name:

player_name = name_entry.get().strip()

If the field is empty, the application displays a warning.

4. Difficulty Selection

The player chooses:

Difficulty	Range	Attempts
Easy	1–50	10
Medium	1–100	10
Hard	1–200	10
5. Random Number Generation

The secret number is generated using:

secret_number = random.randint(minimum, maximum)
6. Guess Validation

The application converts the input into an integer:

guess = int(guess_entry.get())

Invalid input is handled with exception handling.

Numbers outside the selected range are rejected.

7. Guess Comparison

The program compares:

Player Guess
     |
     v
Secret Number

Possible results:

Too Low
Too High
Correct
8. Attempt Tracking

Each valid guess increases:

attempts += 1

The maximum is:

max_attempts = 10
9. Score Calculation

The score is:

score = max_attempts - attempts + 1

Example:

10 maximum attempts
3 attempts used

Score = 8

A lost game receives:

Score = 0
10. Statistics

The application maintains:

games_played
games_won
games_lost
best_score

The dashboard updates automatically after a game ends.

11. Game History

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
12. JSON Persistence

The application saves data to:

game_data.json

Saving is performed using:

with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)

When the application starts, the data is loaded from the same file.

13. Professional Dashboard

Version 8 introduced a dashboard containing:

Header

Application title and description.

Player Setup
Player name
Difficulty
Start Game
Statistics
Games Played
Games Won
Games Lost
Best Score
Current Game
Game message
Guess input
Guess button
Attempts
Score
Actions
New Game
Game History
Reset Data
14. Reset Game Data

Version 9 introduces the reset_data() function.

The function resets:

games_played = 0
games_won = 0
games_lost = 0
best_score = 0
game_history = []

Before resetting, the program asks the user for confirmation:

confirmation = messagebox.askyesno(
    "Reset Game Data",
    "Are you sure you want to delete all game statistics and history?"
)

If the user selects No, nothing changes.

If the user selects Yes, all statistics and history are cleared.

15. Reset Process
Click RESET DATA
       |
       v
Confirmation Dialog
       |
   ┌───┴───┐
   |       |
  NO      YES
   |       |
   v       v
 Cancel   Clear Data
           |
           v
       Save JSON
           |
           v
      Update Dashboard
           |
           v
       Show Message
16. Data Safety

Resetting data is intentionally protected by a confirmation dialog.

This reduces accidental deletion.

The user must explicitly select Yes before the data is cleared.

17. Error Handling

The application handles:

Empty player names
Invalid numbers
Out-of-range guesses
Invalid JSON data
File access errors
Accidental reset attempts
18. Complete Program Flow
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
  v
Compare Guess
  |
  +---- Too Low ----> Try Again
  |
  +---- Too High ---> Try Again
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
19. Reset Data Flow
RESET DATA
    |
    v
Ask Confirmation
    |
    +---- NO ----> Keep Existing Data
    |
    +---- YES
           |
           v
      Clear Statistics
           |
           v
       Clear History
           |
           v
       Save JSON
           |
           v
    Update Dashboard
           |
           v
      Reset Complete
20. Technologies Used
Python
Tkinter
JSON
Random module
File handling
Exception handling
Functions
Loops
Conditional statements
GUI programming

21. Version 9 Improvements

Version 9 adds:

Reset Game Data button
Confirmation dialog
Complete statistics reset
Complete history reset
JSON data update after reset
Improved data management

22. Future Enhancements

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
Dark mode
Custom themes
User authentication

23. Dark Mode

Version 10 introduces a theme-switching system.

The application supports two themes:

```text
🌙 Dark Mode
☀️ Light Mode

The user can switch between themes using the theme button.

24. Theme System

The application defines separate colors for light and dark themes.

Light Theme
LIGHT_BG = "#f4f6f8"
LIGHT_FG = "#1f2937"
LIGHT_FRAME = "#ffffff"
LIGHT_BUTTON = "#2563eb"
Dark Theme
DARK_BG = "#111827"
DARK_FG = "#f9fafb"
DARK_FRAME = "#1f2937"
DARK_BUTTON = "#374151"
25. Theme Switching

The theme is controlled using:

dark_mode = False

When the user clicks the theme button:

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

The value changes between:

False → Light Mode
True  → Dark Mode
26. Applying the Theme

The apply_theme() function updates:

Main window
Frames
Labels
Buttons
Input fields
Statistics
Game area
Footer

This allows the entire interface to change without restarting the application.

27. Theme-Aware History

The Game History window also uses the currently selected theme.

If Dark Mode is active, the history window uses dark colors.

If Light Mode is active, it uses light colors.

28. Version 10 Improvements

Version 10 adds:

🌙 Dark Mode
☀️ Light Mode
Theme switching
Theme-aware buttons
Theme-aware input fields
Theme-aware labels
Theme-aware history window
Improved visual customization
29. Updated Feature Flow
START
  |
  v
Load Data
  |
  v
Display Dashboard
  |
  v
Select Theme
  |
  +---- Light Mode
  |
  +---- Dark Mode
  |
  v
Enter Player Name
  |
  v
Select Difficulty
  |
  v
Play Game
  |
  v
Statistics
  |
  v
History
  |
  v
Reset Data