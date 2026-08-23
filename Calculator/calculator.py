import math


history = []


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero."

    return a / b


def modulus(a, b):
    if b == 0:
        return "Error: Cannot divide by zero."

    return a % b


def power(a, b):
    return a ** b


def floor_division(a, b):
    if b == 0:
        return "Error: Cannot divide by zero."

    return a // b


def square_root(a):

    if a < 0:
        return "Error: Cannot calculate square root of a negative number."

    return math.sqrt(a)


def percentage(a, b):
    return (a / 100) * b


def absolute(a):
    return abs(a)


def show_history():

    if not history:
        print("\nNo calculations yet.")
        return

    print("\n========== HISTORY ==========")

    for item in history:
        print(item)


def main():

    while True:

        print("\n==============================")
        print("      ADVANCED CALCULATOR")
        print("==============================")

        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Modulus")
        print("6. Power")
        print("7. Floor Division")
        print("8. Square Root")
        print("9. Percentage")
        print("10. Absolute Value")
        print("11. History")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "12":
            print("Goodbye!")
            break

        if choice == "11":
            show_history()
            continue

        # Single-number operation
        if choice in ["8", "10"]:

            try:
                number = float(
                    input("Enter number: ")
                )

            except ValueError:
                print("Please enter a valid number.")
                continue

            if choice == "8":

                result = square_root(number)

                calculation = (
                    f"√{number} = {result}"
                )

            else:

                result = absolute(number)

                calculation = (
                    f"|{number}| = {result}"
                )

        # Two-number operations
        elif choice in [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "9"
        ]:

            try:

                num1 = float(
                    input("Enter first number: ")
                )

                num2 = float(
                    input("Enter second number: ")
                )

            except ValueError:

                print("Please enter valid numbers.")
                continue

            if choice == "1":

                result = add(num1, num2)

                calculation = (
                    f"{num1} + {num2} = {result}"
                )

            elif choice == "2":

                result = subtract(num1, num2)

                calculation = (
                    f"{num1} - {num2} = {result}"
                )

            elif choice == "3":

                result = multiply(num1, num2)

                calculation = (
                    f"{num1} × {num2} = {result}"
                )

            elif choice == "4":

                result = divide(num1, num2)

                calculation = (
                    f"{num1} ÷ {num2} = {result}"
                )

            elif choice == "5":

                result = modulus(num1, num2)

                calculation = (
                    f"{num1} % {num2} = {result}"
                )

            elif choice == "6":

                result = power(num1, num2)

                calculation = (
                    f"{num1} ^ {num2} = {result}"
                )

            elif choice == "7":

                result = floor_division(
                    num1,
                    num2
                )

                calculation = (
                    f"{num1} // {num2} = {result}"
                )

            elif choice == "9":

                result = percentage(
                    num1,
                    num2
                )

                calculation = (
                    f"{num1}% of {num2} = {result}"
                )

        else:

            print("Invalid choice.")
            continue

        print("\nResult:", result)

        history.append(calculation)


if __name__ == "__main__":
    main()