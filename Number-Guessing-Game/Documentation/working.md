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

## 30. Game Timer

Version 11 introduces a real-time game timer.

The timer measures how long the player takes to complete a game.

---

## 31. Timer Variables

The application uses:

```python
game_active = False
timer_seconds = 0
timer_job = None
game_active

Determines whether a game is currently running.

timer_seconds

Stores the number of seconds elapsed.

timer_job

Stores the Tkinter scheduled timer task.

32. Timer Formatting

The timer is displayed using the format_time() function:

def format_time(seconds):

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f"{minutes:02d}:{remaining_seconds:02d}"

For example:

0 seconds   → 00:00
5 seconds   → 00:05
60 seconds  → 01:00
125 seconds → 02:05
33. Starting the Timer

When a new game begins:

start_timer()

The timer is reset:

00:00

and the game becomes active.

34. Updating the Timer

Tkinter's after() method is used to execute the timer update every second:

timer_job = root.after(
    1000,
    update_timer
)

The value 1000 represents 1000 milliseconds, which equals one second.

The timer then increments:

timer_seconds += 1
35. Stopping the Timer

When the player wins or loses:

stop_timer()

is called.

This sets:

game_active = False

and cancels the scheduled timer update.

36. Timer in Game History

Version 11 stores the completion time with every game:

game_record = {
    "player": player_name,
    "difficulty": difficulty,
    "result": result,
    "attempts": attempts,
    "score": final_score,
    "time": format_time(timer_seconds)
}

This makes game history more informative.

37. Complete Timer Flow
START GAME
     |
     v
Reset Timer
     |
     v
00:00
     |
     v
Start Timer
     |
     v
Update Every Second
     |
     +------ Wrong Guess ------+
     |                         |
     |                         v
     |                    Continue
     |
     +------ Correct ----------+
     |                         |
     |                         v
     |                    Stop Timer
     |
     +------ 10 Attempts ------+
                               |
                               v
                          Stop Timer
                               |
                               v
                         Save Time
                               |
                               v
                         Game History
38. Version 11 Improvements

Version 11 adds:

⏱️ Real-time timer
Automatic timer start
Automatic timer stop
Timer reset
Elapsed-time formatting
Timer in game history
Improved gameplay tracking

# Version 11 — Real-Time Game Timer

## 30. Game Timer

Version 11 adds a real-time timer to the Number Guessing Game.

The timer measures the amount of time taken by the player to complete a game.

---

## 31. Timer Variables

The application uses three timer variables:

```python
game_active = False
timer_seconds = 0
timer_job = None
game_active

Determines whether a game is currently running.

timer_seconds

Stores the number of seconds elapsed.

timer_job

Stores the Tkinter scheduled callback.

32. Timer Formatting

The timer is converted into a MM:SS format using:

def format_time(seconds):

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f"{minutes:02d}:{remaining_seconds:02d}"

Examples:

0 seconds    → 00:00
5 seconds    → 00:05
60 seconds   → 01:00
125 seconds  → 02:05
33. Starting the Timer

When a new game starts, the timer is reset:

timer_seconds = 0
game_active = True

The display is reset to:

00:00

The timer then schedules an update every 1000 milliseconds.

34. Updating the Timer

Tkinter's after() method is used:

timer_job = root.after(
    1000,
    update_timer
)

Every second:

timer_seconds += 1

The updated time is displayed to the user.

35. Stopping the Timer

When the player wins or loses:

stop_timer()

is called.

The timer is marked inactive:

game_active = False

The scheduled Tkinter callback is also cancelled.

36. Timer and Game Results

When a player wins, the completion time is displayed:

Attempts: 3
Score: 8
Time: 00:14

When the player loses after reaching the maximum attempts, the timer is also stopped and displayed.

37. Saving Time in Game History

Each completed game now stores its time:

game_record = {
    "player": player_name,
    "difficulty": difficulty,
    "result": result,
    "attempts": attempts,
    "score": final_score,
    "time": format_time(timer_seconds)
}

This allows the player to review how quickly previous games were completed.

38. Timer Workflow
START GAME
     |
     v
Reset Timer
     |
     v
00:00
     |
     v
Start Timer
     |
     v
Update Every Second
     |
     +------------------+
     |                  |
     v                  v
Wrong Guess        Correct Guess
     |                  |
     v                  v
Continue Timer      Stop Timer
                        |
                        v
                   Save Time
                        |
                        v
                  Game History
39. Version 11 Improvements

Version 11 adds:

⏱️ Real-time timer
Automatic timer start
Automatic timer stop
Timer reset
MM:SS formatting
Time saved in game history
Time shown in win/loss messages
Improved gameplay tracking

