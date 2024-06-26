from flask import Blueprint, render_template, request, redirect, url_for, abort
from db import db
from models import User, Task
from validationForm import RegisterForm, LoginForm
from flask_login import login_required, login_user, current_user, logout_user, logout_user
from datetime import datetime

html_routes_bp = Blueprint('html_routes', __name__)

"""
Routes allow you to define Flask pages in a logical and organized way
"""

@html_routes_bp.route("/")
def index():
    """Renders the home page under /templates/index.html"""
    tasks = Task.query.all()
    if not current_user.is_authenticated:
        return render_template("index.html", tasks=[])
    current_user_id = current_user.id
    now = datetime.now()
    user_tasks = [task for task in tasks if task.user_id == current_user_id and task.end_date]
    upcoming_task = min(user_tasks, key=lambda task: abs(task.end_date - now), default=None)
    return render_template("index.html", tasks=tasks, upcoming_task=upcoming_task)


@html_routes_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('html_routes.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
                login_user(user)
                return redirect(url_for('html_routes.dashboard'))
    return render_template("login.html", form=form, )

#NOTE @login_required just makes it so login/authentication is needed for users to access the page
@html_routes_bp.route("/logout")
@login_required
def logout():
    """Logs out the user and redirects to the login page."""
    logout_user()
    return redirect(url_for('html_routes.login'))

@html_routes_bp.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('html_routes.dashboard'))
    """Renders the register page."""
    form = RegisterForm()
    return render_template("register.html", form=form)

@html_routes_bp.route("/dashboard")
@login_required
def dashboard():
    """Renders the dashboard page."""
    return render_template("dashboard.html")

@html_routes_bp.route("/tasks")
@login_required
def tasks():
    """Renders the tasks page."""
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)

  
@html_routes_bp.route("/tasks/create", methods=["GET", "POST"])
def create_tasks():
    """
    Creates a task object using the POST request body
    """
    if request.method == "POST":
        task_title = request.form["title"]
        task_description = request.form["description"]
        db.session.add(Task(name=task_title, desc=task_description, user_id=current_user.id))
        db.session.commit()
        return redirect(url_for('html_routes.tasks'))
    return render_template("create.html")


@html_routes_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """
    Deletes a task from the database based on the provided task ID
    """
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("html_routes.tasks"))


@html_routes_bp.route("/tasks/<int:task_id>/edit", methods=["POST"])
def edit_task(task_id):
    """
    Edits a task from the database based on the provided task ID
    """
    if request.method == "POST":
        task = db.session.get(Task, task_id)
        if task is None:
            abort(404)
        task_description = request.form["description"]
        task_title = request.form["title"]
        task.name = task_title
        task.desc = task_description
        db.session.commit()
        return redirect(url_for("html_routes.tasks"))
    return redirect(url_for("html_routes.tasks"))
