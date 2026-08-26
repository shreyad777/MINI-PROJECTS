import tkinter as tk
from tkinter import messagebox
import random
import json
import os


# ==========================================
# DATA
# ==========================================

DATA_FILE = "game_data.json"

secret_number = 0
minimum = 1
maximum = 100

attempts = 0
max_attempts = 10
score = 0

player_name = ""

games_played = 0
games_won = 0
games_lost = 0
best_score = 0

game_history = []


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            return (
                data.get("games_played", 0),
                data.get("games_won", 0),
                data.get("games_lost", 0),
                data.get("best_score", 0),
                data.get("game_history", [])
            )

        except (json.JSONDecodeError, OSError):

            return 0, 0, 0, 0, []

    return 0, 0, 0, 0, []


(
    games_played,
    games_won,
    games_lost,
    best_score,
    game_history
) = load_data()


# ==========================================
# SAVE DATA
# ==========================================

def save_data():

    data = {
        "games_played": games_played,
        "games_won": games_won,
        "games_lost": games_lost,
        "best_score": best_score,
        "game_history": game_history
    }

    try:

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:

        print("Unable to save game data.")


# ==========================================
# UPDATE DASHBOARD
# ==========================================

def update_dashboard():

    played_value.config(
        text=str(games_played)
    )

    won_value.config(
        text=str(games_won)
    )

    lost_value.config(
        text=str(games_lost)
    )

    best_value.config(
        text=str(best_score)
    )


# ==========================================
# START PLAYER GAME
# ==========================================

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


# ==========================================
# SET DIFFICULTY
# ==========================================

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

    else:

        minimum = 1
        maximum = 200

    start_new_game()


# ==========================================
# START NEW GAME
# ==========================================

def start_new_game():

    global secret_number
    global attempts
    global score

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Please enter your name and click Start Game first."
        )

        return

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

    attempts_value.config(
        text=f"0 / {max_attempts}"
    )

    score_value.config(
        text="0"
    )


# ==========================================
# ADD HISTORY
# ==========================================

def add_history(result, final_score):

    difficulty = difficulty_var.get()

    game_record = {
        "player": player_name,
        "difficulty": difficulty,
        "result": result,
        "attempts": attempts,
        "score": final_score
    }

    game_history.append(
        game_record
    )

    save_data()


# ==========================================
# SHOW HISTORY
# ==========================================
def reset_data():

    global games_played
    global games_won
    global games_lost
    global best_score
    global game_history

    confirmation = messagebox.askyesno(
        "Reset Game Data",
        "Are you sure you want to delete all game statistics and history?\n\n"
        "This action cannot be undone."
    )

    if not confirmation:
        return

    games_played = 0
    games_won = 0
    games_lost = 0
    best_score = 0
    game_history = []

    save_data()

    update_dashboard()

    messagebox.showinfo(
        "Data Reset",
        "All game statistics and history have been cleared."
    )
