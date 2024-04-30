from flask import Blueprint, render_template
from models import User, Task

html_routes_bp = Blueprint('html_routes', __name__)

"""
Routes allow you to define Flask pages in a logical and organized way
"""


@html_routes_bp.route("/")
def index():
    """Renders the home page under /templates/index.html"""
    return render_template("index.html")


@html_routes_bp.route("/tasks")
def tasks():
    """
    Renders a list of all tasks in the database using the template /templates/tasks.html
    Tasks are queried from the SQLAlchemy database using Task.query.all() and assigned to the tasks variable
    This is passed in to the template under the same variable name
    Look in templates/tasks.html to see how this works
    """
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)