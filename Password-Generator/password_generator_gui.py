import tkinter as tk
from tkinter import messagebox
import secrets
import string


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 4."
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
                "Please select at least one character type."
            )
            return

        password = ""

        for _ in range(length):
            password += secrets.choice(characters)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        update_strength(password)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


def copy_password():
    password = password_entry.get()

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


def update_strength(password):
    score = 0

    if len(password) >= 8:
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
        strength_label.config(text="Strength: Weak")

    elif score <= 4:
        strength_label.config(text="Strength: Medium")

    else:
        strength_label.config(text="Strength: Strong")


root = tk.Tk()

root.title("Password Generator")
root.geometry("500x500")

title_label = tk.Label(
    root,
    text="PASSWORD GENERATOR",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


length_label = tk.Label(
    root,
    text="Password Length:"
)

length_label.pack()

length_entry = tk.Entry(
    root,
    width=25
)

length_entry.insert(0, "12")
length_entry.pack(pady=5)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)


tk.Checkbutton(
    root,
    text="Include Uppercase Letters",
    variable=uppercase_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Include Lowercase Letters",
    variable=lowercase_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Include Numbers",
    variable=numbers_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Include Special Characters",
    variable=special_var
).pack(anchor="w", padx=120)


generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    width=25
)

generate_button.pack(pady=20)


password_entry = tk.Entry(
    root,
    width=40
)

password_entry.pack(pady=5)


copy_button = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    width=25
)

copy_button.pack(pady=10)


strength_label = tk.Label(
    root,
    text="Strength: -",
    font=("Arial", 12, "bold")
)

strength_label.pack(pady=10)


root.mainloop()