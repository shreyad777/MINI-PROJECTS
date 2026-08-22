import json
import os


TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\n========== TASKS ==========")

    for index, task in enumerate(tasks, start=1):

        status = "✓" if task["completed"] else " "

        print(
            f"{index}. [{status}] {task['title']}"
        )


def add_task(tasks):

    title = input("\nEnter task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    tasks.append({
        "title": title,
        "completed": False
    })

    save_tasks(tasks)

    print("Task added successfully.")


def complete_task(tasks):

    show_tasks(tasks)

    if not tasks:
        return

    try:

        number = int(
            input("\nEnter task number to complete: ")
        )

        if number < 1 or number > len(tasks):
            print("Invalid task number.")
            return

        tasks[number - 1]["completed"] = True

        save_tasks(tasks)

        print("Task completed.")

    except ValueError:

        print("Please enter a valid number.")


def delete_task(tasks):

    show_tasks(tasks)

    if not tasks:
        return

    try:

        number = int(
            input("\nEnter task number to delete: ")
        )

        if number < 1 or number > len(tasks):
            print("Invalid task number.")
            return

        removed = tasks.pop(number - 1)

        save_tasks(tasks)

        print(
            f"Deleted task: {removed['title']}"
        )

    except ValueError:

        print("Please enter a valid number.")


def main():

    tasks = load_tasks()

    while True:

        print("\n==============================")
        print("         TO-DO LIST")
        print("==============================")

        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            add_task(tasks)

        elif choice == "2":

            show_tasks(tasks)

        elif choice == "3":

            complete_task(tasks)

        elif choice == "4":

            delete_task(tasks)

        elif choice == "5":

            print("Goodbye!")
            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    main()
