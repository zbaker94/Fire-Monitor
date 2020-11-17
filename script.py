import threading
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
            
           
        callback_done.set()

    doc_ref = db.collection(collection).document(document)

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

db = firestore.Client()
listen_document('cities', 'SF')
listen_delay = 1
listen_msg = "listening..."

while True:
    sleep(listen_delay)
    print(listen_msg)
    listen_msg = "..."
    