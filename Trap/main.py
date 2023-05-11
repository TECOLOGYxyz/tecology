
### Gloabal packages
from configparser import ConfigParser
import time
import sqlite3
import datetime
import random as rand
from picamera2 import Picamera2, Preview
import os
import logging
import cv2
from gpiozero import CPUTemperature
import csv
from collections import Counter
import socket
import numpy as np


# Webapp
import threading
from flask import Flask, render_template, request, jsonify

### Local modules
# from screen import updateScreen
import light
import helpers
import screen
import ai


###
# Remember to put Restart=always in systemd service config!



###
# Set up configs
logging.basicConfig(level=logging.DEBUG)


# Initialize SQLite database connection and create table to store sensor data
logging.info("Setting up environment database")
connSensor = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/environment.db')
cSensor = connSensor.cursor()
cSensor.execute('''CREATE TABLE IF NOT EXISTS environment
            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, temperature REAL, pressure REAL, humidity REAL)''')


# Initialize SQLite database connection and create table to store image data
logging.info("Setting up vision database")
connVision = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/vision.db')
cVision = connSensor.cursor()
cVision.execute('''CREATE TABLE IF NOT EXISTS vision
            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, imagePath TEXT, drawPath TEXT, predictions TEXT)''')


# Initialize SQLite database connection and create table to store detection overview
logging.info("Setting up detections database")
connDetect = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/detections.db')
cDetect = connDetect.cursor()
cDetect.execute('''CREATE TABLE IF NOT EXISTS detect
            (class TEXT, today REAL, total REAL)''')

