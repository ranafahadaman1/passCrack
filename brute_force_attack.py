import itertools
import time
from multiprocessing import Pool, Manager, Event
from multiprocessing_utils import init_worker, found_password_event, hash_func


def check_brute_force_task(prefix, charset, length_to_gen, target_hash):
    import multiprocessing_utils
    # Check brute force combinations
    if multiprocessing_utils.hash_func is None:
        return None

    combinations = itertools.product(charset, repeat=length_to_gen)

    if length_to_gen == 0:
        if multiprocessing_utils.found_password_event.is_set():
            return None
        if multiprocessing_utils.hash_func(prefix.encode('utf-8')).hexdigest() == target_hash:
            multiprocessing_utils.found_password_event.set()
            return prefix
        return None

    for combo_tuple in combinations:
        if multiprocessing_utils.found_password_event.is_set():
            return None

        password = prefix + "".join(combo_tuple)
        if multiprocessing_utils.hash_func(password.encode('utf-8')).hexdigest() == target_hash:
            multiprocessing_utils.found_password_event.set()
            return password
    return None


def brute_force_attack(target_hash, algorithm, charset, max_length, num_processes):
    # Do brute force attack with multiple processes
    print(f"\nStarting brute-force attack on {target_hash}...")
    print(f"Using charset: '{charset}'")
    print(f"Max length: {max_length}")
    print(f"Using {num_processes} processes.")
    start_time = time.time()
    found = None

    with Manager() as manager, Pool(processes=num_processes, initializer=init_worker, initargs=(manager.Event(), algorithm)) as pool:
        for length in range(1, max_length + 1):
            if found:
                break

            print(f"Checking passwords of length {length}...")

            if length == 1:
                tasks = [(char, charset, 0, target_hash) for char in charset]
            else:
                tasks = [(char, charset, length - 1, target_hash) for char in charset]

            if not tasks:
                continue

            try:
                for result in pool.starmap(check_brute_force_task, tasks):
                    if result:
                        found = result
                        pool.terminate()
                        pool.join()
                        break
            except KeyboardInterrupt:
                print("\nBrute-force attack interrupted.")
                pool.terminate()
                pool.join()
                found = "INTERRUPTED"
                break

    end_time = time.time()
    total_time = end_time - start_time

    if found and found != "INTERRUPTED":
        print(f"\nSUCCESS: Password found!")
        print(f"Password: {found}")
    elif not found:
        print(f"\nFAILED: Password not found (up to length {max_length}).")

    print(f"Time elapsed: {total_time:.2f} seconds.")
    return found