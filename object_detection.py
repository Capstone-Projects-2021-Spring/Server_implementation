from imageai.Classification import ImageClassification
import os

execution_path = os.path.dirname(os.path.abspath(__file__))
prediction = ImageClassification()


# Import the object detection model to be used for photo tag
def import_model():
    global prediction
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath(os.path.join(execution_path, "inception_v3_weights_tf_dim_ordering_tf_kernels.h5"))
    prediction.loadModel()


# Process an image at the specified path, returning all of the associated tags and their probabilities
# Tags are returned as a list of tuples
# Ex. [(predicted_tag, probability), ..., (predicted_tag, probability)]
def process_image(image_path):
    predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, image_path))
    return list(zip(predictions, probabilities))
