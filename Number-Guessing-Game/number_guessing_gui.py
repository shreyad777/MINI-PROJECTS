import tkinter as tk
from tkinter import messagebox
import random
import json
import os

SAVE_FILE = "leaderboard_v25.json"

# =========================
# COLORS
# =========================

BG = "#10152B"
PANEL = "#1A2140"
PANEL2 = "#242D55"

PURPLE = "#8B5CF6"
BLUE = "#38BDF8"
GREEN = "#22C55E"
YELLOW = "#FACC15"
ORANGE = "#FB923C"
RED = "#F43F5E"
PINK = "#EC4899"
WHITE = "#FFFFFF"
MUTED = "#AAB4D4"

DIFFICULTIES = {
    "Easy": {
        "max": 50,
        "attempts": 15,
        "time": 90,
        "score": 100
    },
    "Medium": {
        "max": 100,
        "attempts": 10,
        "time": 60,
        "score": 200
    },
    "Hard": {
        "max": 500,
        "attempts": 7,
        "time": 45,
        "score": 300
    }
}

MODES = [
    "Single Player",
    "Two Player",
    "Tournament"
]

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("🎯 Number Guessing Game - V25")
root.geometry("1100x720")
root.resizable(False, False)
root.configure(bg=BG)

# =========================
# VARIABLES
# =========================

difficulty = tk.StringVar(value="Medium")
game_mode = tk.StringVar(value="Single Player")

player1_name = tk.StringVar(value="Player 1")
player2_name = tk.StringVar(value="Player 2")

guess_var = tk.StringVar()

rounds_var = tk.StringVar(value="3")

secret_number = 0
attempts_left = 0
time_left = 0
score = 0

current_player = 1

streak = 0
best_streak = 0
combo = 1

hints_used = 0
fast_bonus = 0

player1_wins = 0
player2_wins = 0

tournament_round = 1
total_rounds = 3

timer_id = None
timer_running = False

leaderboard = {}

# =========================
# LEADERBOARD
# =========================

def load_leaderboard():

    global leaderboard

    if os.path.exists(SAVE_FILE):

        try:
            with open(SAVE_FILE, "r") as file:
                leaderboard = json.load(file)

        except:
            leaderboard = {}

    else:
        leaderboard = {}


def save_leaderboard():

    with open(SAVE_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)


def create_player(name):

    if not name.strip():
        name = "Player"

    if name not in leaderboard:

        leaderboard[name] = {
            "wins": 0,
            "games": 0,
            "best_score": 0,
            "best_streak": 0
        }

    return name


def record_player(name, won=False, score_value=0):

    name = create_player(name)

    leaderboard[name]["games"] += 1

    if won:
        leaderboard[name]["wins"] += 1

    if score_value > leaderboard[name]["best_score"]:
        leaderboard[name]["best_score"] = score_value

    if streak > leaderboard[name]["best_streak"]:
        leaderboard[name]["best_streak"] = streak

    save_leaderboard()
    refresh_leaderboard()

# =========================
# UTILITY
# =========================

def cancel_timer():

    global timer_id

    if timer_id is not None:

        try:
            root.after_cancel(timer_id)
        except:
            pass

        timer_id = None


def show_feedback(text, color):

    feedback_label.config(
        text=text,
        fg=color
    )


# =========================
# THEME / VISUAL
# =========================

def flash_screen(color, duration=250):

    old_color = root.cget("bg")

    root.configure(bg=color)

    root.after(
        duration,
        lambda: root.configure(bg=old_color)
    )


# =========================
# SETTINGS
# =========================

def change_difficulty(*args):

    new_game()


def change_mode(*args):

    if game_mode.get() == "Tournament":
        tournament_controls.pack(
            side="left",
            padx=10
        )
    else:
        tournament_controls.pack_forget()

    new_game()


def change_rounds(*args):

    global total_rounds

    try:
        total_rounds = int(rounds_var.get())
    except:
        total_rounds = 3

    new_game()


