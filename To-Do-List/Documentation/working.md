# To-Do List — Working Principle

## 1. Introduction

The To-Do List is a command-line Python application for managing daily tasks.

The application allows the user to add tasks, view tasks, mark tasks as completed, and delete tasks.

## 2. Data Structure

Tasks are stored inside a Python list.

Each task is represented using a dictionary.

Example:

```python
{
    "title": "Study Python",
    "completed": False
}

##3. Adding Tasks

The add_task() function asks the user for a task title.

The task is then stored in the list with:

{
    "title": task_title,
    "completed": False
}
##4. Displaying Tasks

The show_tasks() function uses a loop to display every task.

A task that has not been completed is shown as:

[ ]

A completed task is shown as:

[✓]

##5. Completing Tasks

The complete_task() function asks the user to enter a task number.

The selected task's completed value is changed from:

False

to:

True
##6. Deleting Tasks

The delete_task() function uses the task number provided by the user.

The selected task is removed from the list using the pop() method.

##7. Input Validation

The program uses exception handling to prevent invalid numerical input from crashing the application.

For example:

try:
    number = int(input())
except ValueError:
    print("Please enter a valid number.")
##8. Program Flow
Start
  ↓
Display Menu
  ↓
User Selects Option
  ↓
Perform Operation
  ↓
Update Task List
  ↓
Display Result
  ↓
Return to Menu
  ↓
Exit

##9. Functions

The project contains the following main functions:

show_tasks()

Displays all tasks.

add_task()

Creates a new task.

complete_task()

Marks a task as completed.

delete_task()

Deletes a task.

main()

Controls the main application loop.

## 10. Future Development

The application can be improved by adding persistent storage, deadlines, priorities, search functionality, editing, and a graphical interface.



Commit message:


```text
Add To-Do List documentation