# Version 12 — Leaderboard System

## 40. Leaderboard

Version 12 introduces a leaderboard system that ranks the best winning performances.

The leaderboard stores the player's:

- Name
- Score
- Completion time
- Difficulty level

---

## 41. Leaderboard Data Structure

Each leaderboard entry is stored as a Python dictionary:

```python
entry = {
    "player": player_name,
    "score": final_score,
    "time": format_time(timer_seconds),
    "time_seconds": timer_seconds,
    "difficulty": difficulty_var.get()
}

Multiple entries are stored inside the leaderboard list.

42. Adding a Score

When the player wins a game, the score is sent to:

add_to_leaderboard(score)

The function creates a leaderboard entry and adds it to the leaderboard list.

43. Ranking Algorithm

The leaderboard is sorted using:

leaderboard = sorted(
    leaderboard,
    key=lambda entry: (
        -entry["score"],
        entry["time_seconds"]
    )
)

The sorting rules are:

1. Higher score → Higher position
2. Same score → Faster time wins

For example:

Player A → Score: 10 → Time: 00:20
Player B → Score: 10 → Time: 00:15

Player B ranks higher because both have the same score but Player B completed the game faster.

44. Top 10 Limitation

The leaderboard stores only the top 10 performances:

leaderboard = leaderboard[:10]

This keeps the leaderboard compact and focused on the best players.

45. Persistent Leaderboard

Leaderboard data is stored in the existing:

game_data.json

The JSON structure contains:

{
    "games_played": 5,
    "games_won": 3,
    "games_lost": 2,
    "best_score": 10,
    "game_history": [],
    "leaderboard": []
}

Therefore, leaderboard information remains available after closing and reopening the application.

46. Leaderboard Interface

The leaderboard is displayed in a separate Tkinter window.

The interface contains:

🏆 LEADERBOARD

Rank | Player | Score | Time | Difficulty

The top three positions are visually represented using:

🥇 First
🥈 Second
🥉 Third
47. Leaderboard Workflow
Player Starts Game
        |
        v
Player Makes Guesses
        |
        v
Player Wins
        |
        v
Calculate Score
        |
        v
Stop Timer
        |
        v
Create Leaderboard Entry
        |
        v
Sort Leaderboard
        |
        v
Keep Top 10
        |
        v
Save to JSON
        |
        v
Display Leaderboard
48. Reset Integration

The leaderboard is integrated with the Reset Data feature.

When the player confirms a reset:

leaderboard = []

All leaderboard records are removed.

49. Version 12 Improvements

Version 12 adds:

🏆 Leaderboard system
🥇 Automatic ranking
📊 Score-based ranking
⏱️ Time-based tie breaking
👤 Player tracking
🎯 Difficulty tracking
💾 Persistent leaderboard
🔝 Top 10 limitation
🌙 Dark Mode compatibility
🗑️ Leaderboard reset functionality

# Version 13 — Achievement & Badge System

## 50. Achievement System

Version 13 introduces an achievement system that rewards players for completing specific challenges.

The system makes the game more engaging by adding progression and rewards.

---

## 51. Achievement List

The application currently contains six achievements:

| Achievement | Requirement |
|---|---|
| First Victory | Win at least one game |
| Winning Streak | Win 3 consecutive games |
| Speed Demon | Win in under 15 seconds |
| Perfect Guesser | Win in one attempt |
| Score Master | Achieve a score of 10 or higher |
| Leaderboard Champion | Reach first position |

---

## 52. Achievement Data Structure

Achievements are stored using a Python dictionary:

```python
achievements = {
    "First Victory": False,
    "Winning Streak": False,
    "Speed Demon": False,
    "Perfect Guesser": False,
    "Score Master": False,
    "Leaderboard Champion": False
}

The value indicates whether the achievement has been unlocked.

False → Locked
True  → Unlocked
53. Unlocking Achievements

The function:

unlock_achievement(name)

checks whether an achievement has already been unlocked.

If it has not been unlocked, its value changes to:

True

The updated data is then saved to the JSON file.

54. First Victory

The First Victory achievement is unlocked when:

games_won >= 1

This means the player receives the badge after winning their first game.

55. Winning Streak

The application maintains:

winning_streak

After every successful game:

winning_streak += 1

When the player loses:

winning_streak = 0

The achievement is unlocked when:

winning_streak >= 3
56. Speed Demon

The Speed Demon achievement rewards fast gameplay.

The condition is:

timer_seconds < 15

If the player wins within 15 seconds, the achievement is unlocked.

57. Perfect Guesser

The Perfect Guesser achievement is unlocked when the player finds the number on their first attempt.

