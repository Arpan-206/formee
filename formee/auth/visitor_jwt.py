import requests


def get_visitor_jwt() -> str:
    """

    Returns:
        str: The JWT token for a visitor
    """
    token = requests.get(
        'https://formee-auth.hackersreboot.tech/visitor').json()['token']
    return token
