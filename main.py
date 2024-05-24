from flask import Flask
from pathlib import Path
from db import db
from login import login_manager

from routes import html_routes_bp

# Initialize Flask
flaskapp = Flask(__name__)
flaskapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskdatabase.db"
flaskapp.config['SECRET_KEY'] = "foobar"
login_manager.init_app(flaskapp)
login_manager.login_view = "login"
flaskapp.instance_path = Path(".").resolve()

# Register blueprints
flaskapp.register_blueprint(html_routes_bp, url_prefix="/")

# Initialize the database
db.init_app(flaskapp)

# Run Flask on port 8080
if __name__ == '__main__':
    flaskapp.run(debug=True, port=8080)
