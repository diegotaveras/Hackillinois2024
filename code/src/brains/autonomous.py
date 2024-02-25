from . import base
from numpy import ndarray
from PIL import Image
import cv2
import time
import numpy as np
import signal

class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)
        # self.spin_speed = base.Brain.spin_speed



    def logic(self):
        """If anything is detected by the distance_sensors, stop the car"""
        

        def signal_handler(signal, frame):
            self.vehicle.stop()
            print("You pressed Ctrl+C - or killed me with -2")
            exit(0)

        total_seconds = 60

        start_time = time.time()
 
        # while time.time() - start_time < total_seconds:

        signal.signal(signal.SIGINT, signal_handler)

            # if anything is detected by the sensors, stop the car
        stop = False
        #47,89,56 orig color
        lower_green = np.array([0,39,6])
        upper_green = np.array([80, 139, 80])

        for distance_sensor in self.distance_sensors:
            # Modify for sensor distance sensitivity
            if distance_sensor.distance < 0.5:
                self.vehicle.stop()
                stop = True

        if stop == True: 
            self.vehicle.pivot_right(0.1)
            
            self.camera.capture
            image = self.camera.image_array
            im = Image.fromarray(image)
            im = im.convert("RGB")
            im.save("./test_image1.jpeg")


            image = cv2.imread('test_image1.jpeg')

            mask = cv2.inRange(image, lower_green, upper_green)
            detected_output = cv2.bitwise_and(image, image, mask = mask)
            # Corrects upside down camera to right side up
            detected_output = cv2.rotate(detected_output, cv2.ROTATE_180)
            cv2.imshow("green color detection", detected_output)
            cv2.waitKey(0)
            print("max value" + max(detected_output.data))

            # cv2.inRange(image, green_boundary)
        if not stop:
            self.vehicle.drive_forward()
