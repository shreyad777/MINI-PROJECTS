import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# =========================================================
# NUMBER GUESSING GAME - V23
# LEADERBOARD & TOURNAMENT EDITION
# =========================================================

SAVE_FILE = "leaderboard_v23.json"

DIFFICULTIES = {
    "Easy": {
        "maximum": 50,
        "attempts": 15,
        "time": 90,
        "starting_score": 100
    },
    "Medium": {
        "maximum": 100,
        "attempts": 10,
        "time": 60,
        "starting_score": 200
    },
    "Hard": {
        "maximum": 500,
        "attempts": 7,
        "time": 45,
        "starting_score": 300
    }
}

# =========================================================
# GLOBAL VARIABLES
# =========================================================

game_mode = "Single Player"
difficulty = "Medium"

secret_number = 0
current_player = 1

attempts_used = 0
max_attempts = 10
timer_seconds = 60
timer_running = False

player1_name = "Player 1"
player2_name = "Player 2"

player1_score = 0
player2_score = 0

player1_wins = 0
player2_wins = 0

player1_streak = 0
player2_streak = 0

hints_used = 0

tournament_round = 1
tournament_total_rounds = 3

round_active = False

dark_mode = True

leaderboard = {}


# =========================================================
# LOAD LEADERBOARD
# =========================================================

def load_leaderboard():

    global leaderboard

    if not os.path.exists(SAVE_FILE):
        leaderboard = {}
        return

    try:

        with open(SAVE_FILE, "r") as file:
            leaderboard = json.load(file)

    except (json.JSONDecodeError, OSError):

        leaderboard = {}


# =========================================================
# SAVE LEADERBOARD
# =========================================================

def save_leaderboard():

    try:

        with open(SAVE_FILE, "w") as file:
            json.dump(
                leaderboard,
                file,
                indent=4
            )

    except OSError:
        pass


# =========================================================
# CREATE PLAYER RECORD
# =========================================================

def create_player(name):

    if name not in leaderboard:

        leaderboard[name] = {
            "wins": 0,
            "games": 0,
            "best_score": 0,
            "streak": 0,
            "best_streak": 0
        }


# =========================================================
# UPDATE PLAYER RECORD
# =========================================================

def update_player_record(
    name,
    won=False,
    score=0
):

    create_player(name)

    leaderboard[name]["games"] += 1

    if won:

        leaderboard[name]["wins"] += 1
        leaderboard[name]["streak"] += 1

    else:

        leaderboard[name]["streak"] = 0

    if score > leaderboard[name]["best_score"]:

        leaderboard[name]["best_score"] = score

    if (
        leaderboard[name]["streak"]
        > leaderboard[name]["best_streak"]
    ):

        leaderboard[name]["best_streak"] = (
            leaderboard[name]["streak"]
        )

    save_leaderboard()


# =========================================================
# THEME
# =========================================================

def get_background():

    return "#0f1117" if dark_mode else "#f3f5f7"


def get_card():

    return "#1b1f2a" if dark_mode else "#ffffff"


def get_text():

    return "#ffffff" if dark_mode else "#222222"


def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    apply_theme()


def apply_theme():

    bg = get_background()
    card = get_card()
    text = get_text()

    root.configure(bg=bg)

    for widget in [
        title_label,
        subtitle_label,
        mode_label,
        difficulty_label,
        player_turn_label,
        result_label,
        score_label,
        attempts_label,
        timer_label,
        streak_label,
        round_label,
        footer_label
    ]:

        widget.configure(
            bg=bg
        )

    title_label.configure(
        fg=text
    )

    mode_label.configure(
        fg=text
    )

    difficulty_label.configure(
        fg=text
    )

    player_turn_label.configure(
        fg=text
    )

    attempts_label.configure(
        fg=text
    )

    timer_label.configure(
        fg=text
    )

    streak_label.configure(
        fg=text
    )

    round_label.configure(
        fg="#00bfff"
    )

    range_frame.configure(
        bg=card
    )

    range_label.configure(
        bg=card,
        fg=text
    )

    leaderboard_frame.configure(
        bg=card
    )

    leaderboard_title.configure(
        bg=card,
        fg=text
    )

    leaderboard_text.configure(
        bg=card,
        fg=text
    )


