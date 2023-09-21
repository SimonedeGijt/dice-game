from picamera2 import Picamera2
import time
from libcamera import controls
import diceController
import numpy as np


picam2 = Picamera2()
camera_config = picam2.create_preview_configuration({'size':(3280,2464)})
picam2.configure(camera_config)
picam2.start()
picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})


def takePicture():
    diceController.rollDice()
    print("Waiting for steady dice and focus")
    time.sleep(5)
    image = picam2.capture_image("main")
    frame = np.array(image)
    print("captured image")
    return frame







