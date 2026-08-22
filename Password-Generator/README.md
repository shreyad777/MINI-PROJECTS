# 🔐 Password Generator

A simple and secure Python-based Password Generator that creates random passwords according to the user's selected requirements.

The user can choose the password length and decide whether to include uppercase letters, lowercase letters, numbers, and special characters.

## 📌 Project Overview

Creating strong and unique passwords is important for protecting online accounts and personal information.

This project automates password generation using Python. Instead of manually creating passwords, the program generates a random password based on the options selected by the user.

The project uses Python's `secrets` module for secure random password generation.

## 🎯 Objectives

* Generate random passwords automatically.
* Allow users to select the password length.
* Allow users to select different character types.
* Generate stronger passwords using a combination of characters.
* Demonstrate the use of Python functions and modules.
* Understand basic password security concepts.

## ✨ Features

* Custom password length.
* Uppercase letter support.
* Lowercase letter support.
* Number support.
* Special character support.
* Random password generation.
* Input validation.
* Secure random generation using Python's `secrets` module.
* Simple command-line interface.

## 🖥️ GUI Version
## 🖥️ Professional GUI Version

Version 3 of the project includes a professional graphical user interface built using Python Tkinter.

### GUI Features

- 🔐 Secure password generation
- 📏 Custom password length from 4 to 100 characters
- 🔤 Uppercase letter selection
- 🔡 Lowercase letter selection
- 🔢 Number selection
- 🔣 Special character selection
- 👁️ Show/Hide password
- 📋 Copy password to clipboard
- ✖ Clear generated password
- 📊 Password strength indicator
- ⚠️ Input validation

### Run the GUI

From the `Password-Generator` directory:

```bash
python password_generator_gui.py
.

## 🛠️ Technologies Used

| Technology | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| Python     | Main programming language                            |
| `secrets`  | Secure random password generation                    |
| `string`   | Provides letters, digits, and punctuation characters |

## 📂 Project Structure

```text
Password-Generator/
│
├── password_generator.py
└── README.md
```

## ⚙️ How It Works

The program first asks the user for the desired password length.

It then asks whether the user wants to include:

1. Uppercase letters
2. Lowercase letters
3. Numbers
4. Special characters

The selected character sets are combined into a single pool.

The program then uses the `secrets` module to randomly select characters from that pool and create the password.

## 🔄 Program Flow

```text
Start
  ↓
Enter Password Length
  ↓
Select Character Types
  ↓
Create Character Pool
  ↓
Generate Random Password
  ↓
Display Password
  ↓
End
```

## 💻 Example

```text
========================================
       PASSWORD GENERATOR
========================================

Enter password length: 12

Include uppercase letters? (y/n): y
Include lowercase letters? (y/n): y
Include numbers? (y/n): y
Include special characters? (y/n): y

Generated Password: K7@mP2#xQ9!a
```

The generated password will be different each time because the program uses secure random selection.

## 🧠 Concepts Used

This project demonstrates:

* Variables
* Functions
* Conditional statements
* Loops
* Exception handling
* User input
* Python modules
* String manipulation
* Random generation
* Basic security concepts


## 🔮 Future Enhancements

The project can be improved by adding:

* Password history.
* Password strength indicator.
* Option to generate multiple passwords.
* Customizable special-character selection.
* Password generation history export.
* Dark/light GUI themes.

## ⚠️ Security Note

This project is intended for educational purposes.

Generated passwords should not be stored or shared unnecessarily. For real-world password management, users should consider established password managers and security practices.

## 👩‍💻 Author

**Shreya D.**

B.E. Computer Science and Engineering (Data Science)

## 📜 License

This project is created for educational and academic purposes.


