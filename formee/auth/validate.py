from typing import Any

import requests
from formee.auth.visitor_jwt import get_visitor_jwt


def validate_user(username: str, password: str) -> Any:
    """
    Args:
        username (str): Username of the user to be validated
        password (str): Password of the user to be validated

    Returns:
        Any: False when user is not validated, else the user data
    """
    url = 'https://hrbt-portal.hasura.app/api/rest/user/'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + get_visitor_jwt()}
    body = {'username': username, 'password': password}
    response = requests.get(url, headers=headers, json=body).json()
    if len(response['User']) == 0:
        return False
    return response['User'][0]
