from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os

dt = datetime.now()

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")

output_folder = 'images'

picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

ts=datetime.timestamp(dt)
file_name = os.path.join(output_folder, f"{ts}.jpg")
picam2.capture_file(file_name)