with open('/home/tecologyTrap1/tecology/Trap/classes.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    print(spamreader)
    classes = [row[0] for row in spamreader]



# Check if the classes already exist in the detect table
existing_classes = []
cDetect.execute("SELECT class FROM detect")
for row in cDetect.fetchall():
    existing_classes.append(row[0])

# Insert new classes into the detect table if they don't already exist
classes_to_insert = [(c, 0, 0) for c in classes if c not in existing_classes]
if classes_to_insert:
    cDetect.executemany('INSERT INTO detect VALUES(?,?,?);', classes_to_insert)
    connDetect.commit()

# Close the database connection
connDetect.close()

# classesDB = [(c, 0, 0) for c in classes]
# cDetect.executemany('INSERT INTO detect VALUES(?,?,?);', classesDB)
# connDetect.commit()


# # Check internet connection
logging.info("Checking internet connection")
helpers.checkInternet()

# Set welcome screen
hostName = socket.gethostname()
ip_address = socket.gethostbyname(hostName)
hostAddress = socket.gethostbyname(hostName + ".local")

# print(f"Hostname: {hostName}")
# print("IP: ", ip_address)
# print(f"Host Address: {hostAddress, }")

# Check internet

if helpers.checkInternet():
    netStatus = "OK"
else:
    netStatus = "No"

screen.welcomeScreen(hostName, hostAddress, netStatus)



# Maximum number of detections to save
MAX_DETECTIONS = 4

# Desired dimensions for the cropped and resized images
CROP_SIZE = (200, 200)




def save_crop_image(image, detection, i):
    # Extract the bounding box coordinates from the detection
    xmin, ymin, xmax, ymax = detection[0],detection[1],detection[2],detection[3]
    x = xmin #int((xmin + xmax)/2)
    y = ymin # int((ymin + ymax)/2)
    w = xmax - xmin
    h = ymax - ymin
    conf = detection[4]

    # Calculate the padding values to create a square crop
    max_dim = max(w, h)
    pad_x = (max_dim - w) // 2
    pad_y = (max_dim - h) // 2
    
    # Apply padding to the bounding box
    x -= pad_x
    y -= pad_y
    w = h = max_dim
    
    # Extract the crop region from the image
    crop_image = image[max(0, y):y+h, max(0, x):x+w]
    # Resize the crop image to the desired dimensions
    crop_image = cv2.resize(crop_image, CROP_SIZE)
    
    # Create a white bar image
    bar_height = 20
    bar_image = np.ones((bar_height, crop_image.shape[1], 3), dtype=np.uint8) * 255
    
    # Concatenate the crop image and the white bar image
    result_image = np.concatenate((crop_image, bar_image), axis=0)
    
    # Add the detection class label text to the result image
    class_label = detection[5]
    imageLabel = f'{class_label} ({int(conf*100)}%)'
    cv2.putText(result_image, imageLabel, (5, crop_image.shape[0] + 15),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Save the result image
    cv2.imwrite('/home/tecologyTrap1/tecology/Trap/static/crop_{}.jpg'.format(i), result_image)


def runGoodmorning():
    light.lightPowerUp()

    # Create folders for todays data
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    dataToday = os.path.join("/home/tecologyTrap1/tecology/Trap/data", today)

    if not os.path.exists(dataToday):
        os.makedirs(dataToday)

    
    # Set up camera
    logging.info("Setting up camera")
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
    picam2.configure(camera_config)
    picam2.start()

    job = picam2.autofocus_cycle(wait=False)
    success = picam2.wait(job)

    # Check internet connection
    #helpers.checkInternet()

    return dataToday, picam2



# ######## AWAKE ########

maxInterval = 5
cpuThreshold = 72


def runAwake(dataToday, picam2):
    latest_detections = []

    light.lightKill()

    #TODO: Set today of detections to zero
    
    # Zero detection numbers for today
    connDetect = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/detections.db')
    cDetect = connDetect.cursor()
    cDetect.execute(f"UPDATE {'detect'} SET {'today'} = 0")
    connDetect.commit()
    connDetect.close()


    startTime = datetime.datetime.now()
    i = 0
    interval = maxInterval
    while True:
        
        print("Still running main worker: ", i)
        i += 1

#    connSensor, cSensor, connVision, cVision = runGoodmorning()


        ### Environmental variables ###
        temperature = rand.randint(12,25) #bme280.temperature
        pressure = rand.randint(1020, 1200) #bme280.pressure
        humidity =  rand.randint(40,80) #bme280.humidity

        # Get current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert data into env database
        connSensor = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/environment.db')
        cSensor = connSensor.cursor()
        #cSensor.execute("INSERT INTO environment VALUES (?, ?, ?, ?)", (timestamp, temperature, pressure, humidity))
        cSensor.execute('INSERT INTO environment (timestamp, temperature, humidity, pressure) VALUES (?, ?, ?, ?)', (timestamp,temperature,humidity,pressure))
        connSensor.commit()
        print("Env. variables saved")



        ### Vision ###

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        imagePath = os.path.join(dataToday, timestamp+".jpg")

        
        array = picam2.capture_array("main")
        array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)

        arrayInf = array.copy()
        p = ai.inference(arrayInf)

        if p:
            cv2.imwrite('/home/tecologyTrap1/tecology/Trap/static/latest.jpg', arrayInf) # Save image for webapp

            arrayInf, conOut = p
            cv2.imwrite(imagePath, array) # Save image for storage
            startTime = datetime.datetime.now()
            
            # Save detection numbers in db for webapp
            detectionCount = Counter(insect for _, _, _, _, _, insect in conOut)

            connDetect = sqlite3.connect('/home/tecologyTrap1/tecology/Trap/data/detections.db')
            cDetect = connDetect.cursor()

            for insect, count in detectionCount.items():
                # Query the current values of today and total columns for the insect
                cDetect.execute("SELECT today, total FROM detect WHERE class=?", (insect,))
                row = cDetect.fetchone()

                # Update the today and total columns with the new counts
                today = row[0] + count
                total = row[1] + count

                # Update the values in the detect table for the insect
                cDetect.execute("UPDATE detect SET today=?, total=? WHERE class=?", (today, total, insect))

            connDetect.commit()
            connDetect.close()

            print("Array info:")
            print(arrayInf)
            print("conOut:")
            print(conOut)

            # for det in conOut:
            #     save_crop_image(array, det)
            
            latest_detections.extend(conOut)

                # Save crops of the latest four detections

            # BUG: This crops out old detections in new images without the object present.     
            for i, detection in enumerate(latest_detections[-MAX_DETECTIONS:]):
                save_crop_image(array, detection, i)
    
            # Remove older detections if the list exceeds the maximum number of detections
            if len(latest_detections) > MAX_DETECTIONS:
                latest_detections = latest_detections[-MAX_DETECTIONS:]

            ###### Save crops draft ######




            # TODO: Save detection coordinates to database!
        else:
            cv2.imwrite('/home/tecologyTrap1/tecology/Trap/static/latest.jpg', arrayInf)
            elapsed = datetime.datetime.now() - startTime
            if elapsed > datetime.timedelta(minutes=5):
                cv2.imwrite(imagePath, array)
                print("+5 minutes passed. Blank saved.")
                startTime = datetime.datetime.now()
                # TODO: Save info to database!

    

        # Throttle and sleep
        cpu = CPUTemperature()
        cpu = round(cpu.temperature, 1)
 
        if cpu > cpuThreshold:
            interval = maxInterval * 2
            print(f"CPU temperature too high ({str(cpu)} C). Throttling down to run inference every {interval} seconds.")
            time.sleep(interval)
        else:
            if interval > maxInterval:
                interval = max(maxInterval, interval // 2)
                time.sleep(interval)
                print(f"CPU temperature normal ({str(cpu)} C). Ramping down to run inference every {interval} seconds.")
            else:
                print(f"CPU temperature normal ({str(cpu)} C). Running inference every {interval} seconds.")
                time.sleep(interval)



#         ### Screen ###
# #       updateScreen(t, cpu)
        ### Health checks
        # Check CPU tempt to throttle down if getting too hot

# ######## GET READY FOR BED ########


def runBedReady():
    """
    Preparation for sleep mode.
    """
    # # Zip images to
    # # Back up data to drive
    # # Turn of light
    pass

def runSleep():
    """
    Does nothing but await the time for starting a new day
    """
    pass


def runNocturnal():
    """
    A night mode that captures images using the onboard ring light as a flash
    """
    pass





# ######## GO TO SLEEP ########
# #light.lightKill()
# # Take an image an hour - just for fun? With flash



def runTrap():
    dataToday, picam2 = runGoodmorning()
    runAwake(dataToday, picam2)

if __name__ == '__main__':
    runTrap()





























# # ######## WEBAPP ########
# app = Flask(__name__)

# def runApp():
#     app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')

# @app.route('/')
# def index():
#     # connect to the sqlite database
#     conn = sqlite3.connect('data/environment.db')
#     c = conn.cursor()

#     # retrieve the latest weather data from the database
#     c.execute('SELECT temperature, humidity, pressure, timestamp FROM environment ORDER BY timestamp DESC LIMIT 1')
#     latest_data = c.fetchone()
#     temperature = latest_data[0]
#     humidity = latest_data[1]
#     pressure = latest_data[2]
#     timestamp = latest_data[3]

#     # retrieve the data for the graph
#     c.execute('SELECT temperature, humidity, pressure, timestamp FROM environment WHERE date(timestamp) = date("now")')
#     graph_data = c.fetchall()

#     # close the database connection
#     conn.close()

#     # render the template with the data
#     print("Variables: ", temperature, humidity, pressure)
#     return render_template('index.html', temperature=temperature, humidity=humidity, pressure=pressure, timestamp=timestamp, graph_data=graph_data)


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


        # #picam2.capture_file("images/" + timestamp + "_" + str(i) + ".jpg")