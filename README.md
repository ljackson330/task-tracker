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
