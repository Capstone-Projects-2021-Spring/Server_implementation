from flask import Flask, jsonify, request, session, redirect
from uuid import uuid4
import os
import object_detection
import job
from rq import Queue
from rq.job import Job
from worker import conn
import db

q = Queue(connection=conn)


app = Flask(__name__)
execution_path = os.path.dirname(os.path.abspath(__file__))


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    email = request.form.get('email')
    password = request.form.get('password')
    platform = request.form.get('platform')
    photo_identifier = request.form.get('photo_identifier')

    # if not db.auth_user(email, password):
    #     return jsonify({'status': 'error occurred', 'error': 'Firebase auth failed'}), 401

    print(request.form.to_dict())

    # Ensure file is passed with request
    if 'image' not in request.files:
        return jsonify({'status': '400', 'error': 'No image passed with request'}), 400

    upload_file = request.files['image']
    
    # Create a unique file name for this image request
    # Hex encoded to ensure safe filename
    filename = f'{uuid4().hex}.jpg'

    # Save file locally on server
    filepath = os.path.join(execution_path, filename)
    upload_file.save(filepath)

    new_job_obj = job.Job(email=email, password=password, platform=platform,
                      photo_identifier=photo_identifier, photo_path=filepath)

    new_job = q.enqueue_call(func=object_detection.process_new_job, args=(new_job_obj,))

    return jsonify({'status': 'Photo upload success'}), 200


'''
    # Process photo to find all of the detected tags
    # Tags are returned as a list of tuples
    # Ex. [(predicted_tag, probability), ..., (predicted_tag, probability)]
    res = object_detection.process_image(filepath)

    # Iterate over all the items found
    for item in res:
        pred = item[0]  # Prediction
        prob = item[1]  # Probability
        print(f'Prediction: {pred}. Probability: {prob}')

    # Remove file from server once it has been processed
    os.remove(filepath)
'''


@app.route('/getData', methods=['GET'])
def retrieve_images():
    print(request.json)
    content = request.json
    username = content["username"]
    password = content["password"]
    n = 0
    result = {'numImages': n, 'images': {'imageId': [], 'imageId': []}}
    '''
    query = query
    '''
    return jsonify({'status': 200, 'results': result})


if __name__ == '__main__':
    print('Attempting to find firebase api key in environmental variables')
    if os.environ.get('firebase_api_key') is None:
        raise Exception("No firebase api key found in environmental variables")
    print('Found firebase api key')

    print('Starting server')
    app.run()
