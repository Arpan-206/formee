from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    """
    Args:
        password (str): The password to be hashed

    Returns:
        str: Hashed password
    """
    ph = PasswordHasher()
    return ph.hash(password)
