import tkinter as tk
from tkinter import messagebox, filedialog
import secrets
import string
import math


def get_characters():
    characters = ""

    if uppercase_var.get():
        characters += string.ascii_uppercase

    if lowercase_var.get():
        characters += string.ascii_lowercase

    if numbers_var.get():
        characters += string.digits

    if special_var.get():
        characters += string.punctuation

    return characters


def generate_single_password(length, characters):
    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def generate_password():
    try:
        length = int(length_var.get())

        if length < 4 or length > 100:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 4 and 100."
            )
            return

        characters = get_characters()

        if not characters:
            messagebox.showerror(
                "No Character Type",
                "Select at least one character type."
            )
            return

        password = generate_single_password(length, characters)

        password_var.set(password)
        update_strength(password, characters)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


def generate_multiple_passwords():
    try:
        length = int(length_var.get())
        count = int(count_var.get())

        if length < 4 or length > 100:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 4 and 100."
            )
            return

        if count < 1 or count > 20:
            messagebox.showerror(
                "Invalid Count",
                "Generate between 1 and 20 passwords."
            )
            return

        characters = get_characters()

        if not characters:
            messagebox.showerror(
                "No Character Type",
                "Select at least one character type."
            )
            return

        multiple_output.delete("1.0", tk.END)

        passwords = []

        for _ in range(count):
            password = generate_single_password(
                length,
                characters
            )

            passwords.append(password)

        for index, password in enumerate(passwords, start=1):
            multiple_output.insert(
                tk.END,
                f"{index}. {password}\n"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid numeric values."
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
    entropy_var.set("Estimated Entropy: - bits")

    multiple_output.delete("1.0", tk.END)


def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        show_button.config(text="Show")
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")


def update_strength(password, characters):
    pool_size = len(characters)
    entropy = len(password) * math.log2(pool_size)

    entropy_var.set(
        f"Estimated Entropy: {entropy:.1f} bits"
    )

    if entropy < 40:
        strength = "Strength: Weak"
        bar_length = 70

    elif entropy < 60:
        strength = "Strength: Fair"
        bar_length = 120

    elif entropy < 80:
        strength = "Strength: Strong"
        bar_length = 180

    else:
        strength = "Strength: Very Strong"
        bar_length = 250

    strength_var.set(strength)
    strength_bar.config(width=bar_length)


def save_passwords():
    password = password_var.get()
    multiple_passwords = multiple_output.get(
        "1.0",
        tk.END
    ).strip()

    if not password and not multiple_passwords:
        messagebox.showwarning(
            "Nothing to Save",
            "Generate a password first."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ],
        title="Save Passwords"
    )

    if not file_path:
        return

    try:
        with open(file_path, "w") as file:

            file.write("PASSWORD GENERATOR OUTPUT\n")
            file.write("=" * 40 + "\n\n")

            if password:
                file.write(
                    f"Generated Password:\n{password}\n\n"
                )

            if multiple_passwords:
                file.write(
                    "Multiple Generated Passwords:\n"
                )
                file.write(
                    multiple_passwords + "\n"
                )

        messagebox.showinfo(
            "Saved",
            "Passwords saved successfully."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not save file:\n{error}"
        )


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("Advanced Password Generator")
root.geometry("700x850")
root.resizable(False, False)


# -----------------------------
# Variables
# -----------------------------

length_var = tk.StringVar(value="16")
count_var = tk.StringVar(value="5")

password_var = tk.StringVar()

strength_var = tk.StringVar(
    value="Strength: -"
)

entropy_var = tk.StringVar(
    value="Estimated Entropy: - bits"
)

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(root, padx=20, pady=15)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🔐 Advanced Password Generator",
    font=("Arial", 22, "bold")
)

title.pack()

subtitle = tk.Label(
    header,
    text="Generate secure passwords with strength analysis",
    font=("Arial", 10)
)

subtitle.pack(pady=3)


# -----------------------------
# Settings
# -----------------------------

settings_frame = tk.LabelFrame(
    root,
    text="Password Settings",
    padx=20,
    pady=10
)