def show_history():

    history_window = tk.Toplevel(root)

    history_window.title(
        "Game History"
    )

    history_window.geometry(
        "700x550"
    )

    history_window.resizable(
        False,
        False
    )

    tk.Label(
        history_window,
        text="📜 Game History",
        font=("Segoe UI", 22, "bold")
    ).pack(
        pady=20
    )

    if not game_history:

        tk.Label(
            history_window,
            text="No games played yet.",
            font=("Segoe UI", 13)
        ).pack(
            pady=50
        )

        return

    frame = tk.Frame(
        history_window
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    scrollbar = tk.Scrollbar(
        frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    history_text = tk.Text(
        frame,
        font=("Consolas", 11),
        yscrollcommand=scrollbar.set,
        wrap="none"
    )

    history_text.pack(
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=history_text.yview
    )

    for index, game in enumerate(
        reversed(game_history),
        start=1
    ):

        history_text.insert(
            tk.END,
            f"GAME {index}\n"
        )

        history_text.insert(
            tk.END,
            f"Player     : {game['player']}\n"
        )

        history_text.insert(
            tk.END,
            f"Difficulty : {game['difficulty']}\n"
        )

        history_text.insert(
            tk.END,
            f"Result     : {game['result']}\n"
        )

        history_text.insert(
            tk.END,
            f"Attempts   : {game['attempts']}\n"
        )

        history_text.insert(
            tk.END,
            f"Score      : {game['score']}\n"
        )

        history_text.insert(
            tk.END,
            "-" * 55 + "\n\n"
        )

    history_text.config(
        state="disabled"
    )


# ==========================================
# CHECK GUESS
# ==========================================

def check_guess():

    global attempts
    global score
    global best_score
    global games_played
    global games_won
    global games_lost

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Please enter your name and start a game first."
        )

        return

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

    attempts_value.config(
        text=f"{attempts} / {max_attempts}"
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

        score_value.config(
            text=str(score)
        )

        add_history(
            "Won",
            score
        )

        update_dashboard()

        result_label.config(
            text=(
                f"🎉 Congratulations, {player_name}!\n"
                f"You found the number!"
            )
        )

        messagebox.showinfo(
            "You Won!",
            f"Congratulations, {player_name}!\n\n"
            f"Attempts: {attempts}\n"
            f"Score: {score}\n"
            f"Best Score: {best_score}"
        )

        return

    if attempts >= max_attempts:

        games_played += 1
        games_lost += 1

        add_history(
            "Lost",
            0
        )

        update_dashboard()

        result_label.config(
            text=(
                f"❌ Game Over!\n"
                f"The number was {secret_number}."
            )
        )

        messagebox.showinfo(
            "Game Over",
            f"Better luck next time, {player_name}!\n\n"
            f"The number was {secret_number}."
        )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Number Guessing Game | Dashboard"
)

root.geometry(
    "900x750"
)

root.resizable(
    False,
    False
)


# ==========================================
# HEADER
# ==========================================

header = tk.Frame(
    root,
    padx=30,
    pady=20
)

header.pack(
    fill="x"
)

tk.Label(
    header,
    text="🎯 Number Guessing Game",
    font=("Segoe UI", 26, "bold")
).pack(
    side="left"
)

tk.Label(
    header,
    text="Challenge yourself. Beat your best score.",
    font=("Segoe UI", 11)
).pack(
    side="right",
    pady=10
)


# ==========================================
# PLAYER SECTION
# ==========================================

player_frame = tk.LabelFrame(
    root,
    text="  👤 Player Setup  ",
    font=("Segoe UI", 12, "bold"),
    padx=20,
    pady=15
)

player_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Label(
    player_frame,
    text="Player Name:",
    font=("Segoe UI", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)


name_entry = tk.Entry(
    player_frame,
    font=("Segoe UI", 11),
    width=22
)

name_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Label(
    player_frame,
    text="Difficulty:",
    font=("Segoe UI", 11, "bold")
).grid(
    row=0,
    column=2,
    padx=10
)


difficulty_var = tk.StringVar(
    value="Medium"
)


difficulty_menu = tk.OptionMenu(
    player_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard"
)

difficulty_menu.config(
    font=("Segoe UI", 10),
    width=10
)

difficulty_menu.grid(
    row=0,
    column=3,
    padx=10
)
tk.Button(
    player_frame,
    text="🗑️ RESET DATA",
    font=("Segoe UI", 10, "bold"),
    command=reset_data,
    width=18,
    pady=8
).grid(
    row=0,
    column=2,
    padx=10
)

tk.Button(
    player_frame,
    text="START GAME",
    font=("Segoe UI", 10, "bold"),
    command=start_player_game,
    padx=15,
    pady=5
).grid(
    row=0,
    column=4,
    padx=15
)


# ==========================================
# STATISTICS DASHBOARD
# ==========================================

stats_frame = tk.LabelFrame(
    root,
    text="  📊 Your Statistics  ",
    font=("Segoe UI", 12, "bold"),
    padx=15,
    pady=15
)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


def create_stat_card(
    parent,
    title,
    value,
    column
):

    frame = tk.Frame(
        parent,
        padx=25,
        pady=10
    )

    frame.grid(
        row=0,
        column=column,
        padx=8
    )

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 10)
    ).pack()

    value_label = tk.Label(
        frame,
        text=str(value),
        font=("Segoe UI", 22, "bold")
    )

    value_label.pack()

    return value_label


played_value = create_stat_card(
    stats_frame,
    "Games Played",
    games_played,
    0
)

won_value = create_stat_card(
    stats_frame,
    "Games Won",
    games_won,
    1
)

lost_value = create_stat_card(
    stats_frame,
    "Games Lost",
    games_lost,
    2
)

best_value = create_stat_card(
    stats_frame,
    "Best Score",
    best_score,
    3
)


# ==========================================
# GAME AREA
# ==========================================

game_frame = tk.LabelFrame(
    root,
    text="  🎮 Current Game  ",
    font=("Segoe UI", 12, "bold"),
    padx=30,
    pady=20
)

game_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


result_label = tk.Label(
    game_frame,
    text="Enter your name and start a game.",
    font=("Segoe UI", 14, "bold"),
    wraplength=700,
    justify="center"
)

result_label.pack(
    pady=10
)


guess_entry = tk.Entry(
    game_frame,
    font=("Segoe UI", 20),
    justify="center",
    width=12
)

guess_entry.pack(
    pady=10
)


tk.Button(
    game_frame,
    text="GUESS",
    font=("Segoe UI", 12, "bold"),
    command=check_guess,
    width=15,
    pady=8
).pack(
    pady=10
)


# ==========================================
# CURRENT GAME INFO
# ==========================================

info_frame = tk.Frame(
    game_frame
)

info_frame.pack(
    pady=10
)


tk.Label(
    info_frame,
    text="Attempts",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=0,
    padx=40
)


tk.Label(
    info_frame,
    text="Score",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=1,
    padx=40
)


attempts_value = tk.Label(
    info_frame,
    text="0 / 10",
    font=("Segoe UI", 16, "bold")
)

attempts_value.grid(
    row=1,
    column=0,
    padx=40
)


score_value = tk.Label(
    info_frame,
    text="0",
    font=("Segoe UI", 16, "bold")
)

score_value.grid(
    row=1,
    column=1,
    padx=40
)


# ==========================================
# ACTION BUTTONS
# ==========================================

action_frame = tk.Frame(
    root
)

action_frame.pack(
    pady=15
)


tk.Button(
    action_frame,
    text="🔄 NEW GAME",
    font=("Segoe UI", 10, "bold"),
    command=start_new_game,
    width=18,
    pady=8
).grid(
    row=0,
    column=0,
    padx=10
)


tk.Button(
    action_frame,
    text="📜 GAME HISTORY",
    font=("Segoe UI", 10, "bold"),
    command=show_history,
    width=18,
    pady=8
).grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# FOOTER
# ==========================================

tk.Label(
    root,
    text="Python • Tkinter • JSON",
    font=("Segoe UI", 9)
).pack(
    pady=5
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()