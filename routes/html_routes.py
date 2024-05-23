from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from db import db
from models import User, Task
from validationForm import RegisterForm, LoginForm
from flask_login import login_required, login_user, current_user, logout_user, logout_user
from datetime import datetime, timezone

html_routes_bp = Blueprint('html_routes', __name__)

"""
Routes allow you to define Flask pages in a logical and organized way
"""

@html_routes_bp.route("/")
def index():
    """Renders the home page under /templates/index.html"""
    tasks = Task.query.all()
    start_dates = []
    end_dates = []
    for task in tasks:
        date_to_string = datetime.fromisoformat(str(task.start_date))
        start_dates.append(date_to_string.strftime("%Y/%m/%d %I:%M%p"))
        if task.end_date is not None: 
            date_to_string = datetime.fromisoformat(str(task.end_date))
            end_dates.append(date_to_string.strftime("%Y/%m/%d %I:%M%p"))
        else:
            end_dates.append(None)
    return render_template("index.html", tasks=tasks, start_dates=start_dates, end_dates=end_dates)


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
    ## Can be refactored as it is redundant 
    start_dates = []
    end_dates = []
    for task in tasks:
        date_to_string = datetime.fromisoformat(str(task.start_date))
        start_dates.append(date_to_string.strftime("%Y/%m/%d %I:%M%p"))
        
        if task.end_date is not None:
            date_to_string = datetime.fromisoformat(str(task.end_date))
            end_dates.append(date_to_string.strftime("%Y/%m/%d %I:%M%p"))
            
        else:
            end_dates.append(None)
            
        categories = {task.id: task.category.name if task.category else 'No Category' for task in tasks}
        
    return render_template("tasks.html", tasks=tasks, start_dates=start_dates, end_dates=end_dates,categories=categories)
  
@html_routes_bp.route("/tasks/create", methods=["GET", "POST"])
def create_tasks():
    """
    Creates a task object using the POST request body
    """
    if request.method == "POST":
        task_title = request.form["title"]
        task_description = request.form["description"]
        task_due = request.form["due_date"]
        current_time = datetime.now()
        
        ## Takes the due date from 2024/05/11 04:30AM format and converts it into the database format 
        if task_due: 
            parsed_datetime = datetime.strptime(task_due, "%Y-%m-%dT%H:%M")
            if parsed_datetime < datetime.now():
                flash("Due date cannot be before the current date", "error")
                return redirect(url_for("html_routes.create_tasks"))
            
            output_datetime_str = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            output_datetime_str = datetime.fromisoformat(output_datetime_str[:-1])
        ## If task does not have a due date returns none to database
        else:
            output_datetime_str = None
            
        db.session.add(Task(name=task_title, desc=task_description, user_id=current_user.id, start_date=current_time, end_date=output_datetime_str))
        db.session.commit()
        return redirect(url_for('html_routes.tasks'))
    current_time = datetime.now()
    current_time = datetime.fromisoformat(str(current_time)).strftime("%Y/%m/%d %I:%M%p")
    return render_template("create.html",current_time=current_time)


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
        task_due = request.form["due_date"]
        task.name = task_title
        task.desc = task_description
        if task_due: 
            parsed_datetime = datetime.strptime(task_due, "%Y-%m-%dT%H:%M")
            if parsed_datetime < datetime.now():
                flash("Due date cannot be before the current date", "error")
                return redirect(url_for("html_routes.tasks"))
            
            output_datetime_str = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            output_datetime_str = datetime.fromisoformat(output_datetime_str[:-1])
            task.end_date = output_datetime_str
        else:
            task.end_date = None  # If no due date provided, set it to None
        db.session.commit()
        return redirect(url_for("html_routes.tasks"))
    return redirect(url_for("html_routes.tasks"))
