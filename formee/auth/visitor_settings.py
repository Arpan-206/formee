import yaml 
from formee.auth.login import DEST_PATH

def load_visitor_settings():
    yaml.dump({'visitor': True}, open(DEST_PATH, 'w'))