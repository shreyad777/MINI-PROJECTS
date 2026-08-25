import random


def choose_difficulty():
    print("\nChoose Difficulty")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:

        choice = input("Enter your choice: ")

        if choice == "1":
            return 1, 50

        elif choice == "2":
            return 1, 100

        elif choice == "3":
            return 1, 200

        else:
            print("Please choose 1, 2, or 3.")


def calculate_score(attempts, max_attempts):

    score = max_attempts - attempts + 1

    if score < 1:
        score = 1

    return score


def play_game():

    print("\n==============================")
    print("      NUMBER GUESSING GAME")
    print("==============================")

    print("\nSelect a difficulty level.")

    minimum, maximum = choose_difficulty()

    number = random.randint(
        minimum,
        maximum
    )

    max_attempts = 10

    attempts = 0

    print(
        f"\nI have selected a number between "
        f"{minimum} and {maximum}."
    )

    print(
        f"You have {max_attempts} attempts."
    )

    while attempts < max_attempts:

        try:

            guess = int(
                input(
                    f"\nAttempt {attempts + 1}: "
                )
            )

        except ValueError:

            print(
                "Please enter a valid number."
            )

            continue

        if guess < minimum or guess > maximum:

            print(
                f"Enter a number between "
                f"{minimum} and {maximum}."
            )

            continue

        attempts += 1

        if guess < number:

            print("Too low! Try again.")

        elif guess > number:

            print("Too high! Try again.")

        else:

            score = calculate_score(
                attempts,
                max_attempts
            )

            print("\n🎉 Congratulations!")

            print(
                f"You guessed the number "
                f"in {attempts} attempts."
            )

            print(
                f"Your score: {score}"
            )

            return

    print("\n❌ Game Over!")

    print(
        f"The correct number was {number}."
    )


def main():

    while True:

        play_game()

        print("\n------------------------------")

        play_again = input(
            "Do you want to play again? (y/n): "
        ).lower()

        if play_again != "y":

            print("\nThanks for playing! 👋")

            break


if __name__ == "__main__":
    main()
