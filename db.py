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


# Authentication of a user
# @param    String  Users email
# @param    String  Users password
# @return   Bool    True if authentication was successful, False otherwise
def auth_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        return True
    except Exception as e:
        print(f'User failed authentication.')
        print(e)
        return False


# Adds tags to a specific user
# @param    String  Platform the photo is stored on [Android, iOS]
# @param    String  The user identifier under which the users details are stored under
# @param    String  The photo identifier under which the photos details are stored under
# @param    List    A list of tags to be added
# @return   None
# @Throws   e       Exception thrown when an invalid platform is specified
def add_tags(platform, user_identifier, photo_identifier, tags):
    # Ensure correct platform is specified
    if platform not in ['Android', 'iOS']:
        raise Exception('Invalid platform specified when trying to add a tag')

    # Iterate through all the tags adding each one individually to the photo object and the search tag table
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
    print('Attempting to find firebase api key in environmental variables')
    if os.environ.get('firebase_api_key') is None:
        raise Exception("No firebase api key found in environmental variables")
    print('Found firebase api key')
    
    print('Connecting to firebase')

    print(auth_user('tui43030@temple.edu', 'admin123'))

    photo_id = 'testPhotoId'
    tags = ['abc123', '123abc']

    # try:
    #     add_tags(platform='iOS', user_identifier='sebastiantota', photo_identifier=photo_id, tags=tags)
    # except Exception as e:
    #     print(e)
