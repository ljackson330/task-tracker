## ACIT-2911 Agile Project - Task Tracker 🚀

---

This is our repo for the ACIT-2911 Agile project. We are creating a task tracker app using Flask, SQLAlchemy, and more!

### How to Run ⚙️

---

First, clone in to the repository:

```
git clone https://github.com/ljackson330/task-tracker
cd task-tracker
```

Second, ensure that all required dependencies are installed (either system-wide or in a venv - I recommend using venvs, but that might be out of scope)

```
pip install flask flask_sqlalchemy
```

Next, start the Flask server

```
python main.py
```

In a new tab/window, run `manage.py`. This script seeds the database with (currently) hard-coded User and Task objects from .csv files in `data/`

```
python manage.py
```

You will see a file `taskdatabase.db` show up.

You can now open http://127.0.0.1:8080/ and see the default home page, with a link to see all tasks in the database. Hooray ✨

---

Random things I need to write down but should eventually end up somewhere else:

- [ ] Tasks should ideally have a created_timestamp property that stores when the task was created, but I was running in to issues I didn't feel like fixing when trying to implement this
- [ ] Tasks should ideally have an optional due_date (or whatever other name) property that could be used as a due-date for whatever logic or processing we want to do
- [ ] We obviously need to eventually implement session-based authentication and restrict displayed tasks to only those which belong to the currently logged in user. This is a big, big change, though - I recommend we work on that piecemeal and flesh out some of the other functions (creating, editing, deleting tasks etc.) before looking at session auth