# =========================================================
# SET PLAYER NAMES
# =========================================================

def set_names():

    global player1_name
    global player2_name

    name1 = player1_entry.get().strip()
    name2 = player2_entry.get().strip()

    if not name1:
        name1 = "Player 1"

    if not name2:
        name2 = "Player 2"

    player1_name = name1
    player2_name = name2

    create_player(player1_name)
    create_player(player2_name)

    save_leaderboard()

    update_leaderboard()

    if game_mode == "Single Player":

        player_turn_label.configure(
            text=f"👤 {player1_name}'S GAME"
        )

    else:

        player_turn_label.configure(
            text=f"👤 {player1_name}'S TURN"
        )

    messagebox.showinfo(
        "Players",
        (
            f"Player 1: {player1_name}\n"
            f"Player 2: {player2_name}"
        )
    )


# =========================================================
# CHANGE MODE
# =========================================================

def change_mode(value):

    global game_mode

    game_mode = value

    if game_mode == "Single Player":

        player2_entry.configure(
            state=tk.DISABLED
        )

    else:

        player2_entry.configure(
            state=tk.NORMAL
        )

    if game_mode == "Tournament":

        tournament_frame.pack(
            pady=5
        )

    else:

        tournament_frame.pack_forget()

    new_game()


# =========================================================
# CHANGE DIFFICULTY
# =========================================================

def change_difficulty(value):

    global difficulty

    difficulty = value

    new_game()


# =========================================================
# CHANGE TOURNAMENT LENGTH
# =========================================================

def change_tournament_length(value):

    global tournament_total_rounds

    tournament_total_rounds = int(value)

    new_game()


# =========================================================
# NEW GAME
# =========================================================

def new_game():

    global secret_number
    global current_player
    global attempts_used
    global max_attempts
    global timer_seconds
    global timer_running
    global player1_score
    global player2_score
    global player1_wins
    global player2_wins
    global player1_streak
    global player2_streak
    global hints_used
    global tournament_round
    global round_active

    settings = DIFFICULTIES[difficulty]

    secret_number = random.randint(
        1,
        settings["maximum"]
    )

    current_player = 1

    attempts_used = 0
    max_attempts = settings["attempts"]

    timer_seconds = settings["time"]

    timer_running = True

    player1_score = settings["starting_score"]
    player2_score = settings["starting_score"]

    player1_wins = 0
    player2_wins = 0

    player1_streak = 0
    player2_streak = 0

    hints_used = 0

    tournament_round = 1

    round_active = True

    guess_entry.configure(
        state=tk.NORMAL
    )

    guess_button.configure(
        state=tk.NORMAL
    )

    hint_button.configure(
        state=tk.NORMAL
    )

    guess_entry.delete(
        0,
        tk.END
    )

    update_game_information()

    result_label.configure(
        text="🤔 A secret number has been generated.",
        fg="#00bfff"
    )

    guess_entry.focus()

    countdown()


# =========================================================
# GAME INFORMATION
# =========================================================

