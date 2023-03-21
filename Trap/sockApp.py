from flask import Flask, render_template
from flask_sock import Sock
import sqlite3
import random
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html'), 'index.js'


@sock.route('/echo')
def echo(sock):
    conn = sqlite3.connect('numbers.db')
    c = conn.cursor()
    while True:
        # Query the latest number from the database
        cursor = conn.execute("SELECT number FROM numbers ORDER BY id DESC LIMIT 1")
        latest_number = cursor.fetchone()[0]
        sock.send(str(latest_number)) # Convert to string and send to client
        time.sleep(5)
# @sock.route('/echo')
# def echo(sock):
#     while True:
#         data = sock.receive()
#         sock.send(data)
#         sock.send("Helo")

# Run local production with:
# gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 sockApp:app