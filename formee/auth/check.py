import os
from typing import Any

import yaml
from formee.auth.login import DEST_PATH
from formee.auth.validate import validate_user


def check_login() -> Any:
    """
    Args:
        None
    Returns:
        Any: Depends on the login status
    """
    if (os.path.isfile(DEST_PATH)):
        login_data = yaml.safe_load(open(DEST_PATH, 'r'))
        if login_data['visitor']:
            return None
        return validate_user(login_data['username'], login_data['password'])

    return False
