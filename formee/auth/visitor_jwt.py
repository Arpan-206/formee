import requests
def get_visitor_jwt():
    token = requests.get('https://formee-auth.hackersreboot.tech/visitor').json()['token']
    return token