import tkinter as tk
from tkinter import messagebox
import random
import json
import os

SAVE_FILE = "leaderboard_v26.json"

# =========================
# COLORS
# =========================

BG = "#0F172A"
PANEL = "#172554"
PANEL2 = "#1E3A5F"

PURPLE = "#8B5CF6"
BLUE = "#38BDF8"
GREEN = "#22C55E"
YELLOW = "#FACC15"
ORANGE = "#FB923C"
RED = "#F43F5E"
PINK = "#EC4899"
CYAN = "#22D3EE"
WHITE = "#FFFFFF"
MUTED = "#A5B4CC"

DIFFICULTIES = {
    "Easy": {"max": 50, "attempts": 15, "time": 90, "score": 100},
    "Medium": {"max": 100, "attempts": 10, "time": 60, "score": 200},
    "Hard": {"max": 500, "attempts": 7, "time": 45, "score": 300}
}

MODES = ["Single Player", "Two Player", "Tournament"]

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("🎮 Number Guessing Game - V26")
root.geometry("1150x760")
root.resizable(False, False)
root.configure(bg=BG)

# =========================
# VARIABLES
# =========================

difficulty = tk.StringVar(value="Medium")
game_mode = tk.StringVar(value="Single Player")
rounds_var = tk.StringVar(value="3")

player1_name = tk.StringVar(value="Player 1")
player2_name = tk.StringVar(value="Player 2")

guess_var = tk.StringVar()

secret_number = 0
attempts_left = 0
time_left = 0
score = 0

current_player = 1

streak = 0
combo = 1

hints_used = 0
fast_bonus = 0

player1_wins = 0
player2_wins = 0

tournament_round = 1
total_rounds = 3

timer_id = None
timer_running = False

# Power-ups
extra_life_available = True
time_freeze_available = True
double_score_available = True
range_reveal_available = True

double_score_active = False

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
# TIMER
# =========================

def cancel_timer():
    global timer_id

    if timer_id is not None:
        try:
            root.after_cancel(timer_id)
        except:
            pass

        timer_id = None


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

    timer_label.config(text=f"⏱ {time_left}s")

    if time_left <= 0:
        timer_running = False
        game_over("⏰ TIME'S UP!")
        return

    time_left -= 1

    timer_id = root.after(1000, update_timer)


# =========================
# VISUAL EFFECTS
# =========================

def flash_screen(color, duration=250):
    old_color = root.cget("bg")

    root.configure(bg=color)

    root.after(
        duration,
        lambda: root.configure(bg=old_color)
    )


