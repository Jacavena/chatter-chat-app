from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from os import urandom

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = urandom(16)

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  messages = db.relationship("Message", backref='user', lazy=True)

  def __init__(self, name):
    self.name = name


class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(300), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, body, user_id):
    self.body = body
    self.user_id = user_id


@app.route('/')
def index():
  return render_template('index.html', messages=Message.query.all(), users=User.query.all())

@app.route('/message', methods=['POST'])
def message():
  if not request.form['name'] or not request.form['body']:
    flash('No name or message', 'error')
  else:
    user = User.query.filter_by(name = request.form['name']).first()
    if not user:
      user = User(request.form['name'])
      db.session.add(user)
      db.session.commit()
    message = Message(request.form['body'], user.id)
    db.session.add(message)
    db.session.commit()
    session['username'] = user.name
  return redirect(url_for('index'))


if __name__ == '__main__':
  db.create_all()
  app.run(debug = True)