tasks = []


def show_tasks():
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\n========== TASKS ==========")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "

        print(
            f"{index}. [{status}] {task['title']}"
        )


def add_task():
    title = input("\nEnter task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    tasks.append({
        "title": title,
        "completed": False
    })

    print("Task added successfully.")


def complete_task():
    show_tasks()

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

        print("Task completed.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    show_tasks()

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

        print(
            f"Deleted task: {removed['title']}"
        )

    except ValueError:
        print("Please enter a valid number.")


def main():

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
            add_task()

        elif choice == "2":
            show_tasks()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
