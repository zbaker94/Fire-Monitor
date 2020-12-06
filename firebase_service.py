from google.cloud import firestore
from logging_service import log
import os

db = None
doc_ref = None
document_name = None

def init_firebase(name):
    global doc_ref 
    global db
    global document_name
    os.system('export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"')
    db = firestore.Client()
    document_name = name
    doc_ref = db.collection("devices").document(document_name)

def get_firebase():
    global doc_ref
    print(log(doc_ref))
    return doc_ref.get()

def set_firebase(value):
    global doc_ref
    global document_name
    global db
    if(doc_ref == None):
        doc_ref = db.collection(u'devices').document(document_name)
    doc_ref.set(value)

def set_snapshot_callback(on_snapshot):
    global doc_ref
    doc_ref.on_snapshot(on_snapshot)