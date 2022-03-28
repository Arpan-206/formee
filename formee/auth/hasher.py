import hashlib


def hash_password(password: str) -> str:
    """
    Args:
        password (str): The password to be hashed

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
