from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jiseufnjbxslue:05457b355e4aabeaeae4a1c17e76c07fde2b7a91c702f91e9be4d1d270d36817@ec2-3-211-245-154.compute-1.amazonaws.com:5432/ddd507tv8dg7mc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))


db.create_all()
example_user = User(id=1, name="Philip Sterne")
db.session.merge(example_user)
db.session.commit()


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run()
