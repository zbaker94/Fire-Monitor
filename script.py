import threading
import json
from time import sleep
import os.path
from os import path

from getmac import get_mac_address as gma

from google.cloud import firestore

def Merge_Dict(dict1, dict2):
    if dict1 is not None:
        if dict2 is not None:
            return dict1 | dict2
        else: 
            return dict1
    else: 
        print("cannot merge 2 None values")
        return None

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
           
            settings_file = open("settings.json", "r")
            settings = settings_file.read()
            settings_dict = json.loads(settings)
            if data != settings_dict:
                print("updating settings.json: " + str(data))
                with open('settings.json', 'w') as fp:
                    json.dump(Merge_Dict(settings_dict, data), fp)
           
        callback_done.set()

    doc_ref = db.collection(collection).document(document)

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

db = firestore.Client()
### Create settings.json if it doesn't exist
if not path.exists('settings.json'):
    try:
        f = open('settings.json', 'w+')
        json.dump({}, f, indent = 4)
        print("Created settings.json")
        f.close()
    except FileNotFoundError:
        print("Could not create or find settings.json")
### get settings off disk
settings_file = open("settings.json", "r")
settings = settings_file.read()
settings_dict = json.loads(settings)
print('Found settings.json: ' + str(settings_dict))

### get/generate device id
device_id = gma()

if device_id not in settings_dict or settings_dict.device_id != device_id:
    print("Setting device id: " + str(device_id))
    settings_dict["device_id"] = device_id
    with open('settings.json', 'w') as fp:
        json.dump(settings_dict, fp)
### TODO check if document exists but if not, create it in `devices` collection

### listen to changes to device settings
listen_document('devices', 'GUID')
listen_delay = 1
listen_msg = "listening..."

while True:
    sleep(listen_delay)
    print(listen_msg)
    listen_msg = "..."
    