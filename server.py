from flask import Flask, jsonify, request, session, redirect
from uuid import uuid4
from rq import Queue
from rq.job import Job
from worker import conn
import os
import object_detection
import redis
import json

app = Flask(__name__)
execution_path = os.path.dirname(os.path.abspath(__file__))
redis_server = redis.Redis("localhost")

q = Queue(connection=conn)

@app.route('/uploadImage', methods=['POST'])
def upload_image():
    username = request.form.get('username')
    print(f'Receiving image from {username}')

    # Ensure file is passed with request
    if 'file' not in request.files:
        return jsonify({'status': '400', 'error': 'No image passed with request'}), 400

    upload_file = request.files['file']
    
    from server import image_upload

    result = q.enqueue(
        func=image_upload, args=(upload_file, username), result_ttl=5000
    )
    print(result)
    
    return jsonify({'status': 200, 'labels': redis_server.get(filename)})

@app.route('/getData', methods=['GET'])
def retrieve_images():
    print(request.json)
    content = request.json
    username = content["username"]
    password = content["password"]
    n = 0
    result = {"numImages": 0, "images": {}}
    '''
    result = {
        "numImages": 0,
        "images": {
            "filename": tags,
            "filename": tags,
            "filename": tags...
        }
    }
    '''
    user_string = redis_server.get(username)
    if user_string is not None:
        user = json.loads(user_string)
        result["numImages"] = len(user)
        result["images"] = user
    return jsonify({'status': 200, 'results': result})


if __name__ == '__main__':
    print('Importing object detection model')
    object_detection.import_model()

    print('Starting server')
    app.run()

def image_upload(upload_file, username):
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
    
    i = 0
    taglist = []
    user = {}
    '''
    user = {
        "filename": tags,
        "filename": tags,
        "filename": tags...
    }

    '''
    user_string = redis_server.get(username)
    if user_string is not None:
        user = json.loads(user_string)
    else:
        # Iterate over all the items found and add the tags with a high enough probability to the list
        for item in res:
            pred = item[0]  # Prediction
            prob = item[1]  # Probability
            if prob > 80:
                taglist[i] = pred
                i += 1
            print(f'Prediction: {pred}. Probability: {prob}')
        user[filename] = taglist
        user_string = json.dumps(user)
        redis_server.set(username, user_string)


    # Remove file from server once it has been processed
    os.remove(filepath)

    return jsonify({'status': 200, 'labels': user[filename]})