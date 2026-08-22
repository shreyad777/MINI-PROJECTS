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

# Version 2 — Persistent Storage

## JSON Storage

Version 2 introduces persistent storage using a JSON file.

The file is:

```text
tasks.json

# Version 3 — Professional GUI

## Introduction

Version 3 introduces a graphical user interface using Python's Tkinter library.

The GUI provides a more convenient way to manage tasks compared to the command-line interface.

## GUI Components

The application contains:

- Task entry field
- Add button
- Priority selection
- Search field
- Filter menu
- Task list
- Complete button
- Edit button
- Delete button
- Clear Completed button
- Statistics dashboard

## Priority Management

Each task contains a priority value:

```text
Low
Medium
High
