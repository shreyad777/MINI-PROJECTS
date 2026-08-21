import secrets
import string


def generate_password(length, use_uppercase, use_lowercase,
                      use_numbers, use_special):

    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_special:
        characters += string.punctuation

    if not characters:
        return None

    password = ""

    for _ in range(length):
        password += secrets.choice(characters)

    return password


def main():

    print("=" * 40)
    print("       PASSWORD GENERATOR")
    print("=" * 40)

    try:
        length = int(input("Enter password length: "))

        if length < 4:
            print("Password length should be at least 4.")
            return

        uppercase = input(
            "Include uppercase letters? (y/n): "
        ).lower() == "y"

        lowercase = input(
            "Include lowercase letters? (y/n): "
        ).lower() == "y"

        numbers = input(
            "Include numbers? (y/n): "
        ).lower() == "y"

        special = input(
            "Include special characters? (y/n): "
        ).lower() == "y"

        password = generate_password(
            length,
            uppercase,
            lowercase,
            numbers,
            special
        )

        if password is None:
            print("Please select at least one character type.")
            return

        print("\nGenerated Password:", password)

    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()
