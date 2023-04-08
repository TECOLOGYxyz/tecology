
from picamera2 import Picamera2, Preview
import time
import light
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
picam2.configure(camera_config)
picam2.start()


for i in range(10):
    
    job = picam2.autofocus_cycle(wait=False)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    success = picam2.wait(job)
    
    picam2.capture_file("images/" + timestamp + "_" + str(i) + ".jpg")
    light.lightGreenFlash()

    time.sleep(2)

