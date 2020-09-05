from flask import Flask, render_template
import requests

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  response = requests.get('https://randomuser.me/api/', headers = {
      'Accept': 'application/json'
    })
  print(response.json())
  return render_template('index.html')