def update_game_information():

    if game_mode == "Single Player":

        player_turn_label.configure(
            text=f"👤 {player1_name.upper()}'S TURN"
        )

        score_label.configure(
            text=f"🏆 Score: {player1_score}"
        )

        streak_label.configure(
            text=f"🔥 Streak: {player1_streak}"
        )

        round_label.configure(
            text="🎮 SINGLE PLAYER"
        )

    elif game_mode == "Two Player":

        if current_player == 1:

            player_turn_label.configure(
                text=f"👤 {player1_name.upper()}'S TURN"
            )

        else:

            player_turn_label.configure(
                text=f"👤 {player2_name.upper()}'S TURN"
            )

        score_label.configure(
            text=(
                f"🏆 {player1_name}: {player1_score}    "
                f"{player2_name}: {player2_score}"
            )
        )

        streak_label.configure(
            text=(
                f"🔥 {player1_name}: {player1_streak}    "
                f"{player2_name}: {player2_streak}"
            )
        )

        round_label.configure(
            text="⚔️ TWO PLAYER MATCH"
        )

    else:

        if current_player == 1:

            player_turn_label.configure(
                text=f"👤 {player1_name.upper()}'S TURN"
            )

        else:

            player_turn_label.configure(
                text=f"👤 {player2_name.upper()}'S TURN"
            )

        score_label.configure(
            text=(
                f"🏆 {player1_name}: {player1_wins} wins    "
                f"{player2_name}: {player2_wins} wins"
            )
        )

        streak_label.configure(
            text=(
                f"🔥 Scores: "
                f"{player1_score} - {player2_score}"
            )
        )

        round_label.configure(
            text=(
                f"🏆 TOURNAMENT "
                f"ROUND {tournament_round}/"
                f"{tournament_total_rounds}"
            )
        )

    attempts_label.configure(
        text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
    )

    timer_label.configure(
        text=f"⏱️ Time: {timer_seconds}s"
    )


# =========================================================
# TIMER
# =========================================================

def countdown():

    global timer_seconds
    global timer_running

    if not timer_running:
        return

    if timer_seconds > 0:

        timer_seconds -= 1

        timer_label.configure(
            text=f"⏱️ Time: {timer_seconds}s"
        )

        root.after(
            1000,
            countdown
        )

    else:

        timer_running = False

        game_over(
            "⏰ TIME'S UP!"
        )


# =========================================================
# HINT
# =========================================================

def use_hint():

    global hints_used
    global player1_score
    global player2_score

    if not timer_running:
        return

    if hints_used >= 3:

        messagebox.showwarning(
            "Hints",
            "You have already used all 3 hints."
        )

        return

    hints_used += 1

    if current_player == 1:

        player1_score = max(
            0,
            player1_score - 25
        )

    else:

        player2_score = max(
            0,
            player2_score - 25
        )

    if hints_used == 1:

        if secret_number % 2 == 0:

            hint = "💡 Hint: The number is EVEN."

        else:

            hint = "💡 Hint: The number is ODD."

    elif hints_used == 2:

        maximum = DIFFICULTIES[difficulty]["maximum"]

        if secret_number <= maximum // 2:

            hint = (
                f"💡 Hint: The number is in "
                f"the lower half."
            )

        else:

            hint = (
                f"💡 Hint: The number is in "
                f"the upper half."
            )

    else:

        lower = max(
            1,
            secret_number - 10
        )

        upper = min(
            DIFFICULTIES[difficulty]["maximum"],
            secret_number + 10
        )

        hint = (
            f"💡 FINAL HINT\n"
            f"The number is between "
            f"{lower} and {upper}."
        )

    result_label.configure(
        text=hint,
        fg="#00bfff"
    )

    update_game_information()


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():

    global attempts_used
    global player1_score
    global player2_score
    global player1_streak
    global player2_streak
    global current_player
    global timer_running

    if not timer_running:
        return

    value = guess_entry.get().strip()

    if not value:

        result_label.configure(
            text="⚠️ Enter a number first."
        )

        return

    try:

        guess = int(value)

    except ValueError:

        result_label.configure(
            text="❌ Numbers only."
        )

        return

    maximum = DIFFICULTIES[difficulty]["maximum"]

    if guess < 1 or guess > maximum:

        result_label.configure(
            text=(
                f"⚠️ Enter a number from "
                f"1 to {maximum}."
            )
        )

        return

    attempts_used += 1

    # =====================================================
    # CORRECT GUESS
    # =====================================================

    if guess == secret_number:

        timer_running = False

        remaining_attempts = (
            max_attempts - attempts_used
        )

        bonus = (
            remaining_attempts * 15
            + timer_seconds
            - hints_used * 25
        )

        bonus = max(
            10,
            bonus
        )

        if current_player == 1:

            player1_score += bonus
            player1_streak += 1

            winner = player1_name

        else:

            player2_score += bonus
            player2_streak += 1

            winner = player2_name

        result_label.configure(
            text=(
                f"🎉 CORRECT!\n"
                f"{winner} wins the round!"
            ),
            fg="#00ff88"
        )

        if game_mode == "Tournament":

            if current_player == 1:

                player1_wins += 1

            else:

                player2_wins += 1

            update_player_record(
                winner,
                won=True,
                score=(
                    player1_score
                    if current_player == 1
                    else player2_score
                )
            )

            update_game_information()

            root.after(
                1200,
                next_tournament_round
            )

        else:

            update_player_record(
                winner,
                won=True,
                score=(
                    player1_score
                    if current_player == 1
                    else player2_score
                )
            )

            finish_normal_game(
                winner,
                bonus
            )

        return

    # =====================================================
    # WRONG GUESS
    # =====================================================

    if current_player == 1:

        player1_score = max(
            0,
            player1_score - 10
        )

    else:

        player2_score = max(
            0,
            player2_score - 10
        )

    if guess < secret_number:

        result_label.configure(
            text="📈 TOO LOW!\nTry a higher number.",
            fg="#ffaa00"
        )

    else:

        result_label.configure(
            text="📉 TOO HIGH!\nTry a lower number.",
            fg="#ff7777"
        )

    guess_entry.delete(
        0,
        tk.END
    )

    if (
        game_mode != "Single Player"
        and attempts_used < max_attempts
    ):

        current_player = (
            2 if current_player == 1 else 1
        )

    update_game_information()

    if attempts_used >= max_attempts:

        game_over(
            "😢 NO ATTEMPTS LEFT!"
        )


