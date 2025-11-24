import time
from multiprocessing import Pool, Manager, Event
from multiprocessing_utils import init_worker, found_password_event, hash_func


def check_dictionary_chunk(password_chunk, target_hash):
    import multiprocessing_utils

    # Check a list of passwords against the hash
    if multiprocessing_utils.hash_func is None:
        return None

    for password in password_chunk:
        if multiprocessing_utils.found_password_event.is_set():
            return None

        if (
            multiprocessing_utils.hash_func(password.encode("utf-8")).hexdigest()
            == target_hash
        ):
            multiprocessing_utils.found_password_event.set()
            return password

    return None


def dictionary_attack(target_hash, algorithm, wordlist_path, num_processes):
    # Do dictionary attack with multiple processes
    print(f"\nStarting dictionary attack on {target_hash}...")
    print(f"Using {num_processes} processes.")
    start_time = time.time()

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            words = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: Wordlist file not found at '{wordlist_path}'")
        return None
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        return None

    if not words:
        print("Error: Wordlist is empty.")
        return None

    # Split into chunks
    chunk_size = (len(words) + num_processes - 1) // num_processes
    password_chunks = [
        words[i : i + chunk_size] for i in range(0, len(words), chunk_size)
    ]
    print(f"Total passwords: {len(words)}")

    found = None
    with Manager() as manager:
        with Pool(
            processes=num_processes,
            initializer=init_worker,
            initargs=(manager.Event(), algorithm),
        ) as pool:
            # Start tasks
            tasks = [(chunk, target_hash) for chunk in password_chunks]
            results = pool.starmap(check_dictionary_chunk, tasks)

            # Check for found password
            for result in results:
                if result:
                    found = result
                    break

    end_time = time.time()
    total_time = end_time - start_time

    if found:
        print(f"\nSUCCESS: Password found!")
        print(f"Password: {found}")
    else:
        print(f"\nFAILED: Password not found in wordlist.")

    print(f"Time elapsed: {total_time:.2f} seconds.")
    return found
