import threading
import json
from time import sleep

from google.cloud import firestore


def listen_document(collection, document):
    db = firestore.Client()
    print("listening to document")
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')
            data = doc.to_dict()
            
            if data != json.loads(settings):
                print("updating settings.json: " + str(data))
                with open('settings.json', 'w') as fp:
                    json.dump(data, fp)
           
        callback_done.set()

    doc_ref = db.collection(collection).document(document)

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

db = firestore.Client()
### TODO get/generate device id
### TODO check if document exists but if not, create it in `devices` collection

### listen to changes to device settings
listen_document('devices', 'GUID')
listen_delay = 1
listen_msg = "listening..."
settings_file = open("settings.json", "r")
settings = settings_file.read()
print('Found settings.json: ' + str(settings_file.read()))

while True:
    sleep(listen_delay)
    print(listen_msg)
    listen_msg = "..."
    