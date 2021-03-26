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
    except:
        return False


if __name__ == '__main__':
    print('Connecting to firebase')
    # print(auth_user('', ''))

    data = db.child('iOS/sebastiantota/').get()

    for user in data.each():
        print(user.key())
        print(user.val())
