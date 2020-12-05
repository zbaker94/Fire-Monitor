import threading
import json
from time import sleep
import os
import os.path
from os import path

from getmac import get_mac_address as gma

from colors_service import set_color
from settings_service import get_settings, init_settings, update_settings
from logging_service import log
from firebase_service import init_firebase, get_firebase, set_firebase, set_snapshot_callback

def update_colors(settings_colors):
    colors = []
    for color in settings_colors:
        colors.append(eval(color))
    log("new colors: " + str(colors))
    set_color(colors)

def update_power_status(status):
    # turn of / on LEDS
    log("setting power status to " + str(status))
    
def update_lights(settings):
    if(settings['colors'] != None):
        update_colors(settings['colors'])
    if settings['on'] != None:
        update_power_status(settings['on'])

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
           
            settings_dict = get_settings()
            if data != settings_dict:
                log("updating settings.json: " + str(data))
                merged = Merge_Dict(settings_dict, data)
                settings_dict = merged
                with open('settings.json', 'w') as fp:
                    json.dump(merged, fp)
                ### update status of lamp based on changes
                update_lights(merged)
        callback_done.set()

    # Watch the document
    set_snapshot_callback(on_snapshot)

### Create settings.json if it doesn't exist
init_settings()
### get settings off disk
settings_dict = get_settings()
log('Found settings.json: ' + str(settings_dict))

### get/generate device id
device_id = gma()
document_name = 'device_' + str(device_id)

### init firebase connection
init_firebase(document_name)

### if device Id is not in settings, add it.
if device_id not in settings_dict.values():
    log("Setting device id: " + str(device_id))
    update_settings("device_id", device_id, settings_dict)

### check if document exists but if not, create it in `devices` collection. If so, use that config
doc = get_firebase()
if doc.exists:
    log("Document " + document_name + " exists in devices collection. Updating settings.json")
    new_settings = doc.to_dict()
    log(str(new_settings))
    merged_settings = Merge_Dict(settings_dict, new_settings)
    settings_dict = merged_settings
    with open('settings.json', 'w') as fp:
        json.dump(merged_settings, fp)
        set(merged_settings)
else:
    log("Document " + document_name + " does not exist in devices collection")
    log("Creating now...")
    set_firebase(settings_dict)

# Update device based on settings
update_lights(settings_dict)

### listen to changes to device settings
listen_document('devices', document_name)
listen_delay = 1
listen_msg = document_name + "..."

while True:
    sleep(listen_delay)
    print(listen_msg)
    listen_msg = "..."
    