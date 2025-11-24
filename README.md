# Simple Password Cracker

This project is a simple password cracking tool for demonstrating hashing, dictionary attacks, and brute-force attacks in Python.

## Features

* **Hashing**: Hash passwords using MD5, SHA-256, SHA-1, etc.
* **Dictionary Attack**: Crack hashes by checking against a wordlist, using multiple processes.
* **Brute-Force Attack**: Try all combinations up to a set length, using multiple processes.
* **Command-Line Interface**: Easy to use with options.

## Dependencies

Uses Python standard libraries plus:

Install dependencies:
```bash
pip install -r requirements.txt
```

Works with Python 3.6+.

## Versions

- **Main Project**: Uses standard `hashlib` for hashing.
- **`manual_crypto/`**: Complete manual implementation using custom hash functions. See `manual_crypto/README.md` for details.

## How to Run

Run with `python password_cracker.py`. Use `hash` to hash passwords or `crack` to try cracking.

Get help:
`python password_cracker.py --help`

## Stopping Long-Running Processes

Cracking operations, especially brute-force attacks, can run for extended periods. To stop them:

- Press `Ctrl+C` to interrupt the program gracefully
- If the terminal doesn't exit or respond, you may need to kill the terminal process to stop execution

---

### 1. Hashing a Password

Use the `hash` command to hash a password.

**Command:**
`python password_cracker.py hash -p "your_password" -a "algorithm"`

**Example (SHA-256):**
```bash
python password_cracker.py hash -p "password123" -a "sha256"
```
**Output:**
```
Password: password123
Algorithm: sha256
Hash: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
```

**Example (MD5):**
```bash
python password_cracker.py hash -p "admin" -a "md5"
```
**Output:**
```
Password: admin
Algorithm: md5
Hash: 21232f297a57a5a743894a0e4a801fc3
```

---

### 2. Cracking a Hash

Use the `crack` command for attacks. The hash algorithm will be automatically detected from the hash length if not specified.

#### A. Dictionary Attack

Checks hashes against a wordlist file.

First, hash a known password:
```bash
python password_cracker.py hash -p "test" -a "sha256"
```
**Output:**
```
Password: test
Algorithm: sha256
Hash: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

Now crack it (algorithm auto-detected):
```bash
python password_cracker.py crack -H "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" -d "wordlist.txt"
```
**Output:**
```
Probable hash algorithm: sha256
Starting dictionary attack on 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08...
Using 12 processes.

SUCCESS: Password found!
Password: test
Time elapsed: 1.48 seconds.
```

Or specify algorithm explicitly:
```bash
python password_cracker.py crack -H "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" -a "sha256" -d "wordlist.txt"
```

#### B. Brute-Force Attack

Tries all combinations up to a max length.

Hash a short password:
```bash
python password_cracker.py hash -p "abc" -a "md5"
```
**Output:**
```
Password: abc
Algorithm: md5
Hash: 900150983cd24fb0d6963f7d28e17f72
```

Crack with brute-force (algorithm auto-detected):
```bash
python password_cracker.py crack -H "900150983cd24fb0d6963f7d28e17f72" -b -l 3
```
**Output:**
```
Probable hash algorithm: md5
Starting brute-force attack on 900150983cd24fb0d6963f7d28e17f72...
Using charset: 'abcdefghijklmnopqrstuvwxyz'
Max length: 3
Using 12 processes.
Checking passwords of length 1...
Checking passwords of length 2...
Checking passwords of length 3...

SUCCESS: Password found!
Password: abc
Time elapsed: 0.01 seconds.
```

Or specify algorithm explicitly:
```bash
python password_cracker.py crack -H "900150983cd24fb0d6963f7d28e17f72" -a "md5" -b -l 3
```

## Configuration

Settings like max length and allowed algorithms are in `configuration.py`. You can change them there.

## Hash Algorithm Detection

When cracking hashes, the algorithm is automatically detected based on hash length:
- **32 characters**: MD5
- **40 characters**: SHA-1  
- **64 characters**: SHA-256

If the hash length doesn't match any supported algorithm, you'll need to specify it with `-a`.
```