# =========================================================
# NORMAL GAME FINISH
# =========================================================

def finish_normal_game(
    winner,
    bonus
):

    global round_active

    round_active = False

    guess_entry.configure(
        state=tk.DISABLED
    )

    guess_button.configure(
        state=tk.DISABLED
    )

    hint_button.configure(
        state=tk.DISABLED
    )

    update_game_information()

    save_leaderboard()

    update_leaderboard()

    messagebox.showinfo(
        "🏆 WINNER!",
        (
            f"Congratulations, {winner}!\n\n"
            f"Secret Number: {secret_number}\n"
            f"Bonus Score: +{bonus}\n"
            f"Final Score: "
            f"{player1_score if winner == player1_name else player2_score}"
        )
    )


# =========================================================
# NEXT TOURNAMENT ROUND
# =========================================================

def next_tournament_round():

    global tournament_round
    global current_player
    global secret_number
    global attempts_used
    global timer_seconds
    global timer_running
    global hints_used
    global round_active

    if (
        player1_wins
        > tournament_total_rounds // 2
    ):

        finish_tournament(
            player1_name
        )

        return

    if (
        player2_wins
        > tournament_total_rounds // 2
    ):

        finish_tournament(
            player2_name
        )

        return

    if tournament_round >= tournament_total_rounds:

        if player1_wins > player2_wins:

            finish_tournament(
                player1_name
            )

        elif player2_wins > player1_wins:

            finish_tournament(
                player2_name
            )

        else:

            finish_tournament(
                "DRAW"
            )

        return

    tournament_round += 1

    current_player = (
        2 if current_player == 1 else 1
    )

    settings = DIFFICULTIES[difficulty]

    secret_number = random.randint(
        1,
        settings["maximum"]
    )

    attempts_used = 0

    timer_seconds = settings["time"]

    hints_used = 0

    timer_running = True
    round_active = True

    guess_entry.configure(
        state=tk.NORMAL
    )

    guess_button.configure(
        state=tk.NORMAL
    )

    hint_button.configure(
        state=tk.NORMAL
    )

    guess_entry.delete(
        0,
        tk.END
    )

    result_label.configure(
        text=(
            f"⚔️ ROUND {tournament_round}\n"
            f"New number generated!"
        ),
        fg="#00bfff"
    )

    update_game_information()

    guess_entry.focus()

    countdown()


# =========================================================
# FINISH TOURNAMENT
# =========================================================

