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
    connEnv = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/environment.db')
    c = connEnv.cursor()

    connDetect = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/detections.db')

    while True:

        ### Environment
        # Query the latest number from the database
        #cursor = conn.execute("SELECT number FROM environment ORDER BY id DESC LIMIT 1")
        envVariables = connEnv.execute("SELECT temperature, pressure, humidity FROM environment ORDER BY id DESC LIMIT 1")
        envV = envVariables.fetchall()[0]
        latestTemp, latestPress, latestHumi = envV[0], envV[1], envV[2]
        print("Latest env: ", envV)

        detVariables = connDetect.execute(f"SELECT SUM({'today'}), SUM({'total'}) FROM {'detect'}")
        sums = detVariables.fetchall()[0]
        sumToday, sumTotal = int(sums[0]), int(sums[1])

        print("Sum today:", sumToday)
        print(type(sumToday))
        print("Sum all:", sumTotal)

        detVariables = connDetect.execute(f"SELECT {'class'}, {'total'} FROM {'detect'} WHERE {'total'} = (SELECT MAX({'total'}) FROM {'detect'})")
        seenMosts = detVariables.fetchall()[0]
        seenMostClass, seenMostNumber = str(seenMosts[0]), int(seenMosts[1])

        detVariables = connDetect.execute(f"SELECT {'class'}, {'total'} FROM {'detect'} WHERE {'total'} > 0 AND {'total'} = (SELECT MIN({'total'}) FROM {'detect'} WHERE {'total'} > 0)")
        seenLeasts = detVariables.fetchall()[0]
        seenLeastClass, seenLeastNumber = seenLeasts[0], int(seenLeasts[1])

        print("Seen most: ", seenMostClass, seenMostNumber)
        print("Seen least: ", seenLeastClass, seenLeastNumber) 
        print(repr(seenMostClass))
        print(repr(latestTemp))
        
        s = f'{{"temperature": {latestTemp}, "humidity": {latestHumi}, "pressure": {latestPress}, "sumToday": {sumToday}, "sumTotal": {sumTotal}, "seenMostClass": "{seenMostClass}", "seenMostNumber": {seenMostNumber}, "seenLeastClass": "{seenLeastClass}", "seenLeastNumber": {seenLeastNumber}}}'
        sock.send(s)


        time.sleep(5)

# @sock.route('/echo')
# def echo(sock):
#     while True:
#         data = sock.receive()
#         sock.send(data)
#         sock.send("Helo")

# Run local production with:
# gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 sockApp:app