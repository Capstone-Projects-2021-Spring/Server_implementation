from flask import Flask, jsonify, request, session, redirect
from uuid import uuid4
import os
import object_detection

app = Flask(__name__)
execution_path = os.path.dirname(os.path.abspath(__file__))


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    username = request.form.get('username')
    print(f'Receiving image from {username}')

    # Ensure file is passed with request
    if 'file' not in request.files:
        return jsonify({'status': '400', 'error': 'No image passed with request'}), 400

    upload_file = request.files['file']
    
    # Create a unique file name for this image request
    # Hex encoded to ensure safe filename
    filename = uuid4().hex

    # Save file locally on server
    filepath = os.path.join(execution_path, filename)
    upload_file.save(filepath)

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

    return jsonify({'status': 200, 'labels': 'test, '+username})


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
    print('Importing object detection model')
    object_detection.import_model()

    print('Starting server')
    app.run()
