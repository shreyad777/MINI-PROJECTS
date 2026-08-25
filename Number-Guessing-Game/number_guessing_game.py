import random


def main():

    number = random.randint(1, 100)

    attempts = 0

    print("\n==============================")
    print("     NUMBER GUESSING GAME")
    print("==============================")

    print("I have selected a number between 1 and 100.")
    print("Try to guess it!")

    while True:

        try:

            guess = int(
                input("\nEnter your guess: ")
            )

        except ValueError:

            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < number:

            print("Too low! Try again.")

        elif guess > number:

            print("Too high! Try again.")

        else:

            print("\n🎉 Congratulations!")

            print(
                f"You guessed the number in "
                f"{attempts} attempts."
            )

            break


if __name__ == "__main__":
    main()