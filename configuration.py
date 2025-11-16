# Configuration settings for the password cracker
# You can change these values to customize the tool

# Default hash algorithm - sha256 is secure and common
DEFAULT_HASH_ALGORITHM = "sha256"

# Maximum length for brute-force attacks - don't set too high or it takes forever
MAX_BRUTE_FORCE_LENGTH = 8

# Default character set for brute-force - lowercase letters
DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyz"

# Maximum number of processes to use - based on your CPU cores
MAX_PROCESSES = 16

# Allowed hash algorithms - only these are supported
ALLOWED_HASH_ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]