The condition is:

attempts == 1
58. Score Master

The Score Master achievement is based on the player's score.

The condition is:

final_score >= 10

This rewards players who achieve a high score.

59. Leaderboard Champion

The Leaderboard Champion achievement checks the player's position after the leaderboard is updated.

The player must occupy the first position.

The leaderboard is sorted by:

Highest Score
      ↓
Fastest Time

The player at position #1 receives the achievement.

60. Achievement Notification

When a new achievement is unlocked, the game displays:

🏅 NEW ACHIEVEMENTS!

🏆 First Victory

This gives immediate feedback to the player.

61. Achievement Interface

Players can access achievements through:

🏅 ACHIEVEMENTS

The interface displays:

🏆 First Victory
Win your first game.
✅ UNLOCKED

or:

🔒 Winning Streak
Win 3 games consecutively.
🔒 LOCKED
62. Achievement Persistence

Achievement information is stored in:

game_data.json

Example:

{
    "achievements": {
        "First Victory": true,
        "Winning Streak": false,
        "Speed Demon": false,
        "Perfect Guesser": false,
        "Score Master": false,
        "Leaderboard Champion": false
    }
}

The data is loaded when the application starts.

Therefore, unlocked achievements remain available after restarting the program.

63. Reset Integration

The Reset Data function also resets achievements.

When reset is confirmed:

for achievement in achievements:
    achievements[achievement] = False

This returns all achievements to the locked state.

64. Achievement Workflow
Player Completes Game
        |
        v
Check Game Result
        |
        v
Calculate Score + Time
        |
        v
Check Achievement Conditions
        |
        +----------------------+
        |                      |
        v                      v
Condition Met             Not Met
        |                      |
        v                      v
Unlock Badge              Remains Locked
        |
        v
Save to JSON
        |
        v
Show Notification

65. Version 13 Improvements

Version 13 adds:

🏅 Achievement system
🏆 First Victory badge
🔥 Winning Streak badge
⚡ Speed Demon badge
🎯 Perfect Guesser badge
💯 Score Master badge
🥇 Leaderboard Champion badge
🔓 Automatic unlocking
💾 Persistent achievement progress
🔔 Achievement notifications
🌙 Dark Mode compatibility
🗑️ Achievement reset functionality

# Version 14 — Sound Effects & Game Feedback

## 66. Sound System

Version 14 introduces audio feedback into the game.

The system uses Python's built-in `winsound` module.

```python
import winsound

No external sound files are required.

67. Sound Function

The central sound function is:

play_sound(sound_type)

It receives the type of game event and plays the corresponding sound.

Example:

play_sound("win")
68. Sound Types

The application supports the following sound types:

correct
high
low
win
lose
achievement

Each type represents a different game event.

69. Low Guess Feedback

When the player's guess is lower than the secret number:

play_sound("low")

A low-pitch beep is played.

The player also receives:

⬇️ Too low! Try again.
70. High Guess Feedback

When the player's guess is higher than the secret number:

play_sound("high")

A higher-pitch beep is played.

The interface displays:

⬆️ Too high! Try again.
71. Victory Sound

When the player correctly guesses the number:

play_sound("win")

Multiple ascending tones are played to create a victory melody.

The player then receives the victory message.

72. Game Over Sound

If the player reaches the maximum number of attempts:

play_sound("lose")

A descending sound pattern indicates that the game has ended.

73. Achievement Sound

When a new achievement is unlocked:

play_sound("achievement")

The game plays a special multi-tone notification.

This provides immediate audio feedback when the player earns a badge.

74. Sound Toggle

Players can enable or disable audio using:

🔊 SOUND ON

or:

🔇 SOUND OFF

The toggle is controlled by:

sound_enabled
75. Sound Preference

The sound setting is saved in game_data.json.

Example:

{
    "sound_enabled": true
}

If the user disables sound:

{
    "sound_enabled": false
}

The setting is loaded when the application starts.

76. Sound Safety Check

Before playing a sound, the application checks:

if not sound_enabled:
    return

Therefore, no sound is played when the user has disabled audio.

77. V14 Workflow
Player Performs Action
          |
          v
Game Detects Event
          |
          v
play_sound()
          |
          v
sound_enabled?
      /       \
    YES        NO
     |          |
     v          v
 Play Sound   Continue
     |
     v
Visual Feedback
78. V14 Improvements

Version 14 adds:

🔊 Audio feedback
⬆️ High-guess sound
⬇️ Low-guess sound
🎉 Victory sound
❌ Game-over sound
🏅 Achievement sound
🔇 Sound toggle
💾 Persistent sound preference
🖥️ Built-in Windows audio support