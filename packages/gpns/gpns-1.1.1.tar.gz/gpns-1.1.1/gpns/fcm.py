import firebase_admin
from firebase_admin import messaging, credentials


def setup(service_account_key_file):
    cred = credentials.Certificate(service_account_key_file)
    firebase_admin.initialize_app(cred)


# https://firebase.google.com/docs/cloud-messaging/send-message#python
def send_message(registration_token, data):
    # See documentation on defining a message payload.
    message = messaging.Message(
        data=data,
        token=registration_token,
    )
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
