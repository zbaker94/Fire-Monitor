import os.path
from os import path
import json
from logging_service import log

settings = None

default_settings = {
    "on": True, 
    "nickname": "", 
    "colors": ["(255,255,255)"], 
    "lightCount": 52
}

def get_settings():
    global settings
    settings_file = open("settings.json", "r")
    settings = settings_file.read()
    return json.loads(settings)

def init_settings():
    global default_settings
    if not path.exists('settings.json'):
        try:
            f = open('settings.json', 'w+')
            json.dump(default_settings, f, indent = 4)
            log("Created settings.json")
            f.close()
        except FileNotFoundError:
            log("Could not create or find settings.json")

def update_settings(key, value, settings_dict):
    settings_dict[key] = value
    with open('settings.json', 'w') as fp:
        json.dump(settings_dict, fp)