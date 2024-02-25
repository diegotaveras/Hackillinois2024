from . import base
from numpy import ndarray
from PIL import Image


class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)
        # self.spin_speed = base.Brain.spin_speed



    def logic(self):
        """If anything is detected by the distance_sensors, stop the car"""
        
        # if anything is detected by the sensors, stop the car
        stop = False


        for distance_sensor in self.distance_sensors:
            if distance_sensor.distance < 0.25:
                self.vehicle.stop()
                stop = True

        if stop == True: 
            self.vehicle.pivot_right(0.1)
            
            self.camera.capture
            image = self.camera.image_array
            im = Image.fromarray(image)
            im.save("./test_image1.jpeg")
            




        if not stop:
            self.vehicle.drive_forward()