# =========================
# PLAYER SETUP
# =========================

def set_names():

    p1 = player1_entry.get().strip()

    if not p1:
        p1 = "Player 1"

    player1_name.set(p1)
    create_player(p1)

    if game_mode.get() in [
        "Two Player",
        "Tournament"
    ]:

        p2 = player2_entry.get().strip()

        if not p2:
            p2 = "Player 2"

        player2_name.set(p2)
        create_player(p2)

    save_leaderboard()
    refresh_leaderboard()

    show_feedback(
        "✨ Players updated successfully!",
        GREEN
    )


# =========================
# NEW GAME
# =========================

def new_game():

    global secret_number
    global attempts_left
    global time_left
    global score
    global current_player
    global streak
    global combo
    global hints_used
    global fast_bonus
    global player1_wins
    global player2_wins
    global tournament_round
    global timer_running

    cancel_timer()

    config = DIFFICULTIES[difficulty.get()]

    secret_number = random.randint(
        1,
        config["max"]
    )

    attempts_left = config["attempts"]
    time_left = config["time"]

    score = config["score"]

    current_player = 1

    streak = 0
    combo = 1
    hints_used = 0
    fast_bonus = 0

    player1_wins = 0
    player2_wins = 0

    tournament_round = 1

    timer_running = True

    guess_var.set("")

    show_feedback(
        "🎮 Make your first guess!",
        BLUE
    )

    update_display()
    start_timer()


# =========================
# TIMER
# =========================

def start_timer():

    global timer_running

    timer_running = True
    update_timer()


def update_timer():

    global time_left
    global timer_id
    global timer_running

    if not timer_running:
        return

    timer_label.config(
        text=f"⏱ {time_left}s"
    )

    if time_left <= 0:

        timer_running = False

        game_over(
            "⏰ TIME'S UP!"
        )

        return

    time_left -= 1

    timer_id = root.after(
        1000,
        update_timer
    )


# =========================
# DISPLAY
# =========================

def update_display():

    config = DIFFICULTIES[difficulty.get()]

    range_label.config(
        text=f"🎯 Guess between 1 and {config['max']}"
    )

    attempts_label.config(
        text=f"❤️ Lives: {attempts_left}"
    )

    score_label.config(
        text=f"⭐ Score: {score}"
    )

    streak_label.config(
        text=f"🔥 Streak: {streak}"
    )

    combo_label.config(
        text=f"⚡ COMBO x{combo}"
    )

    hint_count_label.config(
        text=f"💡 Hints: {hints_used}/3"
    )

    if game_mode.get() == "Single Player":

        turn_label.config(
            text=f"👤 {player1_name.get()}'s Turn"
        )

    elif game_mode.get() == "Two Player":

        if current_player == 1:

            turn_label.config(
                text=f"🔵 {player1_name.get()}'s Turn"
            )

        else:

            turn_label.config(
                text=f"🟣 {player2_name.get()}'s Turn"
            )

    else:

        turn_label.config(
            text=(
                f"🏆 Tournament "
                f"Round {tournament_round}/{total_rounds}"
            )
        )


# =========================
# GUESS
# =========================

