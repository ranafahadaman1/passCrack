"""
Simple Password Cracker (Multiprocessing Version)
A tool for demonstrating password cracking techniques as outlined
in the project proposal.

This script uses multiprocessing for true parallel execution on CPU-bound
hashing tasks, making it much faster than the threaded version.
"""

import argparse
import sys
import os
from hash_utils import hash_password
from dictionary_attack import dictionary_attack
from brute_force_attack import brute_force_attack
from configuration import MAX_BRUTE_FORCE_LENGTH, DEFAULT_CHARSET, MAX_PROCESSES, DEFAULT_HASH_ALGORITHM, ALLOWED_HASH_ALGORITHMS

def main():
    # Main function that handles command line arguments
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A simple password cracker tool (Multiprocessing).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  1. Hash a password:
     python password_cracker.py hash -p "mysecret" -a sha256

  2. Crack a hash using a dictionary:
     python password_cracker.py crack -H "..." -a sha256 -d wordlist.txt

  3. Crack a hash using brute-force (now much faster!):
     python password_cracker.py crack -H "..." -a md5 -b -c "abc" -l 5
"""
    )
    # Create sub-parsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parser for the hash command
    hash_parser = subparsers.add_parser(
        "hash", help="Hash a plaintext password.")
    hash_parser.add_argument(
        "-p", "--password",
        required=True,
        help="The plaintext password to hash."
    )
    hash_parser.add_argument(
        "-a", "--algorithm",
        default=DEFAULT_HASH_ALGORITHM,
        help=f"Hash algorithm (default: {DEFAULT_HASH_ALGORITHM}). E.g., md5, sha1, sha512."
    )

    # Parser for the crack command
    crack_parser = subparsers.add_parser(
        "crack", help="Crack a given password hash.")
    crack_parser.add_argument(
        "-H", "--hash",
        dest="target_hash",
        required=True,
        help="The target password hash to crack."
    )
    crack_parser.add_argument(
        "-a", "--algorithm",
        required=True,
        help="Hash algorithm used to create the hash (e.g., md5, sha256)."
    )
    crack_parser.add_argument(
        "-pr", "--processes",
        type=int,
        default=min(os.cpu_count() or 4, MAX_PROCESSES),
        help="Number of processes to use (default: all available cores, capped at max)."
    )

    # Group for attack type - one must be chosen
    attack_group = crack_parser.add_mutually_exclusive_group(required=True)
    attack_group.add_argument(
        "-d", "--dictionary",
        dest="wordlist_path",
        help="Path to the dictionary file for a dictionary attack."
    )
    attack_group.add_argument(
        "-b", "--brute-force",
        action="store_true",
        help="Enable brute-force attack."
    )

    # Arguments specific to brute-force
    brute_force_group = crack_parser.add_argument_group("Brute-Force Options")
    brute_force_group.add_argument(
        "-c", "--charset",
        default=DEFAULT_CHARSET,
        help="Character set for brute-force (default: 'abcdef...z')."
    )
    brute_force_group.add_argument(
        "-l", "--length",
        dest="max_length",
        type=int,
        default=MAX_BRUTE_FORCE_LENGTH,
        help=f"Maximum password length for brute-force (default: {MAX_BRUTE_FORCE_LENGTH})."
    )

    args = parser.parse_args()

    # Check if the algorithm is allowed
    if args.algorithm not in ALLOWED_HASH_ALGORITHMS:
        print(f"Error: Unsupported hash algorithm '{args.algorithm}'. Allowed: {ALLOWED_HASH_ALGORITHMS}")
        sys.exit(1)

    # Decide what to do based on the command
    if args.command == "hash":
        hashed_val = hash_password(args.password, args.algorithm)
        print(f"Password: {args.password}")
        print(f"Algorithm: {args.algorithm}")
        print(f"Hash: {hashed_val}")

    elif args.command == "crack":
        # Make sure we don't use too many processes
        args.processes = min(args.processes, MAX_PROCESSES)

        # Convert hash to lowercase for comparison
        args.target_hash = args.target_hash.lower()

        if args.wordlist_path:
            # Do dictionary attack
            dictionary_attack(
                args.target_hash,
                args.algorithm,
                args.wordlist_path,
                args.processes
            )
        elif args.brute_force:
            # Check if length is too long
            if args.max_length > MAX_BRUTE_FORCE_LENGTH:
                print(f"Warning: Max length {args.max_length} exceeds the configured limit of {MAX_BRUTE_FORCE_LENGTH}.")
                print("This could take a significant amount of time.")
                try:
                    choice = input("Continue? (y/n): ").lower()
                    if choice != 'y':
                        print("Attack cancelled.")
                        sys.exit(0)
                except KeyboardInterrupt:
                    print("\nAttack cancelled.")
                    sys.exit(0)

            # Do brute force attack
            brute_force_attack(
                args.target_hash,
                args.algorithm,
                args.charset,
                args.max_length,
                args.processes
            )


# This guard is ESSENTIAL for multiprocessing to work correctly!
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user. Exiting.")
        sys.exit(0)