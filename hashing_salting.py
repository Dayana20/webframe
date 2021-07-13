import hashlib
import os

password = 'password246'
salt = os.urandom(32)
# hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000 # It is recommended to use at least 100,000 iterations of SHA-256 
)

# Store them as:
storage = salt + key 
# Getting the values back out
salt_from_storage = storage[:32] # 32 is the length of the salt
key_from_storage = storage[32:]


password_to_check = 'password246' # The password provided by the user to check

# Use the exact same setup you used to generate the key, but this time put in the password to check
new_key = hashlib.pbkdf2_hmac(
    'sha256',
    password_to_check.encode('utf-8'), # Convert the password to bytes
    salt, 
    100000
)

if new_key == key:
    print('Password is correct')
else:
    print('Password is incorrect')

