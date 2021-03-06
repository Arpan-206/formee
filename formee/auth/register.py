import os

import requests
import yaml
from formee.auth.hasher import hash_password
from formee.auth.login import DEST_PATH
from formee.auth.visitor_jwt import get_visitor_jwt
from PyInquirer import prompt
from rich import print


def registerPrompt() -> None:
    """
    """
    questions = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter your username:',
            'validate': lambda val: val != ''
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter your password:',
            'validate': lambda val: val != '',
            'filter': lambda val: hash_password(val)
        },
    ]
    answers = prompt(questions)
    usr_registered = register(answers['username'], answers['password'])
    if usr_registered:
        print(f"[green]User {answers['username']} registered successfully.")
    else:
        print(
            f"[red]User {answers['username']} not registered. Try new username.")
        registerPrompt()


def register(username: str, password: str) -> bool:
    """

    Args:
        username (str): Username of the user to be registered
        password (str): Password of the user to be registered

    Returns:
        bool: True when registration is successful
    """
    url = 'https://hrbt-portal.hasura.app/api/rest/createUser'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + get_visitor_jwt()}
    body = {'username': username, 'password': password}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        yaml.dump({'username': username, 'password': password, 'visitor': False},
                  open(DEST_PATH, 'w'))

    return response.status_code == 200
