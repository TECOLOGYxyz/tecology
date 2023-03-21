
from picamera2 import Picamera2, Preview
import time

import light

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
picam2.configure(camera_config)
picam2.start()


light.lightPowerUp()

classes = ["one", "two", "three"]

for j in classes:
    for i in range(1):
        job = picam2.autofocus_cycle(wait=False)
        success = picam2.wait(job)
        
        picam2.capture_file("images/" + j + "_" + str(i) + ".jpg")

