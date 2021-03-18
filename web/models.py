from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user
from .forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from .serve import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db.create_all()
example_user = User(id=1, name="Philip Sterne", username="username")
example_user.set_password('mypassword')

db.session.merge(example_user)
db.session.commit()
db.create_all()
