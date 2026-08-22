import tkinter as tk
from tkinter import messagebox
import json
import os


TASKS_FILE = "tasks.json"


# -----------------------------
# Data Management
# -----------------------------

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# -----------------------------
# Dashboard
# -----------------------------

def update_dashboard():
    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending = total - completed

    high_priority = sum(
        1 for task in tasks
        if task.get("priority", "Medium") == "High"
        and not task["completed"]
    )

    stats_label.config(
        text=(
            f"Total: {total}    "
            f"Pending: {pending}    "
            f"Completed: {completed}    "
            f"High Priority: {high_priority}"
        )
    )


# -----------------------------
# Display Tasks
# -----------------------------

def refresh_tasks():
    task_list.delete(0, tk.END)

    search_text = search_var.get().lower()
    selected_filter = filter_var.get()

    for index, task in enumerate(tasks):

        title = task["title"]
        completed = task["completed"]
        priority = task.get("priority", "Medium")

        # Search filter
        if search_text not in title.lower():
            continue

        # Status filter
        if selected_filter == "Pending" and completed:
            continue

        if selected_filter == "Completed" and not completed:
            continue

        if completed:
            status = "✓"
        else:
            status = "☐"

        display_text = (
            f"{status}  {title}  "
            f"[{priority}]"
        )

        task_list.insert(
            tk.END,
            display_text
        )

    update_dashboard()


# -----------------------------
# Add Task
# -----------------------------

def add_task():
    title = task_entry.get().strip()

    if not title:
        messagebox.showwarning(
            "Empty Task",
            "Please enter a task."
        )
        return

    priority = priority_var.get()

    tasks.append({
        "title": title,
        "completed": False,
        "priority": priority
    })

    save_tasks()

    task_entry.delete(0, tk.END)

    refresh_tasks()


# -----------------------------
# Get Selected Task
# -----------------------------

def get_selected_task():

    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a task first."
        )
        return None

    display_index = selected[0]

    search_text = search_var.get().lower()
    selected_filter = filter_var.get()

    visible_tasks = []

    for index, task in enumerate(tasks):

        title = task["title"]
        completed = task["completed"]

        if search_text not in title.lower():
            continue

        if selected_filter == "Pending" and completed:
            continue

        if selected_filter == "Completed" and not completed:
            continue

        visible_tasks.append(index)

    if display_index >= len(visible_tasks):
        return None

    return visible_tasks[display_index]


# -----------------------------
# Complete Task
# -----------------------------

def complete_task():

    index = get_selected_task()

    if index is None:
        return

    tasks[index]["completed"] = True

    save_tasks()

    refresh_tasks()


# -----------------------------
# Delete Task
# -----------------------------

def delete_task():

    index = get_selected_task()

    if index is None:
        return

    task_name = tasks[index]["title"]

    confirmation = messagebox.askyesno(
        "Delete Task",
        f"Delete '{task_name}'?"
    )

    if confirmation:

        tasks.pop(index)

        save_tasks()

        refresh_tasks()


# -----------------------------
# Edit Task
# -----------------------------

