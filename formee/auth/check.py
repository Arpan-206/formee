import os
import yaml

from formee.auth.validate import validate_user
from formee.auth.login import DEST_PATH


def check_login():
    if (os.path.isfile(DEST_PATH)):
        login_data = yaml.safe_load(open(DEST_PATH, 'r'))
        if login_data['visitor']:
            return None
        return validate_user(login_data['username'], login_data['password'])
    
    return False
