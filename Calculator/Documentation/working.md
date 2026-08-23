# Calculator — Working Principle

## Version 1

The first version implemented four basic arithmetic operations:

- Addition
- Subtraction
- Multiplication
- Division

The program used separate functions for each operation.

## Version 2 — Advanced Calculator

Version 2 extends the calculator with additional mathematical operations and calculation history.

## Mathematical Operations

### Addition

```text
a + b
Subtraction
a - b
Multiplication
a × b
Division
a ÷ b

Division by zero is prevented.

Modulus

Returns the remainder:

17 % 5 = 2
Power

Raises one number to another:

2 ^ 5 = 32

Python implements this using:

a ** b
Floor Division

Returns the floor value of the division:

17 // 5 = 3
Square Root

The math.sqrt() function is used:

math.sqrt(number)

Negative values are rejected because their square roots are not real numbers.

Percentage

The calculator calculates:

a% of b

using:

(a / 100) * b
Absolute Value

The abs() function returns the positive magnitude of a number.

Example:

|-25| = 25
Calculation History

The program stores calculations in a Python list:

history = []

After every successful calculation, the operation is added to the list.

The History option displays all calculations performed during the current session.

Error Handling

The application handles:

Invalid numbers
try:
    number = float(input())
except ValueError:
    print("Please enter a valid number.")
Division by zero
if b == 0:
    return "Error: Cannot divide by zero."
Negative square root
if a < 0:
    return "Error: Cannot calculate square root of a negative number."
Program Flow
START
  │
  ▼
Display Menu
  │
  ▼
Select Operation
  │
  ├── Basic Operation
  │
  ├── Advanced Operation
  │
  └── History
  │
  ▼
Validate Input
  │
  ▼
Perform Calculation
  │
  ▼
Display Result
  │
  ▼
Store in History
  │
  ▼
Return to Menu
  │
  ▼
EXIT
Technologies
Python
Math module
Functions
Lists
Loops
Conditional statements
Exception handling