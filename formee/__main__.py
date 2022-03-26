import sys

# Importing third party modules
from pyfiglet import Figlet
from PyInquirer import Separator, prompt
from rich import print

from formee.auth.check import check_login
from formee.auth.login import login
from formee.auth.register import registerPrompt
from formee.auth.user_jwt import get_user_jwt
from formee.auth.visitor_settings import load_visitor_settings

def main():
    # Loading the title
    title = Figlet(font='slant')
    print(f"[red]{title.renderText('Formee')}")
    if not check_login():
        register_or_login = prompt([
            {
                'type': 'list',
                'name': 'register_or_login',
                'message': 'What do you want to do?',
                'choices': ['Register', 'Login', 'I\'m just visiting', Separator(), 'Exit']
            }
        ])
        if register_or_login['register_or_login'] == 'Register':
            registerPrompt()
        elif register_or_login['register_or_login'] == 'Login':
            login()
        elif register_or_login['register_or_login'] == 'I\'m just visiting':
            load_visitor_settings()
        elif register_or_login['register_or_login'] == 'Exit':
            sys.exit()

    usr_data = check_login()
    if usr_data is None:
        print(f"[green]Hi Visitor!")
    else:
        print("[blue] Welcome to Formee! Logged in as [bold]{}".format(
        usr_data['username']))
    # Loading the questions
    action = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': [
                Separator('= Create ='),
                {
                    'name': 'Create a new form'
                },
                Separator('= View Form Data ='),
                {
                    'name': 'View a form file\'s data'
                },
                Separator('= Try a form ='),
                {
                    'name': 'Try a form from a file'
                },
                Separator('= Fill a form ='),
                {
                    'name': 'Fill a form from an ID'
                },
                Separator('= Deploy a form ='),
                {
                    'name': 'Deploy a form'
                },
                Separator('= Exit ='),
                {
                    'name': 'Exit'
                },
            ]
        }
    ]
    # Asking the questions
    answers = prompt(action)
    # Checking the answers
    if answers['action'] == 'Exit':
        sys.exit(1)
    elif answers['action'] == 'Create a new form':
        from formee.formTools.create import create_form
        create_form()
        sys.exit(0)
    elif answers['action'] == 'View a form file\'s data':
        from formee.formTools.read import display_form_data
        display_form_data()
        sys.exit(0)
    elif answers['action'] == 'Try a form from a file':
        from formee.formTools.read import try_form
        try_form()
        sys.exit(0)
    elif answers['action'] == 'Deploy a form':
        if usr_data:
            from formee.formTools.deploy import deploy
            deploy()
            sys.exit(0)
        else:
            print("[red]You must be logged in to deploy a form.")
            sys.exit(1)
    elif answers['action'] == 'Fill a form from an ID':
        from formee.formTools.fill import fill_prompt
        fill_prompt()
        sys.exit(0)

if __name__ == '__main__':
    main()