import python_jwt  # KEEP THIS
import gcloud
from firebase import Firebase
import os

config = {
    "apiKey": os.environ.get('firebase_api_key'),
    "authDomain": "phototag-6ec4a.firebaseapp.com",
    "storageBucket": "",
    "databaseURL": "https://phototag-6ec4a-default-rtdb.firebaseio.com/"
}

firebase = Firebase(config)
db = firebase.database()
auth = firebase.auth()


def auth_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        return True
    except Exception as e:
        print(f'User failed authentication.')
        print(e)
        return False


def add_tags(platform, user_identifier, photo_identifier, tags):
    # Ensure correct platform is specified
    if platform not in ['Android', 'iOS']:
        raise Exception('Invalid platform specified when trying to add a tag')

    for tag in tags:
        try:
            # Set new tag for photo object
            db.child(f'{platform}/{user_identifier}/Photos/{photo_identifier}/photo_tags/{tag}').set(True)
            # Set new tag for search tag 'table'
            db.child(f'{platform}/{user_identifier}/photoTags/{tag}/{photo_identifier}').set(True)
        except Exception as e:
            print(f'Failed adding a tag for user: {user_identifier}, photo: {photo_identifier}')
            print(e)


if __name__ == '__main__':
    print('Connecting to firebase')
    # print(auth_user('', ''))

    photo_id = 'testPhotoId'
    tags = ['abc123', '123abc']

    try:
        add_tags(platform='iOS', user_identifier='sebastiantota', photo_identifier=photo_id, tags=tags)
    except Exception as e:
        print(e)