def edit_task():

    index = get_selected_task()

    if index is None:
        return

    old_title = tasks[index]["title"]

    edit_window = tk.Toplevel(root)

    edit_window.title("Edit Task")
    edit_window.geometry("400x220")

    edit_window.resizable(False, False)

    tk.Label(
        edit_window,
        text="Edit Task",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    edit_entry = tk.Entry(
        edit_window,
        font=("Arial", 12),
        width=35
    )

    edit_entry.insert(0, old_title)

    edit_entry.pack(pady=10)

    def save_edit():

        new_title = edit_entry.get().strip()

        if not new_title:
            messagebox.showwarning(
                "Empty Task",
                "Task cannot be empty."
            )
            return

        tasks[index]["title"] = new_title

        save_tasks()

        refresh_tasks()

        edit_window.destroy()

    tk.Button(
        edit_window,
        text="Save Changes",
        command=save_edit,
        width=20
    ).pack(pady=10)


# -----------------------------
# Clear Completed
# -----------------------------

def clear_completed():

    global tasks

    tasks = [
        task
        for task in tasks
        if not task["completed"]
    ]

    save_tasks()

    refresh_tasks()


# -----------------------------
# Search
# -----------------------------

def search_tasks(*args):

    refresh_tasks()


# -----------------------------
# Main Window
# -----------------------------

tasks = load_tasks()

root = tk.Tk()

root.title("Professional To-Do List")

root.geometry("750x750")

root.resizable(False, False)


# -----------------------------
# Header
# -----------------------------

title_label = tk.Label(
    root,
    text="📝 Professional To-Do List",
    font=("Arial", 25, "bold")
)

title_label.pack(pady=(20, 5))


subtitle_label = tk.Label(
    root,
    text="Organize your tasks and stay productive",
    font=("Arial", 11)
)

subtitle_label.pack()


# -----------------------------
# Add Task Section
# -----------------------------

add_frame = tk.LabelFrame(
    root,
    text="Add New Task",
    padx=15,
    pady=15
)

add_frame.pack(
    padx=35,
    pady=15,
    fill="x"
)


task_entry = tk.Entry(
    add_frame,
    font=("Arial", 12)
)

task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


priority_var = tk.StringVar(
    value="Medium"
)

priority_menu = tk.OptionMenu(
    add_frame,
    priority_var,
    "Low",
    "Medium",
    "High"
)

priority_menu.pack(
    side="left",
    padx=5
)


tk.Button(
    add_frame,
    text="➕ Add",
    command=add_task,
    width=10
).pack(
    side="right",
    padx=5
)


# -----------------------------
# Search
# -----------------------------

search_frame = tk.Frame(root)

search_frame.pack(
    padx=35,
    pady=5,
    fill="x"
)


tk.Label(
    search_frame,
    text="🔍 Search:"
).pack(side="left")


search_var = tk.StringVar()

search_var.trace_add(
    "write",
    search_tasks
)


search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 11)
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10
)


# -----------------------------
# Filter
# -----------------------------

filter_var = tk.StringVar(
    value="All"
)


tk.Label(
    search_frame,
    text="Filter:"
).pack(side="left")


filter_menu = tk.OptionMenu(
    search_frame,
    filter_var,
    "All",
    "Pending",
    "Completed",
    command=lambda _: refresh_tasks()
)

filter_menu.pack(side="left")


# -----------------------------
# Task List
# -----------------------------

list_frame = tk.LabelFrame(
    root,
    text="Tasks",
    padx=10,
    pady=10
)

list_frame.pack(
    padx=35,
    pady=10,
    fill="both",
    expand=True
)


task_list = tk.Listbox(
    list_frame,
    font=("Arial", 12),
    height=18,
    selectmode=tk.SINGLE
)

task_list.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = tk.Scrollbar(
    list_frame,
    command=task_list.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


task_list.config(
    yscrollcommand=scrollbar.set
)


# -----------------------------
# Action Buttons
# -----------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="✓ Complete",
    command=complete_task,
    width=13
).grid(row=0, column=0, padx=4)


tk.Button(
    button_frame,
    text="✏ Edit",
    command=edit_task,
    width=13
).grid(row=0, column=1, padx=4)


tk.Button(
    button_frame,
    text="🗑 Delete",
    command=delete_task,
    width=13
).grid(row=0, column=2, padx=4)


tk.Button(
    button_frame,
    text="Clear Completed",
    command=clear_completed,
    width=15
).grid(row=0, column=3, padx=4)


# -----------------------------
# Dashboard
# -----------------------------

stats_label = tk.Label(
    root,
    text="Total: 0    Pending: 0    Completed: 0    High Priority: 0",
    font=("Arial", 11, "bold")
)

stats_label.pack(pady=15)


# -----------------------------
# Start Application
# -----------------------------

refresh_tasks()

root.mainloop()