def finish_tournament(winner):

    global round_active
    global timer_running

    round_active = False
    timer_running = False

    guess_entry.configure(
        state=tk.DISABLED
    )

    guess_button.configure(
        state=tk.DISABLED
    )

    hint_button.configure(
        state=tk.DISABLED
    )

    if winner == "DRAW":

        result = (
            "🤝 TOURNAMENT DRAW!\n\n"
            f"{player1_name}: {player1_wins} wins\n"
            f"{player2_name}: {player2_wins} wins"
        )

    else:

        result = (
            f"🏆 TOURNAMENT CHAMPION!\n\n"
            f"{winner}\n\n"
            f"{player1_name}: {player1_wins} wins\n"
            f"{player2_name}: {player2_wins} wins"
        )

        update_player_record(
            winner,
            won=True,
            score=(
                player1_score
                if winner == player1_name
                else player2_score
            )
        )

    result_label.configure(
        text=result,
        fg="#ffd700"
    )

    update_game_information()

    save_leaderboard()

    update_leaderboard()

    messagebox.showinfo(
        "🏆 TOURNAMENT COMPLETE",
        result
    )


# =========================================================
# GAME OVER
# =========================================================

def game_over(reason):

    global timer_running
    global round_active

    timer_running = False
    round_active = False

    if game_mode == "Single Player":

        update_player_record(
            player1_name,
            won=False,
            score=player1_score
        )

    else:

        if current_player == 1:

            update_player_record(
                player1_name,
                won=False,
                score=player1_score
            )

        else:

            update_player_record(
                player2_name,
                won=False,
                score=player2_score
            )

    guess_entry.configure(
        state=tk.DISABLED
    )

    guess_button.configure(
        state=tk.DISABLED
    )

    hint_button.configure(
        state=tk.DISABLED
    )

    result_label.configure(
        text=(
            f"{reason}\n"
            f"The number was {secret_number}"
        ),
        fg="#ff5555"
    )

    update_game_information()

    save_leaderboard()

    update_leaderboard()

    messagebox.showinfo(
        "Game Over",
        (
            f"{reason}\n\n"
            f"Correct number: {secret_number}"
        )
    )


# =========================================================
# LEADERBOARD
# =========================================================

def update_leaderboard():

    if not leaderboard:

        leaderboard_text.configure(
            text="No players yet."
        )

        return

    sorted_players = sorted(
        leaderboard.items(),
        key=lambda item: (
            item[1]["wins"],
            item[1]["best_score"],
            item[1]["best_streak"]
        ),
        reverse=True
    )

    output = ""

    for index, (name, data) in enumerate(
        sorted_players[:10],
        start=1
    ):

        games = data["games"]

        if games > 0:

            win_rate = (
                data["wins"]
                / games
                * 100
            )

        else:

            win_rate = 0

        if index == 1:
            medal = "🥇"

        elif index == 2:
            medal = "🥈"

        elif index == 3:
            medal = "🥉"

        else:
            medal = f"{index}."

        output += (
            f"{medal} {name}\n"
            f"   Wins: {data['wins']} | "
            f"Games: {games} | "
            f"Win Rate: {win_rate:.0f}% | "
            f"Best: {data['best_score']}\n\n"
        )

    leaderboard_text.configure(
        text=output
    )


# =========================================================
# RESET LEADERBOARD
# =========================================================

def reset_leaderboard():

    global leaderboard

    answer = messagebox.askyesno(
        "Reset Leaderboard",
        "Delete all leaderboard data?"
    )

    if not answer:
        return

    leaderboard = {}

    save_leaderboard()

    update_leaderboard()

    messagebox.showinfo(
        "Reset",
        "Leaderboard has been cleared."
    )


# =========================================================
# EXIT
# =========================================================

def exit_game():

    save_leaderboard()

    root.destroy()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Number Guessing Game - V23"
)

root.geometry(
    "760x940"
)

root.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="🎯 NUMBER GUESSING GAME",
    font=("Arial", 27, "bold")
)

title_label.pack(
    pady=(18, 2)
)


subtitle_label = tk.Label(
    root,
    text="V23 • LEADERBOARD & TOURNAMENT EDITION",
    font=("Arial", 11, "bold"),
    fg="#00bfff"
)

subtitle_label.pack(
    pady=(0, 10)
)


