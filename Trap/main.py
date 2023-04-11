# from screen import updateScreen
import light
import helpers
# import screen

from configparser import ConfigParser
import time
import sqlite3
from datetime import datetime

# Webapp
import threading
from flask import Flask, render_template, request, jsonify

import random as rand
#import pandas as pd

from picamera2 import Picamera2, Preview
import time

#AI
import ai

# Set up configs



# Initialize SQLite database connection and create table to store sensor data
connSensor = sqlite3.connect('data/environment.db')
cSensor = connSensor.cursor()
cSensor.execute('''CREATE TABLE IF NOT EXISTS environment
            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, temperature REAL, pressure REAL, humidity REAL)''')


### Environmental variables ###
temperature = rand.randint(12,25) #bme280.temperature
pressure = rand.randint(1020, 1200) #bme280.pressure
humidity =  rand.randint(40,80) #bme280.humidity

# Get current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Insert data into env database

connSensor = sqlite3.connect('data/environment.db')
cSensor = connSensor.cursor()
#cSensor.execute("INSERT INTO environment VALUES (?, ?, ?, ?)", (timestamp, temperature, pressure, humidity))
cSensor.execute('INSERT INTO environment (temperature, humidity, timestamp, pressure) VALUES (?, ?, ?, ?)', (10,20,30,40))
connSensor.commit()
print("Env. variables saved")



#### debug up



# # Initialize SQLite database connection and create table to store image data
# connVision = sqlite3.connect('data/vision.db')
# cVision = connSensor.cursor()
# cVision.execute('''CREATE TABLE IF NOT EXISTS vision
#             (timestamp TEXT, imagePath TEXT, predictions TEXT)''')

# #return connSensor, cSensor, connVision, cVision

# # Check internet connection
# helpers.checkInternet()


# def runGoodmorning():
#     light.lightPowerUp()


#     # Create folders for todays data



    

#     # Set up camera
#     picam2 = Picamera2()
#     camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
#     picam2.configure(camera_config)
#     picam2.start()

#     job = picam2.autofocus_cycle(wait=False)
#     success = picam2.wait(job)

#     # Check internet connection
#     helpers.checkInternet()

#     # Set welcome screen
#     screen.welcomeScreen()


# ######## AWAKE ########

# def runAwake():

#     connSensor, cSensor, connVision, cVision = runGoodmorning()

#     i = 0
#     while True:
#         print("Still running main worker: ", i)
#         i += 1
#         time.sleep(2)


#         ### Environmental variables ###
#         temperature = rand.randint(12,25) #bme280.temperature
#         pressure = rand.randint(1020, 1200) #bme280.pressure
#         humidity =  rand.randint(40,80) #bme280.humidity

#         # Get current timestamp
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         # Insert data into env database
#         cSensor.execute("INSERT INTO envVariables VALUES (?, ?, ?, ?)", (timestamp, temperature, pressure, humidity))
#         connSensor.commit()
#         print("Env. variables saved")

#         ### Vision ###

        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # #picam2.capture_file("images/" + timestamp + "_" + str(i) + ".jpg")
        # light.lightGreenFlash()

        # array = picam2.capture_array("main") 

        # ai.inference(array)
#         # Save image
        
#         # Run inference

#         # Save vision info to vision databases

#         # Wait for 5 seconds before reading sensor data again
#         time.sleep(5)



#         ### Screen ###
# #       updateScreen(t, cpu)




# ######## GET READY FOR BED ########
# # Back up images to drive
# # Back up data to drive
# # Turn of light



# ######## GO TO SLEEP ########
# #light.lightKill()
# # Take an image an hour - just for fun? With flash



# ######## WEBAPP ########
app = Flask(__name__)

def runApp():
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')

@app.route('/')
def index():
    # connect to the sqlite database
    conn = sqlite3.connect('data/environment.db')
    c = conn.cursor()

    # retrieve the latest weather data from the database
    c.execute('SELECT temperature, humidity, pressure, timestamp FROM environment ORDER BY timestamp DESC LIMIT 1')
    latest_data = c.fetchone()
    temperature = latest_data[0]
    humidity = latest_data[1]
    pressure = latest_data[2]
    timestamp = latest_data[3]

    # retrieve the data for the graph
    c.execute('SELECT temperature, humidity, pressure, timestamp FROM environment WHERE date(timestamp) = date("now")')
    graph_data = c.fetchall()

    # close the database connection
    conn.close()

    # render the template with the data
    print("Variables: ", temperature, humidity, pressure)
    return render_template('index.html', temperature=temperature, humidity=humidity, pressure=pressure, timestamp=timestamp, graph_data=graph_data)


### RUN PROGRAM ###
# if __name__ == '__main__':
#     try:
#         #logger.info(f'start first thread')
#         t1 = threading.Thread(target=runApp).start()
#         #logger.info(f'start second thread')
# #         t2 = threading.Thread(target=runAwake).start()
#     except Exception as e:
#         print("error")
#         print(e)
#         #logger.error("Unexpected error:" + str(e))


#  gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 sockApp:app