# 📝 Professional To-Do List

A Python-based task management application with both a command-line interface and a professional graphical user interface.

The application allows users to create, manage, search, filter, edit, and complete tasks while storing the data permanently using JSON.

---

## 🎯 Project Objective

The goal of this project is to build a practical task-management application while learning:

- Python programming
- Functions
- Lists and dictionaries
- File handling
- JSON data storage
- Exception handling
- Tkinter GUI development
- CRUD operations
- Search and filtering
- Data persistence

---

## ✨ Features

### Version 1 — Command Line

- ➕ Add tasks
- 📋 View tasks
- ✅ Complete tasks
- 🗑️ Delete tasks
- ⚠️ Input validation
- 💻 Command-line interface

### Version 2 — Persistent Storage

- 💾 Save tasks automatically
- 📂 Load tasks when the application starts
- 🔄 Tasks remain after restarting the program
- 🗃️ JSON-based storage
- 🛡️ Handles missing or invalid JSON files

### Version 3 — Professional GUI

- 🖥️ Tkinter graphical interface
- ➕ Add tasks
- ✏️ Edit tasks
- ✅ Complete tasks
- 🗑️ Delete tasks
- 🧹 Clear completed tasks
- ⭐ Low / Medium / High priority
- 🔍 Search tasks
- 🔽 Filter tasks
- 📊 Task statistics dashboard
- 💾 Persistent JSON storage

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical User Interface |
| JSON | Persistent data storage |
| File Handling | Reading and writing task data |
| Git | Version control |
| GitHub | Project hosting |

---

## 📂 Project Structure

```text
To-Do-List/
│
├── todo.py
├── todo_gui.py
├── tasks.json
├── README.md
├── requirements.txt
├── .gitignore
│
└── Documentation/
    └── working.md

🖥️ Applications

The project contains two interfaces.

1. Command-Line Version

Run:

python todo.py

The command-line version provides:

1. Add Task
2. Show Tasks
3. Complete Task
4. Delete Task
5. Exit
2. GUI Version

Run:

python todo_gui.py

The GUI provides a more user-friendly task management interface.

⭐ Priority System

Each task can have one of three priority levels:

Low
Medium
High

Example:

☐ Complete project report [High]
☐ Study Python [Medium]
☐ Read documentation [Low]
🔍 Search

The GUI includes a search box that allows users to quickly find tasks.

For example, searching:

Python

will display tasks containing the word "Python".

🔽 Task Filtering

Tasks can be filtered using:

All
Pending
Completed

This makes it easier to focus on unfinished or completed tasks.

📊 Dashboard

The application displays task statistics:

Total: 10
Pending: 6
Completed: 4
High Priority: 2

The statistics are automatically updated when tasks change.

💾 Persistent Storage

Tasks are stored in:

tasks.json

Example:

[
    {
        "title": "Complete Python project",
        "completed": false,
        "priority": "High"
    },
    {
        "title": "Study Data Structures",
        "completed": true,
        "priority": "Medium"
    }
]

Because the tasks are stored in JSON, they remain available after closing and reopening the application.

🔄 Application Flow
                  START
                    │
                    ▼
              Load tasks.json
                    │
                    ▼
              Display GUI
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
        Add       Edit      Delete
          │         │         │
          └─────────┼─────────┘
                    │
                    ▼
             Update Task
                    │
                    ▼
              Save JSON
                    │
                    ▼
             Refresh GUI
                    │
                    ▼
               Continue
🚀 How to Run
Step 1 — Check Python
python --version
Step 2 — Run CLI
python todo.py
Step 3 — Run GUI
python todo_gui.py

No external Python packages are required because the project uses Python's standard library.

🧪 Example

A task can be created as:

Task: Complete mini project
Priority: High
Status: Pending

After completion:

✓ Complete mini project [High]
🔮 Future Enhancements

Possible future improvements include:

📅 Due dates
⏰ Task reminders
🔔 Notifications
📊 Graphical charts
🏷️ Task categories
📌 Task sorting
🌙 Dark mode
📤 Export tasks
☁️ Cloud synchronization
👥 Multi-user support
🔐 User authentication
📚 Learning Outcomes

Through this project, the following concepts are practiced:

Variables
Data types
Lists
Dictionaries
Functions
Loops
Conditional statements
Exception handling
File handling
JSON
Object-oriented GUI concepts
Tkinter
CRUD operations
Search
Filtering
Persistent storage
Git and GitHub
👩‍💻 Author

Shreya D.

B.E. Computer Science and Engineering (Data Science)

📜 License

This project is created for educational and academic purposes.