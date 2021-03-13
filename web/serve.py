from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from .forms import LoginForm
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)


db.create_all()
example_user = User(id=1, name="Philip Sterne", username="username")
example_user.set_password('mypassword')

db.session.merge(example_user)
db.session.commit()
db.create_all()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)



@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)



@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Logging in")
    if current_user.is_authenticated:
        print("Authenticated")
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main'))
    return render_template('index.html', form=form)


@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
