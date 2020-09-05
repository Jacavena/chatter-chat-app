from flask import Flask, redirect, request, render_template, session, url_for
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from markupsafe import escape
from json import dumps
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///messages.db')
app = Flask(__name__)
app.secret_key = b'insertsecretkeyhere'
api = Api(app)

class Messages(Resource):
  def get(self):
    conn = db_connect.connect()
    query = conn.execute("SELECT * FROM messages")
    return { 'messages': [query.cursor.fetchall()] }
  def post(self):
    print("POSTED!")

api.add_resource(Messages, '/messages')

if __name__ == '__main__':
    app.run(port='5002')

@app.route('/')
def index():
  if 'username' in session:
    return render_template('index.html', username=escape(session['username']))
  return render_template('login-form.html') # The form will POST with the value username

@app.route('/login', methods=['POST'])
def login():
  if request.method == 'POST' and request.form['username']:
    session['username'] = request.form['username']
  return redirect(url_for('index'))

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))