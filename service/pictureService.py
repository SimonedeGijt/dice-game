from picamera2 import Picamera2
import time
from libcamera import controls
from service.diceController import roll_dice
import numpy as np


picam2 = Picamera2()
camera_config = picam2.create_preview_configuration({'size':(1920,1080)})
picam2.configure(camera_config)
picam2.start()
picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})


def take_picture():
    roll_dice()
    print("Waiting for steady dice and focus")
    time.sleep(5)
    image = picam2.capture_image("main")
    frame = np.array(image)
    print("captured image")
    return frame







