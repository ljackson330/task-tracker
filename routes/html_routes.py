from flask import Blueprint, render_template, redirect, url_for
from models import User, Task
from validationForm import RegisterForm, LoginForm
from flask_login import login_required, login_user, current_user, logout_user, logout_user

html_routes_bp = Blueprint('html_routes', __name__)

"""
Routes allow you to define Flask pages in a logical and organized way
"""

@html_routes_bp.route("/")
def index():
    """Renders the home page under /templates/index.html"""
    return render_template("index.html")

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
