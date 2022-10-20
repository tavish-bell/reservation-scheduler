from flask import Flask, flash, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user

from model import Goal, User, connect_to_db, db

app = Flask(__name__)
app.secret_key = "test"
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(email):
    """This is used by flask_login to load the current user."""

    return User.query.get(email)


@app.route("/")
def display_index():
    """Display homepage."""

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def log_in_user():
    """Log in a user."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.get(email)
    if user and user.check_password(password):
        login_user(user)

        return redirect("/goals")

    flash("Your email or password was incorrect")
    return redirect("/")


@app.route("/register", methods=["POST"])
def register_user():
    """Create a new user account."""

    email = request.form["email"]
    password = request.form["password"]

    if not User.query.get(email):
        user = User(email, password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect("/")

    flash("There was an error processing your registration")
    return redirect("/")


@app.route("/goals")
@login_required
def display_goals_dashboard():
    """Display user dashboard."""

    return render_template("goals.html", goals=current_user.goals)


@app.route("/goal/new", methods=["POST"])
@login_required
def create_goal():
    """Create a new goal for the current user."""

    title = request.form["title"]

    goal = Goal(title)
    current_user.add_goal(goal)
    db.session.commit()

    flash(f'New goal - "{goal.title}"')
    return redirect(f"/goals")


@app.route("/goal/<int:goal_id>/edit", methods=["POST"])
@login_required
def edit_goal(goal_id):
    """Edit a goal."""

    goal = Goal.query.get(goal_id)

    title = request.form.get("title", goal.title)
    completed = request.form.get("completed", goal.completed)

    # Parse value of `completed` if necessary, set it to True or False
    if type(completed) is str:
        completed = completed == "true"

    goal.title = title
    goal.completed = completed

    db.session.commit()

    flash(f'Successfully edited "{goal.title}"!')
    return redirect(f"/goals")


if __name__ == "__main__":
    connect_to_db(app, "postgresql:///goals")
    app.run(debug=True, host="0.0.0.0")