def make_guess(event=None):

    global attempts_left
    global score
    global current_player
    global streak
    global combo
    global fast_bonus

    value = guess_var.get().strip()

    if not value.isdigit():

        show_feedback(
            "❌ Enter a valid number!",
            RED
        )

        return

    guess = int(value)

    maximum = DIFFICULTIES[
        difficulty.get()
    ]["max"]

    if guess < 1 or guess > maximum:

        show_feedback(
            f"⚠️ Choose between 1 and {maximum}!",
            ORANGE
        )

        return

    attempts_left -= 1

    # =====================
    # CORRECT
    # =====================

    if guess == secret_number:

        global timer_running

        timer_running = False
        cancel_timer()

        streak += 1

        combo = min(
            5,
            1 + (streak // 2)
        )

        fast_bonus = time_left * 2

        base_reward = (
            50
            + (attempts_left * 15)
            + fast_bonus
        )

        score += base_reward * combo

        flash_screen(
            GREEN
        )

        show_feedback(
            "🎉 CORRECT! AMAZING!",
            GREEN
        )

        if game_mode.get() == "Single Player":

            finish_single_player()

        elif game_mode.get() == "Two Player":

            finish_two_player()

        else:

            finish_tournament_round()

        return

    # =====================
    # WRONG
    # =====================

    combo = 1

    if guess < secret_number:

        show_feedback(
            "📈 TOO LOW! Try higher!",
            ORANGE
        )

    else:

        show_feedback(
            "📉 TOO HIGH! Try lower!",
            PINK
        )

    score = max(
        score - 10,
        0
    )

    guess_var.set("")

    if game_mode.get() == "Two Player":

        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

    if attempts_left <= 0:

        game_over(
            "💔 NO LIVES LEFT!"
        )

        return

    update_display()


# =========================
# HINT
# =========================

def use_hint():

    global hints_used
    global score
    global combo

    if hints_used >= 3:

        show_feedback(
            "🚫 Maximum 3 hints per game!",
            RED
        )

        return

    hints_used += 1

    score = max(
        score - 25,
        0
    )

    combo = 1

    if hints_used == 1:

        if secret_number % 2 == 0:
            hint = "💡 The number is EVEN."
        else:
            hint = "💡 The number is ODD."

    elif hints_used == 2:

        maximum = DIFFICULTIES[
            difficulty.get()
        ]["max"]

        if secret_number <= maximum // 2:
            hint = "💡 The number is in the LOWER HALF."
        else:
            hint = "💡 The number is in the UPPER HALF."

    else:

        if secret_number % 5 == 0:

            hint = "💡 The number is divisible by 5."

        elif secret_number % 3 == 0:

            hint = "💡 The number is divisible by 3."

        else:

            hint = "💡 It is NOT divisible by 3 or 5."

    show_feedback(
        hint,
        YELLOW
    )

    update_display()


# =========================
# SINGLE PLAYER
# =========================

def finish_single_player():

    player = player1_name.get()

    record_player(
        player,
        True,
        score
    )

    messagebox.showinfo(
        "🏆 VICTORY!",
        f"🎉 Congratulations {player}!\n\n"
        f"🔢 Number: {secret_number}\n"
        f"⭐ Score: {score}\n"
        f"🔥 Streak: {streak}\n"
        f"⚡ Combo: x{combo}\n"
        f"🎁 Fast Bonus: {fast_bonus}"
    )

    new_game()


# =========================
# TWO PLAYER
# =========================

def finish_two_player():

    global current_player

    winner = (
        player1_name.get()
        if current_player == 1
        else player2_name.get()
    )

    record_player(
        winner,
        True,
        score
    )

    messagebox.showinfo(
        "🏆 WINNER!",
        f"🎉 {winner} guessed it!\n\n"
        f"🔢 Number: {secret_number}\n"
        f"⭐ Score: {score}\n"
        f"🔥 Streak: {streak}"
    )

    new_game()


# =========================
# TOURNAMENT
# =========================

def finish_tournament_round():

    global player1_wins
    global player2_wins
    global tournament_round

    winner = (
        player1_name.get()
        if current_player == 1
        else player2_name.get()
    )

    if current_player == 1:
        player1_wins += 1
    else:
        player2_wins += 1

    record_player(
        winner,
        True,
        score
    )

    if (
        player1_wins > total_rounds // 2
        or player2_wins > total_rounds // 2
    ):

        finish_tournament()

        return

    if tournament_round >= total_rounds:

        finish_tournament()

        return

    messagebox.showinfo(
        "🎉 ROUND COMPLETE!",
        f"{winner} won Round {tournament_round}!"
    )

    tournament_round += 1

    start_tournament_round()


def start_tournament_round():

    global secret_number
    global attempts_left
    global time_left
    global score
    global current_player
    global hints_used
    global combo
    global fast_bonus
    global timer_running

    cancel_timer()

    config = DIFFICULTIES[
        difficulty.get()
    ]

    secret_number = random.randint(
        1,
        config["max"]
    )

    attempts_left = config["attempts"]
    time_left = config["time"]

    score = config["score"]

    current_player = 1

    hints_used = 0
    combo = 1
    fast_bonus = 0

    guess_var.set("")

    timer_running = True

    show_feedback(
        "🥊 NEW ROUND! LET'S GO!",
        BLUE
    )

    update_display()

    start_timer()


def finish_tournament():

    global timer_running

    timer_running = False
    cancel_timer()

    if player1_wins > player2_wins:

        champion = player1_name.get()

    elif player2_wins > player1_wins:

        champion = player2_name.get()

    else:

        champion = "DRAW"

    if champion == "DRAW":

        result = (
            f"🤝 IT'S A DRAW!\n\n"
            f"{player1_name.get()}: "
            f"{player1_wins} wins\n"
            f"{player2_name.get()}: "
            f"{player2_wins} wins"
        )

    else:

        result = (
            f"👑 CHAMPION: {champion}!\n\n"
            f"🔵 {player1_name.get()}: "
            f"{player1_wins} wins\n"
            f"🟣 {player2_name.get()}: "
            f"{player2_wins} wins"
        )

    flash_screen(
        PURPLE,
        400
    )

    messagebox.showinfo(
        "🏆 TOURNAMENT COMPLETE",
        result
    )

    new_game()


# =========================
# GAME OVER
# =========================

def game_over(reason):

    global timer_running
    global streak
    global combo

    timer_running = False
    cancel_timer()

    player = (
        player1_name.get()
        if current_player == 1
        else player2_name.get()
    )

    if game_mode.get() == "Single Player":

        record_player(
            player,
            False,
            score
        )

    streak = 0
    combo = 1

    flash_screen(
        RED,
        350
    )

    messagebox.showinfo(
        "GAME OVER",
        f"{reason}\n\n"
        f"🔢 The number was: {secret_number}\n"
        f"⭐ Final Score: {score}"
    )

    new_game()


# =========================
# LEADERBOARD
# =========================

def refresh_leaderboard():

    for widget in leaderboard_list.winfo_children():
        widget.destroy()

    players = sorted(
        leaderboard.items(),
        key=lambda x: (
            x[1]["best_score"],
            x[1]["wins"]
        ),
        reverse=True
    )

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    if not players:

        tk.Label(
            leaderboard_list,
            text="No players yet!\nBe the first champion! 🚀",
            font=("Arial", 12, "bold"),
            bg=PANEL,
            fg=MUTED
        ).pack(
            pady=30
        )

        return

    for index, (name, data) in enumerate(
        players[:10]
    ):

        if index < 3:
            medal = medals[index]
        else:
            medal = f"{index + 1}."

        card = tk.Frame(
            leaderboard_list,
            bg=PANEL2,
            padx=8,
            pady=6
        )

        card.pack(
            fill="x",
            padx=8,
            pady=4
        )

        tk.Label(
            card,
            text=f"{medal} {name}",
            font=("Arial", 11, "bold"),
            bg=PANEL2,
            fg=WHITE
        ).pack(
            anchor="w"
        )

        tk.Label(
            card,
            text=(
                f"⭐ {data['best_score']}   "
                f"🏆 {data['wins']} wins   "
                f"🔥 {data['best_streak']} streak"
            ),
            font=("Arial", 9),
            bg=PANEL2,
            fg=MUTED
        ).pack(
            anchor="w"
        )


def reset_leaderboard():

    global leaderboard

    confirm = messagebox.askyesno(
        "Reset Leaderboard",
        "Delete the entire leaderboard?"
    )

    if confirm:

        leaderboard = {}

        save_leaderboard()
        refresh_leaderboard()


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x",
    padx=25,
    pady=18
)


