from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    """A user.

    Instance attributes:
      email (str): The user's email
      password (str): The user's password
    """

    __tablename__ = "users"

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"<User email={self.email}>"

    def __init__(self, email, password):
        """Initialize a user.

        Args:
          email (str): The user's email address
          password (str): The user's password
        """

        password = bcrypt.generate_password_hash(password)
        super().__init__(email=email, password=password)

    def get_id(self):
        """Override UserMixin.get_id."""

        return self.email

    def add_goal(self, goal):
        """Add a user's goal.

        Args:
          goal (Goal): A goal
        """

        self.goals.append(goal)

    def check_password(self, password):
        """Validate a password.

        Args:
          password (str): A password

        Returns:
          True if password matches user's hashed password
        """

        return bcrypt.check_password_hash(self.password, password)


class Goal(db.Model):
    """A goal.

    Instance attributes:
      title (str): The title or description of the goal
      author (User): The user who created the goal
    """

    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    author_email = db.Column(db.String, db.ForeignKey("users.email"), nullable=False)
    author = db.relationship("User", backref="goals")

    def __repr__(self):
        return f"<Goal id={self.id} title={self.title}>"

    def __init__(self, title):
        """Initialize a goal.

        Arguments:
          title (str): The title or description of the goal
        """

        super().__init__(title=title)


def connect_to_db(app, db_uri):
    """Connect a Flask application to a database.

    Arguments:
      app (Flask): A Flask application instance
      db_uri (str): A database URI
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)


def create_test_data():
    """Create test data."""

    db.create_all()
    user = User("test@test.test", "test")
    user.goals.append(Goal("Test 1"))
    user.goals.append(Goal("Test 2"))
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    import os
    import sys

    from server import app

    connect_to_db(app, "postgresql:///goals")

    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        os.system("dropdb goals")
        os.system("createdb goals")
        create_test_data()
