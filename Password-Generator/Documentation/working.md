# Password Generator — Working Principle

## 1. Introduction

The Password Generator is a Python-based application that generates random passwords according to the requirements provided by the user.

The program allows the user to specify the password length and select the types of characters that should be included.

## 2. Character Types

The program can use four types of characters:

### Uppercase Letters

```text
A B C D E ... Z
```

These are obtained using:

```python
string.ascii_uppercase
```

### Lowercase Letters

```text
a b c d e ... z
```

These are obtained using:

```python
string.ascii_lowercase
```

### Numbers

```text
0 1 2 3 4 5 6 7 8 9
```

These are obtained using:

```python
string.digits
```

### Special Characters

Examples include:

```text
! @ # $ % ^ & * ( )
```

These are obtained using:

```python
string.punctuation
```

## 3. Password Generation

The program first creates a character pool based on the options selected by the user.

For example, if the user selects:

* Uppercase letters
* Lowercase letters
* Numbers
* Special characters

all four character sets are combined.

The program then uses:

```python
secrets.choice()
```

to randomly select characters from the available pool.

## 4. Why `secrets` Is Used

Python provides both `random` and `secrets` modules.

For password generation, `secrets` is preferred because it is designed for generating random values for security-sensitive applications.

## 5. Input Validation

The program checks whether the password length is valid.

If the user enters a value smaller than 4, the program displays:

```text
Password length should be at least 4.
```

The program also handles invalid numerical input using exception handling.

## 6. Program Flow

```text
Start
  ↓
Enter password length
  ↓
Select character types
  ↓
Create character pool
  ↓
Generate random characters
  ↓
Create password
  ↓
Display password
  ↓
End
```

## 7. Main Functions

### `generate_password()`

This function receives the password length and the selected character options and generates the password.

### `main()`

This function controls the main program flow, accepts user input, validates the input, and displays the generated password.

## 8. Result

The program successfully generates a random password according to the user's selected requirements.

Example:

```text
Generated Password: A7@kP2!xQ9#m
```

The generated value will change each time the program is executed.


# Advanced Features

## Password Strength

The application estimates password strength using password length and character pool size.

The approximate entropy is calculated using:

Entropy = Length × log₂(Character Pool Size)

Higher entropy indicates a larger number of possible password combinations.

## Multiple Password Generation

The application can generate between 1 and 20 passwords in a single operation.

Each password is generated independently using:

```python
secrets.choice()