def show_feedback(text, color):
    feedback_label.config(
        text=text,
        fg=color
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
# PLAYERS
# =========================

def set_names():

    p1 = player1_entry.get().strip()

    if not p1:
        p1 = "Player 1"

    player1_name.set(p1)
    create_player(p1)

    if game_mode.get() in ["Two Player", "Tournament"]:

        p2 = player2_entry.get().strip()

        if not p2:
            p2 = "Player 2"

        player2_name.set(p2)
        create_player(p2)

    save_leaderboard()
    refresh_leaderboard()

    show_feedback(
        "✨ Players updated!",
        GREEN
    )


# =========================
# NEW GAME
# =========================

def reset_powerups():

    global extra_life_available
    global time_freeze_available
    global double_score_available
    global range_reveal_available
    global double_score_active

    extra_life_available = True
    time_freeze_available = True
    double_score_available = True
    range_reveal_available = True
    double_score_active = False


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

    reset_powerups()

    timer_running = True

    guess_var.set("")

    show_feedback(
        "🎮 Make your first guess!",
        BLUE
    )

    update_display()
    update_powerup_buttons()
    start_timer()


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

    hint_label.config(
        text=f"💡 Hints: {hints_used}/3"
    )

    if game_mode.get() == "Single Player":

        turn_label.config(
            text=f"👤 {player1_name.get()}'s Turn",
            fg=BLUE
        )

    elif game_mode.get() == "Two Player":

        if current_player == 1:
            turn_label.config(
                text=f"🔵 {player1_name.get()}'s Turn",
                fg=BLUE
            )
        else:
            turn_label.config(
                text=f"🟣 {player2_name.get()}'s Turn",
                fg=PINK
            )

    else:

        turn_label.config(
            text=f"🏆 Tournament Round "
                 f"{tournament_round}/{total_rounds}",
            fg=YELLOW
        )


# =========================
# POWER-UP SYSTEM
# =========================

def update_powerup_buttons():

    if extra_life_available:
        extra_life_button.config(
            text="❤️ EXTRA LIFE",
            state="normal",
            bg=RED
        )
    else:
        extra_life_button.config(
            text="❤️ USED",
            state="disabled",
            bg="#4B5563"
        )

    if time_freeze_available:
        time_freeze_button.config(
            text="❄️ TIME FREEZE",
            state="normal",
            bg=CYAN
        )
    else:
        time_freeze_button.config(
            text="❄️ USED",
            state="disabled",
            bg="#4B5563"
        )

    if double_score_available:
        double_score_button.config(
            text="⭐ 2X SCORE",
            state="normal",
            bg=YELLOW
        )
    else:
        double_score_button.config(
            text="⭐ USED",
            state="disabled",
            bg="#4B5563"
        )

    if range_reveal_available:
        range_button.config(
            text="🔍 REVEAL RANGE",
            state="normal",
            bg=PURPLE
        )
    else:
        range_button.config(
            text="🔍 USED",
            state="disabled",
            bg="#4B5563"
        )


def use_extra_life():

    global extra_life_available
    global attempts_left

    if not extra_life_available:
        return

    extra_life_available = False

    attempts_left += 2

    show_feedback(
        "❤️ +2 LIVES!",
        RED
    )

    flash_screen(
        RED,
        180
    )

    update_display()
    update_powerup_buttons()


def use_time_freeze():

    global time_freeze_available
    global timer_running
    global time_left

    if not time_freeze_available:
        return

    time_freeze_available = False

    timer_running = False

    show_feedback(
        "❄️ TIME FROZEN FOR 10 SECONDS!",
        CYAN
    )

    update_powerup_buttons()

    root.after(
        10000,
        resume_timer
    )


def resume_timer():

    global timer_running

    if not timer_running:
        timer_running = True
        update_timer()


def use_double_score():

    global double_score_available
    global double_score_active

    if not double_score_available:
        return

    double_score_available = False
    double_score_active = True

    show_feedback(
        "⭐ DOUBLE SCORE ACTIVATED!",
        YELLOW
    )

    update_powerup_buttons()


def use_range_reveal():

    global range_reveal_available

    if not range_reveal_available:
        return

    range_reveal_available = False

    maximum = DIFFICULTIES[difficulty.get()]["max"]

    lower = max(
        1,
        secret_number - max(5, maximum // 10)
    )

    upper = min(
        maximum,
        secret_number + max(5, maximum // 10)
    )

    show_feedback(
        f"🔍 SECRET IS BETWEEN {lower} AND {upper}!",
        PURPLE
    )

    update_powerup_buttons()


# =========================
# GUESS LOGIC
# =========================

def make_guess(event=None):

    global attempts_left
    global score
    global current_player
    global streak
    global combo
    global fast_bonus
    global double_score_active

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
            1 + streak // 2
        )

        fast_bonus = time_left * 2

        reward = (
            50
            + attempts_left * 15
            + fast_bonus
        )

        if double_score_active:
            reward *= 2
            double_score_active = False

        score += reward * combo

        flash_screen(
            GREEN,
            300
        )

        show_feedback(
            "🎉 PERFECT GUESS!",
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
    double_score_active = False

    if guess < secret_number:

        show_feedback(
            "📈 TOO LOW!",
            ORANGE
        )

    else:

        show_feedback(
            "📉 TOO HIGH!",
            PINK
        )

    score = max(
        0,
        score - 10
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
            "🚫 Maximum 3 hints!",
            RED
        )

        return

    hints_used += 1

    score = max(
        0,
        score - 25
    )

    combo = 1

    maximum = DIFFICULTIES[
        difficulty.get()
    ]["max"]

    if hints_used == 1:

        if secret_number % 2 == 0:
            hint = "💡 EVEN NUMBER"
        else:
            hint = "💡 ODD NUMBER"

    elif hints_used == 2:

        if secret_number <= maximum // 2:
            hint = "💡 LOWER HALF"
        else:
            hint = "💡 UPPER HALF"

    else:

        if secret_number % 5 == 0:
            hint = "💡 DIVISIBLE BY 5"
        elif secret_number % 3 == 0:
            hint = "💡 DIVISIBLE BY 3"
        else:
            hint = "💡 NOT DIVISIBLE BY 3 OR 5"

    show_feedback(
        hint,
        YELLOW
    )

    update_display()


# =========================
# FINISH GAMES
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
        f"🎉 {player} WON!\n\n"
        f"🔢 Number: {secret_number}\n"
        f"⭐ Score: {score}\n"
        f"🔥 Streak: {streak}\n"
        f"⚡ Combo: x{combo}\n"
        f"🎁 Fast Bonus: {fast_bonus}"
    )

    new_game()


def finish_two_player():

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
        f"🎉 {winner} WON!\n\n"
        f"🔢 Number: {secret_number}\n"
        f"⭐ Score: {score}"
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
    global streak
    global combo
    global hints_used
    global fast_bonus
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

    reset_powerups()

    guess_var.set("")

    timer_running = True

    show_feedback(
        "🥊 NEW TOURNAMENT ROUND!",
        BLUE
    )

    update_display()
    update_powerup_buttons()
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
            "🤝 IT'S A DRAW!\n\n"
            f"🔵 {player1_name.get()}: "
            f"{player1_wins} wins\n"
            f"🟣 {player2_name.get()}: "
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
        f"🔢 Number: {secret_number}\n"
        f"⭐ Score: {score}"
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
        key=lambda item: (
            item[1]["best_score"],
            item[1]["wins"]
        ),
        reverse=True
    )

    medals = ["🥇", "🥈", "🥉"]

    if not players:

        tk.Label(
            leaderboard_list,
            text="No champions yet!\n🚀 Be the first!",
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

        medal = (
            medals[index]
            if index < 3
            else f"{index + 1}."
        )

        card = tk.Frame(
            leaderboard_list,
            bg=PANEL2,
            padx=8,
            pady=7
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
                f"🔥 {data['best_streak']}"
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
        "Delete the complete leaderboard?"
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
    pady=15
)


tk.Label(
    header,
    text="🎯",
    font=("Arial", 34),
    bg=BG,
    fg=YELLOW
).pack(side="left")


tk.Label(
    header,
    text="NUMBER GUESSING",
    font=("Arial", 27, "bold"),
    bg=BG,
    fg=WHITE
).pack(
    side="left",
    padx=8
)


tk.Label(
    header,
    text="ARCADE",
    font=("Arial", 27, "bold"),
    bg=BG,
    fg=PURPLE
).pack(side="left")


tk.Label(
    header,
    text="V26",
    font=("Arial", 12, "bold"),
    bg=PINK,
    fg=WHITE,
    padx=9,
    pady=4
).pack(
    side="right"
)


# =========================
# SETTINGS
# =========================

settings = tk.Frame(
    root,
    bg=PANEL,
    padx=15,
    pady=10
)

settings.pack(
    fill="x",
    padx=25
)


tk.Label(
    settings,
    text="⚙️ Difficulty",
    bg=PANEL,
    fg=WHITE,
    font=("Arial", 10, "bold")
).pack(
    side="left"
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
    padx=7
)


tk.Label(
    settings,
    text="🎮 Mode",
    bg=PANEL,
    fg=WHITE,
    font=("Arial", 10, "bold")
).pack(
    side="left",
    padx=(15, 5)
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
    relief="flat"
)

mode_menu.pack(
    side="left"
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
    pady=10
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
    padx=25
)


# =========================
# GAME PANEL
# =========================

game_panel = tk.Frame(
    content,
    bg=PANEL
)

game_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


tk.Label(
    game_panel,
    text="⚡ POWER-UP ARENA ⚡",
    font=("Arial", 18, "bold"),
    bg=PANEL,
    fg=YELLOW
).pack(
    pady=(15, 5)
)


range_label = tk.Label(
    game_panel,
    text="🎯 Guess between 1 and 100",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=WHITE
)

range_label.pack(pady=3)


turn_label = tk.Label(
    game_panel,
    text="👤 Player 1's Turn",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=BLUE
)

turn_label.pack(pady=3)


stats = tk.Frame(
    game_panel,
    bg=PANEL
)

stats.pack(
    pady=8
)


def stat_box(text, color):

    label = tk.Label(
        stats,
        text=text,
        font=("Arial", 10, "bold"),
        bg=PANEL2,
        fg=color,
        padx=9,
        pady=6
    )

    label.pack(
        side="left",
        padx=3
    )

    return label


timer_label = stat_box("⏱ 60s", BLUE)
attempts_label = stat_box("❤️ Lives: 10", RED)
score_label = stat_box("⭐ Score: 200", YELLOW)
streak_label = stat_box("🔥 Streak: 0", ORANGE)
combo_label = stat_box("⚡ x1", PINK)


hint_label = tk.Label(
    game_panel,
    text="💡 Hints: 0/3",
    font=("Arial", 9, "bold"),
    bg=PANEL,
    fg=MUTED
)

hint_label.pack()


feedback_label = tk.Label(
    game_panel,
    text="🎮 Make your first guess!",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=BLUE
)

feedback_label.pack(
    pady=8
)


guess_entry = tk.Entry(
    game_panel,
    textvariable=guess_var,
    font=("Arial", 21, "bold"),
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


# =========================
# MAIN BUTTONS
# =========================

buttons = tk.Frame(
    game_panel,
    bg=PANEL
)

buttons.pack(
    pady=10
)


tk.Button(
    buttons,
    text="🎯 GUESS",
    command=make_guess,
    bg=GREEN,
    fg=BG,
    activebackground=YELLOW,
    relief="flat",
    font=("Arial", 11, "bold"),
    width=12,
    pady=6
).grid(
    row=0,
    column=0,
    padx=4
)


tk.Button(
    buttons,
    text="💡 HINT",
    command=use_hint,
    bg=YELLOW,
    fg=BG,
    activebackground=ORANGE,
    relief="flat",
    font=("Arial", 11, "bold"),
    width=12,
    pady=6
).grid(
    row=0,
    column=1,
    padx=4
)


tk.Button(
    buttons,
    text="🔄 NEW GAME",
    command=new_game,
    bg=PURPLE,
    fg=WHITE,
    activebackground=PINK,
    relief="flat",
    font=("Arial", 11, "bold"),
    width=12,
    pady=6
).grid(
    row=0,
    column=2,
    padx=4
)


# =========================
# POWER-UP PANEL
# =========================

powerup_panel = tk.Frame(
    game_panel,
    bg=PANEL2,
    padx=8,
    pady=8
)

powerup_panel.pack(
    fill="x",
    padx=15,
    pady=8
)


tk.Label(
    powerup_panel,
    text="🚀 POWER-UPS",
    font=("Arial", 11, "bold"),
    bg=PANEL2,
    fg=CYAN
).pack(
    pady=(0, 6)
)


power_buttons = tk.Frame(
    powerup_panel,
    bg=PANEL2
)

power_buttons.pack()


extra_life_button = tk.Button(
    power_buttons,
    text="❤️ EXTRA LIFE",
    command=use_extra_life,
    bg=RED,
    fg=WHITE,
    relief="flat",
    font=("Arial", 9, "bold"),
    width=15,
    pady=5
)

extra_life_button.grid(
    row=0,
    column=0,
    padx=3
)


time_freeze_button = tk.Button(
    power_buttons,
    text="❄️ TIME FREEZE",
    command=use_time_freeze,
    bg=CYAN,
    fg=BG,
    relief="flat",
    font=("Arial", 9, "bold"),
    width=15,
    pady=5
)

time_freeze_button.grid(
    row=0,
    column=1,
    padx=3
)


double_score_button = tk.Button(
    power_buttons,
    text="⭐ 2X SCORE",
    command=use_double_score,
    bg=YELLOW,
    fg=BG,
    relief="flat",
    font=("Arial", 9, "bold"),
    width=15,
    pady=5
)

double_score_button.grid(
    row=1,
    column=0,
    padx=3,
    pady=5
)


range_button = tk.Button(
    power_buttons,
    text="🔍 REVEAL RANGE",
    command=use_range_reveal,
    bg=PURPLE,
    fg=WHITE,
    relief="flat",
    font=("Arial", 9, "bold"),
    width=15,
    pady=5
)

range_button.grid(
    row=1,
    column=1,
    padx=3,
    pady=5
)


# =========================
# LEADERBOARD
# =========================

leaderboard_panel = tk.Frame(
    content,
    bg=PANEL,
    width=325
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
    pady=6
).pack(
    pady=10
)


# =========================
# FOOTER
# =========================

tk.Label(
    root,
    text="🐍 Python • Tkinter • JSON • Power-Ups • Arcade Edition • V26",
    font=("Arial", 9),
    bg=BG,
    fg=MUTED
).pack(
    pady=7
)


# =========================
# START
# =========================

load_leaderboard()
refresh_leaderboard()
new_game()

root.mainloop()