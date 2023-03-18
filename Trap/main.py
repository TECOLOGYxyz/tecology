# from screen import updateScreen
# import light
# import helpers
# import screen

import time
import sqlite3
from datetime import datetime

# Webapp
import threading
from flask import Flask, render_template, request, jsonify

import random as rand
import pandas as pd

from picamera2 import Picamera2, Preview
import time


######## WAKE UP ########

def runGoodmorning():
    picam2 = Picamera2()
    picam2.start()
    job = picam2.autofocus_cycle(wait=False)



    #light.lightPowerUp()

    # Check internet connection
    #helpers.checkInternet()

    # Set welcome screen
    #screen.welcomeScreen()
    # Check abiotic sensor

    # Initialize BME280 sensor
    #i2c = busio.I2C(board.SCL, board.SDA)
    #bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    # Initialize SQLite database connection and create table to store sensor data
    connSensor = sqlite3.connect('envVariables.db')
    cSensor = connSensor.cursor()
    cSensor.execute('''CREATE TABLE IF NOT EXISTS envVariables
                (timestamp TEXT, temperature REAL, pressure REAL, humidity REAL)''')
    
    # Initialize SQLite database connection and create table to store sensor data
    connVision = sqlite3.connect('vision.db')
    cVision = connSensor.cursor()
    cVision.execute('''CREATE TABLE IF NOT EXISTS vision
                (timestamp TEXT, imagePath TEXT, predictions TEXT)''')
    
    success = picam2.wait(job) # Check if camera autofocus was a success (returns True if so)
    print("Camera focused: ", success)

    return connSensor, cSensor, connVision, cVision




######## AWAKE ########

def runAwake():

    connSensor, cSensor, connVision, cVision = runGoodmorning()

    i = 0
    while True:
        print("Still running main worker: ", i)
        i += 1
        time.sleep(2)


        ### Environmental variables ###
        temperature = rand.randint(12,25) #bme280.temperature
        pressure = rand.randint(1020, 1200) #bme280.pressure
        humidity =  rand.randint(40,80) #bme280.humidity

        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert data into env database
        cSensor.execute("INSERT INTO envVariables VALUES (?, ?, ?, ?)", (timestamp, temperature, pressure, humidity))
        connSensor.commit()
        print("Env. variables saved")

        ### Vision ###

        # Save image
        
        # Run inference

        # Save vision info to vision databases

        # Wait for 5 seconds before reading sensor data again
        time.sleep(5)



        ### Screen ###
#       updateScreen(t, cpu)




######## GET READY FOR BED ########
# Back up images to drive
# Back up data to drive
# Turn of light



######## GO TO SLEEP ########
#light.lightKill()
# Take an image an hour - just for fun? With flash



######## WEBAPP ########
app = Flask(__name__)

def runApp():
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')

@app.route('/')
def index():
    # connect to the sqlite database
    conn = sqlite3.connect('envVariables.db')
    c = conn.cursor()

    # retrieve the latest weather data from the database
    c.execute('SELECT temperature, humidity, pressure, timestamp FROM envVariables ORDER BY timestamp DESC LIMIT 1')
    latest_data = c.fetchone()
    temperature = latest_data[0]
    humidity = latest_data[1]
    pressure = latest_data[2]
    timestamp = latest_data[3]

    # retrieve the data for the graph
    c.execute('SELECT temperature, humidity, pressure, timestamp FROM envVariables WHERE date(timestamp) = date("now")')
    graph_data = c.fetchall()

    # close the database connection
    conn.close()

    # render the template with the data
    print("Variables: ", temperature, humidity, pressure)
    return render_template('index.html', temperature=temperature, humidity=humidity, pressure=pressure, timestamp=timestamp, graph_data=graph_data)


### RUN PROGRAM ###
if __name__ == '__main__':
    try:
        #logger.info(f'start first thread')
        #t1 = threading.Thread(target=runApp).start()
        #logger.info(f'start second thread')
        t2 = threading.Thread(target=runAwake).start()
    except Exception as e:
        print("error")
        #logger.error("Unexpected error:" + str(e))