tk.Label(
    header,
    text="🎯",
    font=("Arial", 34),
    bg=BG,
    fg=YELLOW
).pack(
    side="left"
)


tk.Label(
    header,
    text="NUMBER GUESSING",
    font=("Arial", 28, "bold"),
    bg=BG,
    fg=WHITE
).pack(
    side="left",
    padx=8
)


tk.Label(
    header,
    text="ARCADE",
    font=("Arial", 28, "bold"),
    bg=BG,
    fg=PURPLE
).pack(
    side="left"
)


tk.Label(
    header,
    text="V25",
    font=("Arial", 12, "bold"),
    bg=PINK,
    fg=WHITE,
    padx=8,
    pady=4
).pack(
    side="right"
)


# =========================
# SETTINGS PANEL
# =========================

settings = tk.Frame(
    root,
    bg=PANEL,
    padx=15,
    pady=12
)

settings.pack(
    fill="x",
    padx=25
)


tk.Label(
    settings,
    text="⚙️ Difficulty",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(
    side="left",
    padx=5
)


difficulty_menu = tk.OptionMenu(
    settings,
    difficulty,
    *DIFFICULTIES.keys(),
    command=change_difficulty
)

difficulty_menu.config(
    bg=PURPLE,
    fg=WHITE,
    activebackground=PINK,
    activeforeground=WHITE,
    relief="flat"
)

difficulty_menu.pack(
    side="left",
    padx=5
)


tk.Label(
    settings,
    text="🎮 Mode",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=WHITE
).pack(
    side="left",
    padx=(20, 5)
)


mode_menu = tk.OptionMenu(
    settings,
    game_mode,
    *MODES,
    command=change_mode
)

mode_menu.config(
    bg=BLUE,
    fg=BG,
    activebackground=GREEN,
    activeforeground=BG,
    relief="flat"
)

mode_menu.pack(
    side="left",
    padx=5
)


tournament_controls = tk.Frame(
    settings,
    bg=PANEL
)

tk.Label(
    tournament_controls,
    text="Rounds:",
    bg=PANEL,
    fg=WHITE
).pack(
    side="left"
)


rounds_menu = tk.OptionMenu(
    tournament_controls,
    rounds_var,
    "3",
    "5",
    command=change_rounds
)

rounds_menu.config(
    bg=ORANGE,
    fg=BG,
    relief="flat"
)

rounds_menu.pack(
    side="left",
    padx=5
)


# =========================
# PLAYER PANEL
# =========================

players = tk.Frame(
    root,
    bg=PANEL,
    padx=15,
    pady=12
)

players.pack(
    fill="x",
    padx=25,
    pady=10
)


tk.Label(
    players,
    text="🔵 Player 1",
    bg=PANEL,
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=5
)


player1_entry = tk.Entry(
    players,
    width=18,
    bg=BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

player1_entry.insert(
    0,
    "Player 1"
)

player1_entry.grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    players,
    text="🟣 Player 2",
    bg=PANEL,
    fg=PINK,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=2,
    padx=5
)


player2_entry = tk.Entry(
    players,
    width=18,
    bg=BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

player2_entry.insert(
    0,
    "Player 2"
)

player2_entry.grid(
    row=0,
    column=3,
    padx=5
)


tk.Button(
    players,
    text="✨ SET PLAYERS",
    command=set_names,
    bg=GREEN,
    fg=BG,
    activebackground=YELLOW,
    relief="flat",
    font=("Arial", 10, "bold"),
    padx=12
).grid(
    row=0,
    column=4,
    padx=15
)


# =========================
# MAIN CONTENT
# =========================

content = tk.Frame(
    root,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=5
)


# =========================
# GAME PANEL
# =========================

game_panel = tk.Frame(
    content,
    bg=PANEL,
    width=700
)

game_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


tk.Label(
    game_panel,
    text="GUESS THE SECRET NUMBER",
    font=("Arial", 18, "bold"),
    bg=PANEL,
    fg=YELLOW
).pack(
    pady=(20, 8)
)


range_label = tk.Label(
    game_panel,
    text="🎯 Guess between 1 and 100",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=WHITE
)

range_label.pack(
    pady=5
)


turn_label = tk.Label(
    game_panel,
    text="👤 Player 1's Turn",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=BLUE
)

turn_label.pack(
    pady=5
)


stats = tk.Frame(
    game_panel,
    bg=PANEL
)

stats.pack(
    pady=12
)


def create_stat(text, color):

    label = tk.Label(
        stats,
        text=text,
        font=("Arial", 11, "bold"),
        bg=PANEL2,
        fg=color,
        padx=12,
        pady=8
    )

    label.pack(
        side="left",
        padx=4
    )

    return label


timer_label = create_stat(
    "⏱ 60s",
    BLUE
)

attempts_label = create_stat(
    "❤️ Lives: 10",
    RED
)

score_label = create_stat(
    "⭐ Score: 200",
    YELLOW
)


streak_label = create_stat(
    "🔥 Streak: 0",
    ORANGE
)


combo_label = create_stat(
    "⚡ COMBO x1",
    PINK
)


hint_count_label = tk.Label(
    game_panel,
    text="💡 Hints: 0/3",
    font=("Arial", 10, "bold"),
    bg=PANEL,
    fg=MUTED
)

hint_count_label.pack(
    pady=3
)


feedback_label = tk.Label(
    game_panel,
    text="🎮 Make your first guess!",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=BLUE
)

feedback_label.pack(
    pady=15
)


guess_entry = tk.Entry(
    game_panel,
    textvariable=guess_var,
    font=("Arial", 22, "bold"),
    justify="center",
    width=10,
    bg=BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

guess_entry.pack(
    pady=5
)

guess_entry.bind(
    "<Return>",
    make_guess
)


buttons = tk.Frame(
    game_panel,
    bg=PANEL
)

buttons.pack(
    pady=18
)


tk.Button(
    buttons,
    text="🎯 GUESS",
    command=make_guess,
    bg=GREEN,
    fg=BG,
    activebackground=YELLOW,
    relief="flat",
    font=("Arial", 12, "bold"),
    width=13,
    pady=8
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    buttons,
    text="💡 HINT",
    command=use_hint,
    bg=YELLOW,
    fg=BG,
    activebackground=ORANGE,
    relief="flat",
    font=("Arial", 12, "bold"),
    width=13,
    pady=8
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    buttons,
    text="🔄 NEW GAME",
    command=new_game,
    bg=PURPLE,
    fg=WHITE,
    activebackground=PINK,
    relief="flat",
    font=("Arial", 12, "bold"),
    width=13,
    pady=8
).grid(
    row=1,
    column=0,
    columnspan=2,
    pady=10
)


# =========================
# LEADERBOARD PANEL
# =========================

leaderboard_panel = tk.Frame(
    content,
    bg=PANEL,
    width=330
)

leaderboard_panel.pack(
    side="right",
    fill="y"
)


tk.Label(
    leaderboard_panel,
    text="🏆 TOP CHAMPIONS",
    font=("Arial", 17, "bold"),
    bg=PANEL,
    fg=YELLOW
).pack(
    pady=15
)


leaderboard_list = tk.Frame(
    leaderboard_panel,
    bg=PANEL
)

leaderboard_list.pack(
    fill="both",
    expand=True
)


tk.Button(
    leaderboard_panel,
    text="🗑 RESET LEADERBOARD",
    command=reset_leaderboard,
    bg=RED,
    fg=WHITE,
    activebackground=PINK,
    relief="flat",
    font=("Arial", 9, "bold"),
    padx=10,
    pady=7
).pack(
    pady=12
)


# =========================
# FOOTER
# =========================

tk.Label(
    root,
    text="🐍 Python • Tkinter • JSON • Arcade Edition • V25",
    font=("Arial", 9),
    bg=BG,
    fg=MUTED
).pack(
    pady=8
)


# =========================
# START
# =========================

load_leaderboard()
refresh_leaderboard()
new_game()

root.mainloop()