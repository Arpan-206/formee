import os

import yaml
from PyInquirer import prompt
from rich import print

from formee.auth.validate import validate_user
from formee.auth.hasher import hash_password
DEST_DIR = os.path.expanduser('~')
DEST_PATH = os.path.join(DEST_DIR, '.formee.yml')


def login():
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
    usr_logged_in = validate_user(
        answers['username'], answers['password'])

    if not usr_logged_in:
        print(
            f"[red]User {answers['username']} not logged in. Try new username.")
        login()

    else:
        yaml.dump({'username': answers['username'], 'password': answers['password'], 'visitor': False},
                  open(DEST_PATH, 'w'))
        print(
            f"[green]User {answers['username']} logged in successfully.")
        return True
