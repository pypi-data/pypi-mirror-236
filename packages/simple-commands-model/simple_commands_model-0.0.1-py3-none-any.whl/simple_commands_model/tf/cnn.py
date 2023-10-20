import tensorflow as tf
from tensorflow import keras
class tf_model_load:
    def __init__(self, path):
        self.load_model = tf.saved_model.load(path)
    def process(self, image):
        predictions = self.load_model(image)
        return predictions
class keras_model_load:
    def __init__(self, path):
        self.load_model = keras.models.load_model(path)
    def Process(self, image):
        return self.load_model.predict(image)
    
    
