import hashlib


def hash_string(input_string):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Assume the input string is UTF-8 encoded. You can use another encoding if you expect it.
    encoded_string = input_string.encode('utf-8')

    # Update the hash object with the bytes of the string
    hash_object.update(encoded_string)

    # Get the hexadecimal representation of the digest
    hex_dig = hash_object.hexdigest()

    return hex_dig
