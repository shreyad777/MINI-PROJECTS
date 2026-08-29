import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# =========================================================
# NUMBER GUESSING GAME - V19
# Professional Edition
# =========================================================

SAVE_FILE = "game_data.json"

# -----------------------------
# GAME SETTINGS
# -----------------------------

DIFFICULTIES = {
    "Easy": {
        "max_number": 50,
        "attempts": 15,
        "points": 100
    },
    "Medium": {
        "max_number": 100,
        "attempts": 10,
        "points": 200
    },
    "Hard": {
        "max_number": 500,
        "attempts": 7,
        "points": 300
    }
}

# -----------------------------
# GAME VARIABLES
# -----------------------------

secret_number = 0
attempts_used = 0
max_attempts = 10
score = 0
current_score = 0
streak = 0
games_played = 0
games_won = 0
best_score = 0
timer_seconds = 60
timer_running = False
dark_mode = True

difficulty = "Medium"


# =========================================================
# DATA MANAGEMENT
# =========================================================

def load_data():
    global best_score, streak, games_played, games_won

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)

                best_score = data.get("best_score", 0)
                streak = data.get("streak", 0)
                games_played = data.get("games_played", 0)
                games_won = data.get("games_won", 0)

        except (json.JSONDecodeError, OSError):
            pass


def save_data():
    data = {
        "best_score": best_score,
        "streak": streak,
        "games_played": games_played,
        "games_won": games_won
    }

    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        pass


# =========================================================
# START NEW GAME
# =========================================================

def new_game():
    global secret_number
    global attempts_used
    global max_attempts
    global current_score
    global timer_seconds
    global timer_running
    global games_played

    settings = DIFFICULTIES[difficulty]

    secret_number = random.randint(1, settings["max_number"])
    attempts_used = 0
    max_attempts = settings["attempts"]
    current_score = settings["points"]

    timer_seconds = 60
    timer_running = True

    games_played += 1

    range_label.config(
        text=f"Guess a number between 1 and {settings['max_number']}"
    )

    result_label.config(
        text="🤔 Make your first guess!",
        fg=get_text_color()
    )

    attempts_label.config(
        text=f"🎯 Attempts: 0/{max_attempts}"
    )

    score_label.config(
        text=f"🏆 Score: {current_score}"
    )

    timer_label.config(
        text=f"⏱️ Time: {timer_seconds}s"
    )

    guess_entry.delete(0, tk.END)
    guess_entry.config(state=tk.NORMAL)

    guess_button.config(state=tk.NORMAL)

    guess_entry.focus()

    update_statistics()
    save_data()

    countdown()


# =========================================================
# COUNTDOWN TIMER
# =========================================================

def countdown():
    global timer_seconds
    global timer_running

    if not timer_running:
        return

    if timer_seconds > 0:
        timer_seconds -= 1

        timer_label.config(
            text=f"⏱️ Time: {timer_seconds}s"
        )

        root.after(1000, countdown)

    else:
        timer_running = False
        game_over("⏰ Time's Up!")


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():
    global attempts_used
    global current_score
    global streak
    global games_won
    global best_score
    global timer_running

    if not timer_running:
        return

    value = guess_entry.get().strip()

    if not value:
        result_label.config(
            text="⚠️ Please enter a number!"
        )
        return

    try:
        guess = int(value)

    except ValueError:
        result_label.config(
            text="❌ Please enter numbers only!"
        )
        return

    settings = DIFFICULTIES[difficulty]

    if guess < 1 or guess > settings["max_number"]:
        result_label.config(
            text=f"⚠️ Enter a number between 1 and {settings['max_number']}!"
        )
        return

    attempts_used += 1

    # -------------------------
    # CORRECT GUESS
    # -------------------------

    if guess == secret_number:

        timer_running = False
        games_won += 1

        # Bonus for remaining attempts
        remaining_attempts = max_attempts - attempts_used
        current_score += remaining_attempts * 10

        # Bonus for time
        current_score += timer_seconds

        streak += 1

        if current_score > best_score:
            best_score = current_score

        result_label.config(
            text=f"🎉 AMAZING!\n"
                 f"You found {secret_number}!",
            fg="#00ff88"
        )

        score_label.config(
            text=f"🏆 Score: {current_score}"
        )

        attempts_label.config(
            text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
        )

        guess_entry.config(state=tk.DISABLED)
        guess_button.config(state=tk.DISABLED)

        update_statistics()
        save_data()

        messagebox.showinfo(
            "🎉 YOU WON!",
            f"Congratulations!\n\n"
            f"Number: {secret_number}\n"
            f"Attempts: {attempts_used}\n"
            f"Score: {current_score}\n"
            f"🔥 Streak: {streak}"
        )

        return

    # -------------------------
    # WRONG GUESS
    # -------------------------

    current_score = max(0, current_score - 10)

    if guess < secret_number:
        result_label.config(
            text="📈 TOO LOW!\nTry a higher number.",
            fg="#ffaa00"
        )

    else:
        result_label.config(
            text="📉 TOO HIGH!\nTry a lower number.",
            fg="#ff7777"
        )

    score_label.config(
        text=f"🏆 Score: {current_score}"
    )

    attempts_label.config(
        text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
    )

    guess_entry.delete(0, tk.END)

    # -------------------------
    # GAME OVER
    # -------------------------

    if attempts_used >= max_attempts:
        game_over("😢 No Attempts Left!")


