import tkinter as tk
from tkinter import messagebox
import random


# -----------------------------
# Game Variables
# -----------------------------

secret_number = 0
minimum = 1
maximum = 100

attempts = 0
max_attempts = 10
score = 0

best_score = 0
games_played = 0
games_won = 0
games_lost = 0


# -----------------------------
# Difficulty Selection
# -----------------------------

def set_difficulty():

    global minimum, maximum

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


# -----------------------------
# Start New Game
# -----------------------------

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
        text=f"Guess a number between {minimum} and {maximum}."
    )

    attempts_label.config(
        text=f"Attempts: 0 / {max_attempts}"
    )

    score_label.config(
        text="Score: 0"
    )


# -----------------------------
# Update Statistics
# -----------------------------

def update_statistics():

    statistics_label.config(
        text=(
            f"Games Played: {games_played}\n"
            f"Games Won: {games_won}\n"
            f"Games Lost: {games_lost}\n"
            f"Best Score: {best_score}"
        )
    )


# -----------------------------
# Check Guess
# -----------------------------

def check_guess():

    global attempts
    global score
    global best_score
    global games_played
    global games_won
    global games_lost

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

    if guess < minimum or guess > maximum:

        messagebox.showwarning(
            "Out of Range",
            f"Enter a number between {minimum} and {maximum}."
        )

        return

    attempts += 1

    attempts_label.config(
        text=f"Attempts: {attempts} / {max_attempts}"
    )

    if guess < secret_number:

        result_label.config(
            text="⬇️ Too low! Try again."
        )

    elif guess > secret_number:

        result_label.config(
            text="⬆️ Too high! Try again."
        )

    else:

        score = max_attempts - attempts + 1

        games_played += 1
        games_won += 1

        if score > best_score:
            best_score = score

        score_label.config(
            text=f"Score: {score}"
        )

        update_statistics()

        result_label.config(
            text=f"🎉 Correct! The number was {secret_number}."
        )

        messagebox.showinfo(
            "Congratulations!",
            f"You guessed the number in {attempts} attempts!\n"
            f"Your score: {score}\n"
            f"Best score: {best_score}"
        )

        return

    if attempts >= max_attempts:

        games_played += 1
        games_lost += 1

        update_statistics()

        result_label.config(
            text=f"❌ Game Over! Number was {secret_number}."
        )

        messagebox.showinfo(
            "Game Over",
            f"You ran out of attempts.\n"
            f"The number was {secret_number}."
        )


# -----------------------------
# Main Window
# -----------------------------

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


# -----------------------------
# Title
# -----------------------------

title_label = tk.Label(
    root,
    text="🎯 Number Guessing Game",
    font=("Arial", 25, "bold")
)

title_label.pack(
    pady=(25, 5)
)


subtitle_label = tk.Label(
    root,
    text="Guess the hidden number!",
    font=("Arial", 12)
)

subtitle_label.pack(
    pady=(0, 15)
)


# -----------------------------
# Difficulty
# -----------------------------

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


tk.Button(
    difficulty_frame,
    text="Start Game",
    font=("Arial", 11, "bold"),
    command=set_difficulty
).pack(
    side="left",
    padx=10
)


# -----------------------------
# Instructions
# -----------------------------

instruction_label = tk.Label(
    root,
    text="Enter your guess below:",
    font=("Arial", 12)
)

instruction_label.pack(
    pady=(20, 5)
)


# -----------------------------
# Guess Entry
# -----------------------------

guess_entry = tk.Entry(
    root,
    font=("Arial", 20),
    justify="center",
    width=15
)

guess_entry.pack(
    pady=10
)


# -----------------------------
# Guess Button
# -----------------------------

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


# -----------------------------
# Result
# -----------------------------

result_label = tk.Label(
    root,
    text="Choose a difficulty and start the game.",
    font=("Arial", 13, "bold"),
    wraplength=500
)

result_label.pack(
    pady=15
)


# -----------------------------
# Attempts
# -----------------------------

attempts_label = tk.Label(
    root,
    text="Attempts: 0 / 10",
    font=("Arial", 12)
)

attempts_label.pack(
    pady=5
)


# -----------------------------
# Score
# -----------------------------

score_label = tk.Label(
    root,
    text="Score: 0",
    font=("Arial", 12, "bold")
)

score_label.pack(
    pady=5
)


# -----------------------------
# Statistics
# -----------------------------

statistics_label = tk.Label(
    root,
    text=(
        "Games Played: 0\n"
        "Games Won: 0\n"
        "Games Lost: 0\n"
        "Best Score: 0"
    ),
    font=("Arial", 12),
    justify="center"
)

statistics_label.pack(
    pady=15
)


# -----------------------------
# New Game Button
# -----------------------------

tk.Button(
    root,
    text="🔄 New Game",
    font=("Arial", 11, "bold"),
    command=start_new_game,
    width=15
).pack(
    pady=15
)


# -----------------------------
# Start Application
# -----------------------------

root.mainloop()