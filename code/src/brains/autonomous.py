from . import base
from numpy import ndarray
from PIL import Image
import cv2
import random
import numpy as np
import signal
from time import sleep

class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)
        # self.spin_speed = base.Brain.spin_speed



    def logic(self):
        # For exiting the program
        def signal_handler(signal, frame):
            self.vehicle.stop()
            print("You pressed Ctrl+C - or killed me with -2")
            exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        # Shades of green bounds in HSV
        lower_green = np.array([36,0,0])
        upper_green = np.array([86, 255, 255])

        self.vehicle.drive_forward()
        
        for distance_sensor in self.distance_sensors:
            if distance_sensor.distance < 0.75:
                self.vehicle.stop()
                # Take a picture
                self.camera.capture
                image = self.camera.image_array
                
                if image is None:
                    print("No image found")
                    continue
                
                im = Image.fromarray(image)
                im = im.convert("RGB")
                im.save("./test_image1.jpeg")


                image = cv2.imread('test_image1.jpeg')
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_image, lower_green, upper_green)
                # Image Contouring
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                min_area = 3000  # Minimum area to be considered a cap
                max_area = 10000  # Maximum area to be considered a cap
                cap_contours = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]
                # Check if a cap (target) is present
                is_cap_present = len(cap_contours) > 0
                
                if (is_cap_present):
                    self.vehicle.stop()
                    detected_output = cv2.bitwise_and(image, image, mask = mask)
                    # Corrects upside down camera to right side up
                    detected_output = cv2.rotate(detected_output, cv2.ROTATE_180)
                    cv2.imshow("green color detection", detected_output)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # Stop checking for caps
                    break

                else:
                    #Spin right if no cap is detected
                    spin_time  = random.uniform(1, 2)
                    # Max spin speed
                    self.vehicle.pivot_right(1)
                    sleep(spin_time)
                    self.vehicle.drive_forward()
