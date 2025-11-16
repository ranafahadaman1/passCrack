import hashlib
from multiprocessing import Event

# Globals for workers
found_password_event = None
hash_func = None

def init_worker(event, algorithm):
    # Set up the worker
    global found_password_event, hash_func
    found_password_event = event
    try:
        hash_func = getattr(hashlib, algorithm)
    except AttributeError:
        print(f"Error: Invalid hash algorithm '{algorithm}' in worker.")
        hash_func = None