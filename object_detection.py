import datetime
from imageai.Classification import ImageClassification
import os
import db

execution_path = os.path.dirname(os.path.abspath(__file__))
prediction = ImageClassification()


# Import the object detection model to be used for photo tag
def import_model():
    global prediction
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath(os.path.join(execution_path, "inception_v3_weights_tf_dim_ordering_tf_kernels.h5"))
    prediction.loadModel()


def process_new_job(job):
    start = datetime.datetime.now()
    tags = process_image(job.photo_path)
    print(tags)
    db.add_tags(platform=job.platform, user_identifier=job.email, photo_identifier=job.photo_identifier, tags=tags)
    os.remove(job.photo_path)
    print(f'Process time: {datetime.datetime.now() - start}')


# Process an image at the specified path, returning all of the associated tags and their probabilities
# Tags are returned as a list of tuples
# Ex. [(predicted_tag, probability), ..., (predicted_tag, probability)]
def process_image(image_path, min_probability=30):
    try:
        predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, image_path))
    
        ret_tags = list()
        for tag in zip(predictions, probabilities):
            print(f'Prediction: {tag[0]}  |   Probability: {tag[1]}')
            if tag[1] >= min_probability:
                ret_tags.append(tag[0])

    except Exception as e:
        print(e)
            
    return ret_tags or []


if __name__ == '__main__':
    print(process_image('/home/anon/Downloads/AKQXH4V3YYI6VF6BNTYRN77CNQ.jpg'))
