import requests
from formee.auth.check import check_login


def get_user_jwt() -> str:
    """
    Returns:
        str: The JWT token of the user
    """
    login_data = check_login()
    if not login_data:
        token = requests.get(
            'https://formee-auth.hackersreboot.tech/visitor').json()['token']
        return token

    if login_data:
        token = requests.get('https://formee-auth.hackersreboot.tech/', json={
                             'username': login_data['username'], 'password': login_data['password']}).json()['token']
        return token
