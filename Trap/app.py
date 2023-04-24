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
    conn = sqlite3.connect('data/environment.db')
    c = conn.cursor()
    while True:

        ### Environment
        # Query the latest number from the database
        #cursor = conn.execute("SELECT number FROM environment ORDER BY id DESC LIMIT 1")
        x = conn.execute("SELECT temperature, pressure, humidity FROM environment ORDER BY id DESC LIMIT 1")
        print("Hello")
        envV = x.fetchall()[0]
        latestTemp, latestPress, latestHumi = envV[0], envV[1], envV[2]
        print(envV)
        # latestTemp = cursor.fetchone()[0]
        # latestHumi = cursor.fetchone()[0]
        # latestPress = cursor.fetchone()[0]
        s = f'{{"temperature": {latestTemp}, "humidity": {latestHumi}, "pressure": {latestPress}}}'
        sock.send(s)
        #sock.send('{"temperature": latestTemp, "humidity": "70", "pressure": "1013"}')

        # sock.send(str(latestTemp)) # Convert to string and send to client
        # sock.send(str(latestHumi))
        # sock.send(str(latestPress))

        ### Vision


        time.sleep(5)

# @sock.route('/echo')
# def echo(sock):
#     while True:
#         data = sock.receive()
#         sock.send(data)
#         sock.send("Helo")

# Run local production with:
# gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 sockApp:app