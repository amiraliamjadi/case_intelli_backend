from flask import Blueprint, render_template
from .extensions import db
from app.models import User

# Define a Blueprint
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

# Example usage (in a route or other function)
@main.route('/about')
def about():
    # Example: Create a new user
    new_user = User(username='testuser3', email='test3@example.com', password='12345')
    db.session.add(new_user)
    db.session.commit()

    # Example: Query users
    users = User.query.all()
    user_names = [user.username for user in users]

    return f"Users: {user_names}"