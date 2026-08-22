import tkinter as tk
from tkinter import messagebox
import secrets
import string


def generate_password():
    try:
        length = int(length_var.get())

        if length < 4 or length > 100:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 4 and 100."
            )
            return

        characters = ""

        if uppercase_var.get():
            characters += string.ascii_uppercase

        if lowercase_var.get():
            characters += string.ascii_lowercase

        if numbers_var.get():
            characters += string.digits

        if special_var.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror(
                "No Character Type",
                "Select at least one character type."
            )
            return

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        password_var.set(password)

        update_strength(password)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


def copy_password():
    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


def clear_password():
    password_var.set("")
    strength_var.set("Strength: -")


def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        show_button.config(text="Show")
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")


def update_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        strength_var.set("Strength: Weak")
        strength_bar.config(width=80)

    elif score <= 4:
        strength_var.set("Strength: Medium")
        strength_bar.config(width=160)

    else:
        strength_var.set("Strength: Strong")
        strength_bar.config(width=240)


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("Professional Password Generator")
root.geometry("620x650")
root.resizable(False, False)


# -----------------------------
# Variables
# -----------------------------

length_var = tk.StringVar(value="16")
password_var = tk.StringVar()
strength_var = tk.StringVar(value="Strength: -")

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(
    root,
    padx=20,
    pady=20
)

header.pack(fill="x")

title = tk.Label(
    header,
    text="🔐 Password Generator",
    font=("Arial", 24, "bold")
)

title.pack()

subtitle = tk.Label(
    header,
    text="Create strong and secure passwords instantly",
    font=("Arial", 11)
)

subtitle.pack(pady=5)


# -----------------------------
# Length
# -----------------------------

length_frame = tk.LabelFrame(
    root,
    text="Password Length",
    padx=20,
    pady=15
)

length_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)

length_entry = tk.Entry(
    length_frame,
    textvariable=length_var,
    font=("Arial", 14),
    justify="center"
)

length_entry.pack()


# -----------------------------
# Character Options
# -----------------------------

options_frame = tk.LabelFrame(
    root,
    text="Character Options",
    padx=20,
    pady=15
)

options_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Checkbutton(
    options_frame,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
).pack(anchor="w", pady=3)


tk.Checkbutton(
    options_frame,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
).pack(anchor="w", pady=3)


tk.Checkbutton(
    options_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
).pack(anchor="w", pady=3)


tk.Checkbutton(
    options_frame,
    text="Special Characters (!@#$...)",
    variable=special_var,
    font=("Arial", 11)
).pack(anchor="w", pady=3)


# -----------------------------
# Generate Button
# -----------------------------

generate_button = tk.Button(
    root,
    text="🔑 Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10
)

generate_button.pack(pady=15)


# -----------------------------
# Password Display
# -----------------------------

password_frame = tk.LabelFrame(
    root,
    text="Generated Password",
    padx=15,
    pady=15
)

password_frame.pack(
    padx=40,
    pady=5,
    fill="x"
)

password_entry = tk.Entry(
    password_frame,
    textvariable=password_var,
    font=("Consolas", 13),
    justify="center",
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True
)


show_button = tk.Button(
    password_frame,
    text="Show",
    command=toggle_password,
    width=8
)

show_button.pack(
    side="right",
    padx=(10, 0)
)


# -----------------------------
# Action Buttons
# -----------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


copy_button = tk.Button(
    button_frame,
    text="📋 Copy",
    command=copy_password,
    width=15,
    padx=10,
    pady=7
)

copy_button.pack(
    side="left",
    padx=5
)


clear_button = tk.Button(
    button_frame,
    text="✖ Clear",
    command=clear_password,
    width=15,
    padx=10,
    pady=7
)

clear_button.pack(
    side="left",
    padx=5
)


# -----------------------------
# Strength
# -----------------------------

strength_label = tk.Label(
    root,
    textvariable=strength_var,
    font=("Arial", 12, "bold")
)

strength_label.pack(pady=5)


strength_bar = tk.Frame(
    root,
    width=240,
    height=8,
    relief="solid",
    borderwidth=1
)

strength_bar.pack()

strength_bar.pack_propagate(False)


# -----------------------------
# Footer
# -----------------------------

footer = tk.Label(
    root,
    text="Generated using Python secrets module",
    font=("Arial", 9)
)

footer.pack(pady=20)


root.mainloop()