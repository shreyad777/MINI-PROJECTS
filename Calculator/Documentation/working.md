# Calculator — Working Principle

## Overview

The Calculator project contains two versions:

1. Command-line calculator
2. Tkinter GUI calculator

---

# Version 1 — Basic Calculator

The first version supports:

- Addition
- Subtraction
- Multiplication
- Division

It uses functions to perform each arithmetic operation.

---

# Version 2 — Advanced Calculator

Version 2 added:

- Modulus
- Power
- Floor division
- Square root
- Percentage
- Absolute value
- Calculation history

The `math` module is used for mathematical operations such as square root.

---

# Version 3 — GUI Calculator

Version 3 introduces a graphical interface using Tkinter.

The GUI contains:

- Calculator display
- Number buttons
- Arithmetic operators
- Clear button
- Backspace button
- Square root
- Percentage
- Power
- Equals button
- Calculation history

---

## GUI Architecture

```text
                 Tkinter Window
                       │
             ┌─────────┴─────────┐
             │                   │
        Calculator            History
             │                   │
      ┌──────┴──────┐            │
      │             │            │
   Display       Buttons       History
      │             │            │
      └──────┬──────┘            │
             │                   │
             └────────┬──────────┘
                      │
                      ▼
                Calculation