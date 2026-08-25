import tkinter as tk
from tkinter import messagebox
import random
import json
import os


# ---------------------------------
# Game Variables
# ---------------------------------

secret_number = 0
minimum = 1
maximum = 100

attempts = 0
max_attempts = 10
score = 0

DATA_FILE = "game_data.json"

player_name = ""

best_score = 0
games_played = 0
games_won = 0
games_lost = 0


# ---------------------------------
# Load Statistics
# ---------------------------------

def load_statistics():

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            return (
                data.get("games_played", 0),
                data.get("games_won", 0),
                data.get("games_lost", 0),
                data.get("best_score", 0)
            )

        except (json.JSONDecodeError, OSError):

            return 0, 0, 0, 0

    return 0, 0, 0, 0


# ---------------------------------
# Save Statistics
# ---------------------------------

def save_statistics():

    data = {
        "games_played": games_played,
        "games_won": games_won,
        "games_lost": games_lost,
        "best_score": best_score
    }

    try:

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:

        print("Unable to save game statistics.")


# Load saved statistics when program starts
games_played, games_won, games_lost, best_score = load_statistics()


# ---------------------------------
# Update Statistics Display
# ---------------------------------

def update_statistics():

    statistics_label.config(
        text=(
            f"Games Played: {games_played}\n"
            f"Games Won: {games_won}\n"
            f"Games Lost: {games_lost}\n"
            f"Best Score: {best_score}"
        )
    )


# ---------------------------------
# Start Player Game
# ---------------------------------

def start_player_game():

    global player_name

    player_name = name_entry.get().strip()

    if not player_name:

        messagebox.showwarning(
            "Name Required",
            "Please enter your name before starting the game."
        )

        return

    set_difficulty()


# ---------------------------------
# Difficulty Selection
# ---------------------------------

def set_difficulty():

    global minimum
    global maximum

    difficulty = difficulty_var.get()

    if difficulty == "Easy":

        minimum = 1
        maximum = 50

    elif difficulty == "Medium":

        minimum = 1
        maximum = 100

    elif difficulty == "Hard":

        minimum = 1
        maximum = 200

    start_new_game()


# ---------------------------------
# Start New Game
# ---------------------------------

def start_new_game():

    global secret_number
    global attempts
    global score

    secret_number = random.randint(
        minimum,
        maximum
    )

    attempts = 0
    score = 0

    guess_entry.delete(
        0,
        tk.END
    )

    result_label.config(
        text=(
            f"Welcome, {player_name}!\n"
            f"Guess a number between {minimum} and {maximum}."
        )
    )

    attempts_label.config(
        text=f"Attempts: 0 / {max_attempts}"
    )

    score_label.config(
        text="Score: 0"
    )


# ---------------------------------
# Check Guess
# ---------------------------------

def check_guess():

    global attempts
    global score
    global best_score
    global games_played
    global games_won
    global games_lost

    # Check whether player has entered a name
    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Please enter your name and start a game first."
        )

        return

    # Get user input
    try:

        guess = int(
            guess_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )

        return

    # Check range
    if guess < minimum or guess > maximum:

        messagebox.showwarning(
            "Out of Range",
            f"Enter a number between {minimum} and {maximum}."
        )

        return

    # Increase attempts
    attempts += 1

    attempts_label.config(
        text=f"Attempts: {attempts} / {max_attempts}"
    )

    # ---------------------------------
    # Guess is Too Low
    # ---------------------------------

    if guess < secret_number:

        result_label.config(
            text="⬇️ Too low! Try again."
        )

    # ---------------------------------
    # Guess is Too High
    # ---------------------------------

    elif guess > secret_number:

        result_label.config(
            text="⬆️ Too high! Try again."
        )

    # ---------------------------------
    # Correct Guess
    # ---------------------------------

    else:

        score = max_attempts - attempts + 1

        games_played += 1
        games_won += 1

        # Update best score
        if score > best_score:

            best_score = score

        # Save statistics
        save_statistics()

        # Update GUI
        score_label.config(
            text=f"Score: {score}"
        )

        update_statistics()

        result_label.config(
            text=(
                f"🎉 Congratulations, {player_name}!\n"
                f"The number was {secret_number}."
            )
        )

        messagebox.showinfo(
            "Congratulations!",
            f"Well done, {player_name}!\n\n"
            f"You guessed the number in {attempts} attempts.\n"
            f"Your score: {score}\n"
            f"Best score: {best_score}"
        )

        return

    # ---------------------------------
    # Maximum Attempts Reached
    # ---------------------------------

    if attempts >= max_attempts:

        games_played += 1
        games_lost += 1

        save_statistics()

        update_statistics()

        result_label.config(
            text=(
                f"❌ Game Over, {player_name}!\n"
                f"The number was {secret_number}."
            )
        )

        messagebox.showinfo(
            "Game Over",
            f"Sorry, {player_name}!\n\n"
            f"You used all {max_attempts} attempts.\n"
            f"The number was {secret_number}."
        )


# ---------------------------------
# Main Window
# ---------------------------------

root = tk.Tk()

root.title(
    "Number Guessing Game"
)

root.geometry(
    "600x750"
)

root.resizable(
    False,
    False
)


# ---------------------------------
# Title
# ---------------------------------

title_label = tk.Label(
    root,
    text="🎯 Number Guessing Game",
    font=("Arial", 25, "bold")
)

title_label.pack(
    pady=(25, 5)
)


# ---------------------------------
# Subtitle
# ---------------------------------

subtitle_label = tk.Label(
    root,
    text="Enter your name and start guessing!",
    font=("Arial", 12)
)

subtitle_label.pack(
    pady=(0, 15)
)


# ---------------------------------
# Player Name
# ---------------------------------

name_frame = tk.Frame(
    root
)

name_frame.pack(
    pady=10
)


tk.Label(
    name_frame,
    text="Player Name:",
    font=("Arial", 12, "bold")
).pack(
    side="left",
    padx=10
)


name_entry = tk.Entry(
    name_frame,
    font=("Arial", 12),
    width=20
)

name_entry.pack(
    side="left"
)


# ---------------------------------
# Difficulty
# ---------------------------------

difficulty_frame = tk.Frame(
    root
)

difficulty_frame.pack(
    pady=10
)


tk.Label(
    difficulty_frame,
    text="Difficulty:",
    font=("Arial", 12, "bold")
).pack(
    side="left",
    padx=10
)


difficulty_var = tk.StringVar(
    value="Medium"
)


difficulty_menu = tk.OptionMenu(
    difficulty_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard"
)

difficulty_menu.config(
    font=("Arial", 11)
)

difficulty_menu.pack(
    side="left"
)


# ---------------------------------
# Start Game Button
# ---------------------------------

tk.Button(
    difficulty_frame,
    text="Start Game",
    font=("Arial", 11, "bold"),
    command=start_player_game
).pack(
    side="left",
    padx=10
)


# ---------------------------------
# Instructions
# ---------------------------------

instruction_label = tk.Label(
    root,
    text="Enter your guess below:",
    font=("Arial", 12)
)

instruction_label.pack(
    pady=(20, 5)
)


# ---------------------------------
# Guess Entry
# ---------------------------------

guess_entry = tk.Entry(
    root,
    font=("Arial", 20),
    justify="center",
    width=15
)

guess_entry.pack(
    pady=10
)


# ---------------------------------
# Guess Button
# ---------------------------------

guess_button = tk.Button(
    root,
    text="GUESS",
    font=("Arial", 14, "bold"),
    width=15,
    height=2,
    command=check_guess
)

guess_button.pack(
    pady=10
)


# ---------------------------------
# Result
#