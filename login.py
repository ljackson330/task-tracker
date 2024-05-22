from models import User
from flask_login import LoginManager
from flask import redirect

login_manager = LoginManager()


"""Gets the user id and session"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""Unauthorize users trying to access by changing the url gets redirected"""
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')