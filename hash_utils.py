import hashlib
import sys

def hash_password(password, algorithm='sha256'):
    # Hash a password with the given algorithm
    try:
        hash_func_local = getattr(hashlib, algorithm)
    except AttributeError:
        print(f"Error: Hash algorithm '{algorithm}' not supported by hashlib.")
        sys.exit(1)

    password_bytes = password.encode('utf-8')
    hash_obj = hash_func_local(password_bytes)
    return hash_obj.hexdigest()