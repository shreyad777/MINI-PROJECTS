import tkinter as tk
from tkinter import messagebox
import math


history = []


# -----------------------------
# Calculator Functions
# -----------------------------

def add_to_display(value):
    current = display_var.get()

    if current == "Error":
        current = ""

    display_var.set(current + str(value))


def clear_display():
    display_var.set("")


def delete_last():
    current = display_var.get()

    if current:
        display_var.set(current[:-1])


def calculate_result():

    expression = display_var.get()

    if not expression:
        return

    try:

        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        display_var.set(format_result(result))

        history.append(
            f"{expression} = {format_result(result)}"
        )

        update_history()

    except ZeroDivisionError:

        show_error(
            "Division by zero is not allowed."
        )

    except Exception:

        show_error(
            "Invalid calculation."
        )


def square_root():

    try:

        value = float(display_var.get())

        if value < 0:
            show_error(
                "Cannot calculate square root of a negative number."
            )
            return

        result = math.sqrt(value)

        display_var.set(
            format_result(result)
        )

        history.append(
            f"√{value} = {format_result(result)}"
        )

        update_history()

    except ValueError:

        show_error(
            "Enter a valid number first."
        )


def percentage():

    try:

        value = float(display_var.get())

        result = value / 100

        display_var.set(
            format_result(result)
        )

        history.append(
            f"{value}% = {format_result(result)}"
        )

        update_history()

    except ValueError:

        show_error(
            "Enter a valid number first."
        )


def format_result(value):

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


# -----------------------------
# Error Handling
# -----------------------------

def show_error(message):

    display_var.set("Error")

    messagebox.showerror(
        "Calculator Error",
        message
    )


# -----------------------------
# History
# -----------------------------

def update_history():

    history_list.delete(
        0,
        tk.END
    )

    for item in history:

        history_list.insert(
            tk.END,
            item
        )


def clear_history():

    history.clear()

    update_history()


# -----------------------------
# Keyboard Support
# -----------------------------

def keyboard_input(event):

    key = event.char

    if key in "0123456789.+-*/":

        add_to_display(key)

    elif key == "^":

        add_to_display("^")

    elif event.keysym == "Return":

        calculate_result()

    elif event.keysym == "BackSpace":

        delete_last()

    elif event.keysym == "Escape":

        clear_display()


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("Professional Calculator")

root.geometry("760x650")

root.resizable(False, False)


# -----------------------------
# Header
# -----------------------------

title_label = tk.Label(
    root,
    text="🧮 Calculator",
    font=("Arial", 26, "bold")
)

title_label.pack(
    pady=(20, 5)
)


subtitle_label = tk.Label(
    root,
    text="Simple and advanced calculations",
    font=("Arial", 11)
)

subtitle_label.pack()


# -----------------------------
# Display
# -----------------------------

display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Arial", 24, "bold"),
    justify="right",
    state="readonly"
)

display.pack(
    padx=35,
    pady=20,
    fill="x",
    ipady=15
)


# -----------------------------
# Main Content
# -----------------------------

main_frame = tk.Frame(root)

main_frame.pack(
    padx=35,
    fill="both",
    expand=True
)


# -----------------------------
# Calculator Buttons
# -----------------------------

button_frame = tk.Frame(main_frame)

button_frame.pack(
    side="left",
    fill="both",
    expand=True
)


buttons = [
    ("7", 0, 0),
    ("8", 0, 1),
    ("9", 0, 2),
    ("÷", 0, 3),

    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("×", 1, 3),

    ("1", 2, 0),
    ("2", 2, 1),
    ("3", 2, 2),
    ("-", 2, 3),

    ("0", 3, 0),
    (".", 3, 1),
    ("^", 3, 2),
    ("+", 3, 3),
]


for text, row, column in buttons:

    tk.Button(
        button_frame,
        text=text,
        font=("Arial", 16, "bold"),
        command=lambda value=text:
        add_to_display(value),
        width=5,
        height=2
    ).grid(
        row=row,
        column=column,
        padx=4,
        pady=4
    )


# -----------------------------
# Special Buttons
# -----------------------------

special_frame = tk.Frame(
    button_frame
)

special_frame.grid(
    row=4,
    column=0,
    columnspan=4,
    pady=8
)


tk.Button(
    special_frame,
    text="C",
    font=("Arial", 13, "bold"),
    command=clear_display,
    width=6
).grid(
    row=0,
    column=0,
    padx=3
)


tk.Button(
    special_frame,
    text="⌫",
    font=("Arial", 13, "bold"),
    command=delete_last,
    width=6
).grid(
    row=0,
    column=1,
    padx=3
)


tk.Button(
    special_frame,
    text="√",
    font=("Arial", 13, "bold"),
    command=square_root,
    width=6
).grid(
    row=0,
    column=2,
    padx=3
)


tk.Button(
    special_frame,
    text="%",
    font=("Arial", 13, "bold"),
    command=percentage,
    width=6
).grid(
    row=0,
    column=3,
    padx=3
)


tk.Button(
    button_frame,
    text="=",
    font=("Arial", 16, "bold"),
    command=calculate_result,
    width=23,
    height=2
).grid(
    row=5,
    column=0,
    columnspan=4,
    pady=5
)


# -----------------------------
# History Panel
# -----------------------------

history_frame = tk.LabelFrame(
    main_frame,
    text="Calculation History",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

history_frame.pack(
    side="right",
    fill="both",
    padx=(20, 0)
)


history_list = tk.Listbox(
    history_frame,
    width=27,
    height=18,
    font=("Arial", 10)
)

history_list.pack(
    fill="both",
    expand=True
)


tk.Button(
    history_frame,
    text="Clear History",
    command=clear_history,
    width=18
).pack(
    pady=10
)


# -----------------------------
# Keyboard Binding
# -----------------------------

root.bind(
    "<Key>",
    keyboard_input
)


# -----------------------------
# Start Application
# -----------------------------

root.mainloop()