# =========================================================
# MODE
# =========================================================

mode_label = tk.Label(
    root,
    text="🎮 GAME MODE",
    font=("Arial", 11, "bold")
)

mode_label.pack()


mode_variable = tk.StringVar(
    value=game_mode
)

mode_menu = tk.OptionMenu(
    root,
    mode_variable,
    "Single Player",
    "Two Player",
    "Tournament",
    command=change_mode
)

mode_menu.configure(
    width=17,
    font=("Arial", 10, "bold")
)

mode_menu.pack(
    pady=4
)


# =========================================================
# PLAYER NAMES
# =========================================================

names_frame = tk.Frame(
    root
)

names_frame.pack(
    pady=4
)


player1_entry = tk.Entry(
    names_frame,
    width=17,
    font=("Arial", 10)
)

player1_entry.grid(
    row=0,
    column=0,
    padx=4
)

player1_entry.insert(
    0,
    "Player 1"
)


player2_entry = tk.Entry(
    names_frame,
    width=17,
    font=("Arial", 10)
)

player2_entry.grid(
    row=0,
    column=1,
    padx=4
)

player2_entry.insert(
    0,
    "Player 2"
)

player2_entry.configure(
    state=tk.DISABLED
)


set_names_button = tk.Button(
    names_frame,
    text="SET NAMES",
    font=("Arial", 9, "bold"),
    command=set_names,
    bg="#008cff",
    fg="white",
    bd=0
)

set_names_button.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=4
)


# =========================================================
# DIFFICULTY
# =========================================================

difficulty_label = tk.Label(
    root,
    text="🎚️ DIFFICULTY",
    font=("Arial", 11, "bold")
)

difficulty_label.pack()


difficulty_variable = tk.StringVar(
    value=difficulty
)

difficulty_menu = tk.OptionMenu(
    root,
    difficulty_variable,
    *DIFFICULTIES.keys(),
    command=change_difficulty
)

difficulty_menu.configure(
    width=17,
    font=("Arial", 10, "bold")
)

difficulty_menu.pack(
    pady=4
)


# =========================================================
# TOURNAMENT SETTINGS
# =========================================================

tournament_frame = tk.Frame(
    root
)

tk.Label(
    tournament_frame,
    text="🏆 ROUNDS",
    font=("Arial", 10, "bold")
).pack(
    side=tk.LEFT,
    padx=4
)

tournament_variable = tk.StringVar(
    value="3"
)

tournament_menu = tk.OptionMenu(
    tournament_frame,
    tournament_variable,
    "3",
    "5",
    command=change_tournament_length
)

tournament_menu.configure(
    width=8,
    font=("Arial", 9, "bold")
)

tournament_menu.pack(
    side=tk.LEFT
)

tournament_frame.pack_forget()


# =========================================================
# RANGE
# =========================================================

range_frame = tk.Frame(
    root,
    padx=20,
    pady=7
)

range_frame.pack(
    pady=5
)


range_label = tk.Label(
    range_frame,
    text="Guess a number between 1 and 100",
    font=("Arial", 12, "bold")
)

range_label.pack()


# =========================================================
# PLAYER TURN
# =========================================================

player_turn_label = tk.Label(
    root,
    text="👤 PLAYER 1'S TURN",
    font=("Arial", 13, "bold")
)

player_turn_label.pack(
    pady=4
)


# =========================================================
# ROUND
# =========================================================

round_label = tk.Label(
    root,
    text="🎮 SINGLE PLAYER",
    font=("Arial", 11, "bold"),
    fg="#00bfff"
)

round_label.pack(
    pady=2
)


# =========================================================
# GUESS ENTRY
# =========================================================

guess_entry = tk.Entry(
    root,
    font=("Arial", 21, "bold"),
    justify="center",
    width=10
)

guess_entry.pack(
    pady=6
)


# =========================================================
# GUESS BUTTON
# =========================================================

guess_button = tk.Button(
    root,
    text="🎯 GUESS",
    font=("Arial", 11, "bold"),
    width=17,
    height=2,
    command=check_guess,
    bg="#008cff",
    fg="white",
    bd=0
)

