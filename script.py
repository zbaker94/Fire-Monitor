import threading
import json
from time import sleep
import os
import os.path
from os import path

from getmac import get_mac_address as gma
from google.cloud import firestore

db = firestore.Client()
doc_ref = None


def log(msg):
    print(msg)
    print("__________________________________________")

def Merge_Dict(dict1, dict2):
    log("merging " + str(dict1) + " with " + str(dict2))
    if dict1 is not None:
        if dict2 is not None:
            for key in dict1.keys():
                if key not in dict2:
                    dict2[key] = dict1[key]
            return dict2
        else: 
            return dict1
    else: 
        log("cannot merge 2 None values")
        return None

def listen_document(collection, document):
    
    log("listening to document")
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            log(f'Received document snapshot: {doc.id}')
            data = doc.to_dict()
           
            settings_file = open("settings.json", "r")
            settings = settings_file.read()
            settings_dict = json.loads(settings)
            if data != settings_dict:
                log("updating settings.json: " + str(data))
                merged = Merge_Dict(settings_dict, data)
                settings_dict = merged
                with open('settings.json', 'w') as fp:
                    json.dump(merged, fp)
                ### update status of lamp based on changes
           
        callback_done.set()

    doc_ref = db.collection(collection).document(document)

    # Watch the document
    doc_ref.on_snapshot(on_snapshot)

### Create settings.json if it doesn't exist
if not path.exists('settings.json'):
    try:
        f = open('settings.json', 'w+')
        json.dump({"on": True, "nickname": "", "colors": []}, f, indent = 4)
        log("Created settings.json")
        f.close()
    except FileNotFoundError:
        log("Could not create or find settings.json")
### get settings off disk
settings_file = open("settings.json", "r")
settings = settings_file.read()
settings_dict = json.loads(settings)
log('Found settings.json: ' + str(settings_dict))

### get/generate device id
device_id = gma()

### if device Id is not in settings, add it.
if device_id not in settings_dict.values():
    log("Setting device id: " + str(device_id))
    settings_dict["device_id"] = device_id
    with open('settings.json', 'w') as fp:
        json.dump(settings_dict, fp)

### check if document exists but if not, create it in `devices` collection. If so, use that config
document_name = 'device_' + str(device_id)
doc_ref = db.collection("devices").document(document_name)
doc = doc_ref.get()
if doc.exists:
    log("Document " + document_name + " exists in devices collection. Updating settings.json")
    new_settings = doc.to_dict()
    log(str(new_settings))
    merged_settings = Merge_Dict(settings_dict, new_settings)
    with open('settings.json', 'w') as fp:
        json.dump(merged_settings, fp)
        doc_ref.set(merged_settings)
else:
    log("Document " + document_name + " does not exist in devices collection")
    log("Creating now...")
    db.collection(u'devices').document(document_name).set(settings_dict)
    
### listen to changes to device settings
listen_document('devices', document_name)
listen_delay = 1
listen_msg = document_name + "..."

while True:
    sleep(listen_delay)
    print(listen_msg)
    listen_msg = "..."
    