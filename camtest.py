
from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
#camera_config = picam2.create_preview_configuration()
#picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()

time.sleep(2)
#picam2.capture_file("test4.jpg")

job = picam2.autofocus_cycle(wait=False)


print("Doing something else...")
success = picam2.wait(job)
print(success)


picam2.capture_file("test7.jpg")
array = picam2.capture_array("main") # Capture image as numpy array
image = picam2.capture_image("main") # Capture PIL image

