import numpy as np
import simple_commands as sc
class load_and_process_image:
    def __init__(self, image):
        self.image = image
    def process_image(self, size):
        image = sc.load_images(self.image)
        image = sc.resize(image, size)
        image = sc.BGR_TO_RGB(image)
        image = image.astype('float64') / 255.0
        image = np.expand_dims(image, axis=0)
        return image