# =========================================================
# GAME OVER
# =========================================================

def game_over(reason):
    global timer_running
    global streak

    timer_running = False
    streak = 0

    result_label.config(
        text=f"{reason}\nThe number was {secret_number}",
        fg="#ff5555"
    )

    guess_entry.config(state=tk.DISABLED)
    guess_button.config(state=tk.DISABLED)

    update_statistics()
    save_data()

    messagebox.showinfo(
        "Game Over",
        f"{reason}\n\n"
        f"The correct number was: {secret_number}\n\n"
        f"Better luck next time!"
    )


# =========================================================
# DIFFICULTY CHANGE
# =========================================================

def change_difficulty(value):
    global difficulty

    difficulty = value

    new_game()


# =========================================================
# THEME COLORS
# =========================================================

def get_background():
    if dark_mode:
        return "#151522"
    return "#f2f2f2"


def get_card_color():
    if dark_mode:
        return "#222238"
    return "#ffffff"


def get_text_color():
    if dark_mode:
        return "#ffffff"
    return "#222222"


def toggle_theme():
    global dark_mode

    dark_mode = not dark_mode

    apply_theme()


def apply_theme():

    bg = get_background()
    card = get_card_color()
    text = get_text_color()

    root.configure(bg=bg)

    title_label.config(
        bg=bg,
        fg=text
    )

    version_label.config(
        bg=bg
    )

    range_label.config(
        bg=card,
        fg=text
    )

    result_label.config(
        bg=bg
    )

    score_label.config(
        bg=bg
    )

    attempts_label.config(
        bg=bg,
        fg=text
    )

    timer_label.config(
        bg=bg,
        fg=text
    )

    statistics_label.config(
        bg=card,
        fg=text
    )

    difficulty_label.config(
        bg=bg,
        fg=text
    )

    footer_label.config(
        bg=bg
    )


# =========================================================
# STATISTICS
# =========================================================

def update_statistics():

    if games_played > 0:
        win_rate = (games_won / games_played) * 100
    else:
        win_rate = 0

    statistics_label.config(
        text=
        f"📊 STATISTICS\n\n"
        f"Games Played : {games_played}\n"
        f"Games Won   : {games_won}\n"
        f"Win Rate    : {win_rate:.1f}%\n"
        f"Best Score  : {best_score}\n"
        f"🔥 Streak    : {streak}"
    )


# =========================================================
# RESET STATISTICS
# =========================================================

def reset_statistics():

    global best_score
    global streak
    global games_played
    global games_won

    answer = messagebox.askyesno(
        "Reset Statistics",
        "Are you sure you want to reset all statistics?"
    )

    if answer:

        best_score = 0
        streak = 0
        games_played = 0
        games_won = 0

        save_data()
        update_statistics()

        messagebox.showinfo(
            "Statistics Reset",
            "All statistics have been reset."
        )


# =========================================================
# EXIT
# =========================================================

def exit_game():

    answer = messagebox.askyesno(
        "Exit Game",
        "Are you sure you want to exit?"
    )

    if answer:
        save_data()
        root.destroy()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("Number Guessing Game - V19")
root.geometry("600x750")
root.resizable(False, False)

load_data()


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="🎯 NUMBER GUESSING GAME",
    font=("Arial", 25, "bold")
)

title_label.pack(pady=(25, 5))