settings_frame.pack(
    padx=40,
    pady=8,
    fill="x"
)


tk.Label(
    settings_frame,
    text="Password Length:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)

length_entry = tk.Entry(
    settings_frame,
    textvariable=length_var,
    width=10,
    justify="center"
)

length_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Label(
    settings_frame,
    text="Number of Passwords:"
).grid(
    row=0,
    column=2,
    padx=10
)

count_entry = tk.Entry(
    settings_frame,
    textvariable=count_var,
    width=10,
    justify="center"
)

count_entry.grid(
    row=0,
    column=3,
    padx=10
)


# -----------------------------
# Character Options
# -----------------------------

options_frame = tk.LabelFrame(
    root,
    text="Character Options",
    padx=20,
    pady=10
)

options_frame.pack(
    padx=40,
    pady=8,
    fill="x"
)


tk.Checkbutton(
    options_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var
).grid(row=0, column=0, padx=10, pady=5)


tk.Checkbutton(
    options_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var
).grid(row=0, column=1, padx=10, pady=5)


tk.Checkbutton(
    options_frame,
    text="Numbers (0-9)",
    variable=numbers_var
).grid(row=1, column=0, padx=10, pady=5)


tk.Checkbutton(
    options_frame,
    text="Special Characters",
    variable=special_var
).grid(row=1, column=1, padx=10, pady=5)


# -----------------------------
# Single Password
# -----------------------------

single_frame = tk.LabelFrame(
    root,
    text="Generate Single Password",
    padx=15,
    pady=15
)

single_frame.pack(
    padx=40,
    pady=8,
    fill="x"
)


tk.Button(
    single_frame,
    text="🔑 Generate Password",
    command=generate_password,
    width=25
).pack(pady=5)


password_display_frame = tk.Frame(single_frame)
password_display_frame.pack(
    fill="x",
    pady=10
)


password_entry = tk.Entry(
    password_display_frame,
    textvariable=password_var,
    font=("Consolas", 12),
    justify="center",
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True
)


show_button = tk.Button(
    password_display_frame,
    text="Show",
    command=toggle_password,
    width=8
)

show_button.pack(
    side="right",
    padx=5
)


tk.Label(
    single_frame,
    textvariable=strength_var,
    font=("Arial", 11, "bold")
).pack()


strength_bar = tk.Frame(
    single_frame,
    width=0,
    height=8,
    relief="solid",
    borderwidth=1
)

strength_bar.pack(pady=5)
strength_bar.pack_propagate(False)


tk.Label(
    single_frame,
    textvariable=entropy_var
).pack()


# -----------------------------
# Action Buttons
# -----------------------------

action_frame = tk.Frame(single_frame)
action_frame.pack(pady=10)


tk.Button(
    action_frame,
    text="📋 Copy",
    command=copy_password,
    width=12
).pack(side="left", padx=5)


tk.Button(
    action_frame,
    text="💾 Save",
    command=save_passwords,
    width=12
).pack(side="left", padx=5)


tk.Button(
    action_frame,
    text="✖ Clear",
    command=clear_password,
    width=12
).pack(side="left", padx=5)


# -----------------------------
# Multiple Passwords
# -----------------------------

multiple_frame = tk.LabelFrame(
    root,
    text="Generate Multiple Passwords",
    padx=15,
    pady=10
)

multiple_frame.pack(
    padx=40,
    pady=8,
    fill="both",
    expand=True
)


tk.Button(
    multiple_frame,
    text="🎲 Generate Multiple Passwords",
    command=generate_multiple_passwords
).pack(pady=5)


multiple_output = tk.Text(
    multiple_frame,
    height=10,
    font=("Consolas", 11)
)

multiple_output.pack(
    fill="both",
    expand=True,
    pady=5
)


# -----------------------------
# Footer
# -----------------------------

footer = tk.Label(
    root,
    text="Uses Python secrets module for secure random generation",
    font=("Arial", 9)
)

footer.pack(pady=10)


root.mainloop()
