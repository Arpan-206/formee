from formee.auth.visitor_jwt import get_visitor_jwt
import requests


def validate_user(username, password):
    url = 'https://hrbt-portal.hasura.app/api/rest/user/'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + get_visitor_jwt()}
    body = {'username': username, 'password': password}
    response = requests.get(url, headers=headers, json=body).json()
    if len(response['User']) == 0:
        return False
    return response['User'][0]