version_label = tk.Label(
    root,
    text="V19 • PROFESSIONAL EDITION",
    font=("Arial", 11, "bold"),
    fg="#00bfff"
)

version_label.pack(pady=(0, 20))


# =========================================================
# DIFFICULTY
# =========================================================

difficulty_label = tk.Label(
    root,
    text="🎚️ SELECT DIFFICULTY",
    font=("Arial", 12, "bold")
)

difficulty_label.pack()


difficulty_menu = tk.OptionMenu(
    root,
    tk.StringVar(value=difficulty),
    *DIFFICULTIES.keys(),
    command=change_difficulty
)

difficulty_menu.config(
    font=("Arial", 11, "bold"),
    width=12
)

difficulty_menu.pack(pady=10)


# =========================================================
# RANGE
# =========================================================

range_frame = tk.Frame(
    root,
    padx=20,
    pady=12
)

range_frame.pack(pady=10)

range_label = tk.Label(
    range_frame,
    text="Guess a number between 1 and 100",
    font=("Arial", 13, "bold")
)

range_label.pack()


# =========================================================
# ENTRY
# =========================================================

guess_entry = tk.Entry(
    root,
    font=("Arial", 22, "bold"),
    justify="center",
    width=10
)

guess_entry.pack(pady=15)


# =========================================================
# GUESS BUTTON
# =========================================================

guess_button = tk.Button(
    root,
    text="🎯 GUESS",
    font=("Arial", 13, "bold"),
    width=15,
    height=2,
    command=check_guess,
    bg="#008cff",
    fg="white",
    bd=0
)

guess_button.pack(pady=8)


# =========================================================
# RESULT
# =========================================================

result_label = tk.Label(
    root,
    text="🤔 Make your first guess!",
    font=("Arial", 15, "bold"),
    justify="center"
)

result_label.pack(pady=18)


# =========================================================
# SCORE / ATTEMPTS / TIMER
# =========================================================

score_label = tk.Label(
    root,
    text="🏆 Score: 200",
    font=("Arial", 13, "bold"),
    fg="#ffd700"
)

score_label.pack(pady=3)


attempts_label = tk.Label(
    root,
    text="🎯 Attempts: 0/10",
    font=("Arial", 13, "bold")
)

attempts_label.pack(pady=3)


timer_label = tk.Label(
    root,
    text="⏱️ Time: 60s",
    font=("Arial", 13, "bold")
)

timer_label.pack(pady=3)


# =========================================================
# STATISTICS PANEL
# =========================================================

statistics_label = tk.Label(
    root,
    text="",
    font=("Arial", 11, "bold"),
    justify="left",
    padx=20,
    pady=15
)

statistics_label.pack(pady=15)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


new_game_button = tk.Button(
    button_frame,
    text="🔄 NEW GAME",
    font=("Arial", 10, "bold"),
    width=13,
    height=2,
    command=new_game,
    bg="#28a745",
    fg="white",
    bd=0
)

new_game_button.grid(row=0, column=0, padx=5)


theme_button = tk.Button(
    button_frame,
    text="🌓 THEME",
    font=("Arial", 10, "bold"),
    width=13,
    height=2,
    command=toggle_theme,
    bg="#6f42c1",
    fg="white",
    bd=0
)

theme_button.grid(row=0, column=1, padx=5)


reset_button = tk.Button(
    button_frame,
    text="🗑️ RESET",
    font=("Arial", 10, "bold"),
    width=13,
    height=2,
    command=reset_statistics,
    bg="#fd7e14",
    fg="white",
    bd=0
)

reset_button.grid(row=0, column=2, padx=5)


# =========================================================
# EXIT
# =========================================================

exit_button = tk.Button(
    root,
    text="❌ EXIT",
    font=("Arial", 10, "bold"),
    width=12,
    command=exit_game,
    bg="#dc3545",
    fg="white",
    bd=0
)

exit_button.pack(pady=5)


# =========================================================
# FOOTER
# =========================================================

footer_label = tk.Label(
    root,
    text="Python • Tkinter • V19",
    font=("Arial", 9),
    fg="#888888"
)

footer_label.pack(side="bottom", pady=12)


# =========================================================
# KEYBOARD SUPPORT
# =========================================================

root.bind(
    "<Return>",
    lambda event: check_guess()
)


# =========================================================
# APPLY INITIAL THEME
# =========================================================

apply_theme()

update_statistics()

new_game()


# =========================================================
# START
# =========================================================

root.mainloop()