guess_button.pack(
    pady=3
)


# =========================================================
# HINT BUTTON
# =========================================================

hint_button = tk.Button(
    root,
    text="💡 USE HINT",
    font=("Arial", 10, "bold"),
    width=17,
    height=2,
    command=use_hint,
    bg="#6f42c1",
    fg="white",
    bd=0
)

hint_button.pack(
    pady=3
)


# =========================================================
# RESULT
# =========================================================

result_label = tk.Label(
    root,
    text="🤔 A secret number has been generated.",
    font=("Arial", 13, "bold"),
    justify="center"
)

result_label.pack(
    pady=8
)


# =========================================================
# SCORE
# =========================================================

score_label = tk.Label(
    root,
    text="🏆 Score: 200",
    font=("Arial", 11, "bold"),
    fg="#ffd700"
)

score_label.pack(
    pady=1
)


# =========================================================
# ATTEMPTS
# =========================================================

attempts_label = tk.Label(
    root,
    text="🎯 Attempts: 0/10",
    font=("Arial", 11, "bold")
)

attempts_label.pack(
    pady=1
)


# =========================================================
# TIMER
# =========================================================

timer_label = tk.Label(
    root,
    text="⏱️ Time: 60s",
    font=("Arial", 11, "bold")
)

timer_label.pack(
    pady=1
)


# =========================================================
# STREAK
# =========================================================

streak_label = tk.Label(
    root,
    text="🔥 Streak: 0",
    font=("Arial", 11, "bold")
)

streak_label.pack(
    pady=1
)


# =========================================================
# LEADERBOARD
# =========================================================

leaderboard_frame = tk.Frame(
    root,
    padx=15,
    pady=7
)

leaderboard_frame.pack(
    pady=7
)


leaderboard_title = tk.Label(
    leaderboard_frame,
    text="🏆 LEADERBOARD",
    font=("Arial", 11, "bold")
)

leaderboard_title.pack()


leaderboard_text = tk.Label(
    leaderboard_frame,
    text="No players yet.",
    font=("Arial", 8, "bold"),
    justify="left"
)

leaderboard_text.pack(
    pady=3
)


# =========================================================
# CONTROL BUTTONS
# =========================================================

control_frame = tk.Frame(
    root
)

control_frame.pack(
    pady=5
)


new_game_button = tk.Button(
    control_frame,
    text="🔄 NEW GAME",
    font=("Arial", 9, "bold"),
    width=12,
    height=2,
    command=new_game,
    bg="#28a745",
    fg="white",
    bd=0
)

new_game_button.grid(
    row=0,
    column=0,
    padx=2
)


theme_button = tk.Button(
    control_frame,
    text="🌓 THEME",
    font=("Arial", 9, "bold"),
    width=12,
    height=2,
    command=toggle_theme,
    bg="#6f42c1",
    fg="white",
    bd=0
)

theme_button.grid(
    row=0,
    column=1,
    padx=2
)


reset_button = tk.Button(
    control_frame,
    text="🗑️ RESET",
    font=("Arial", 9, "bold"),
    width=12,
    height=2,
    command=reset_leaderboard,
    bg="#fd7e14",
    fg="white",
    bd=0
)

reset_button.grid(
    row=0,
    column=2,
    padx=2
)


# =========================================================
# EXIT
# =========================================================

exit_button = tk.Button(
    root,
    text="❌ EXIT",
    font=("Arial", 9, "bold"),
    width=12,
    command=exit_game,
    bg="#dc3545",
    fg="white",
    bd=0
)

exit_button.pack(
    pady=3
)


# =========================================================
# FOOTER
# =========================================================

footer_label = tk.Label(
    root,
    text="Python • Tkinter • JSON • V23",
    font=("Arial", 8),
    fg="#888888"
)

footer_label.pack(
    side="bottom",
    pady=5
)


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: check_guess()
)


# =========================================================
# INITIALIZE
# =========================================================

load_leaderboard()

apply_theme()

update_leaderboard()

new_game()


# =========================================================
# START
# =========================================================

root.mainloop()
