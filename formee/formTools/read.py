from yaml.parser import ParserError
import yaml
from rich import print
from PyInquirer import prompt, Validator, ValidationError
from formee.formTools.validators import NumberValidator
def read_form():
    form_path = prompt([
        {
            'type': 'input',
            'name': 'form_path',
            'message': 'Enter the path to the form:',
            'validate': lambda val: val != '' and len(val) <= 20
        }
    ])
    form = read_form_file(form_path['form_path'])
    if form == 'Invalid YAML file':
        print(f"[red]It is not a valid YAML File.")
        read_form()
    elif form == 'File not found':
        print(f"[red]File not found.")
        read_form()
    elif form == 'Invalid content in YAML file':
        print(f"[red]Invalid content in YAML file.")
        read_form()
    return form

def display_form_data():
    form = read_form()
    print(f"\n[bold]Name: {form['name']}")
    print(f"Description: {form['description']}")
    print(f"Generated by: {form['gen_detail']}")
    print(f"\n[bold]Questions:")
    for question in form['questions']:
        print(f"\n[bold]Question: {question['question']}")
        print(f"Type: {question['type']}")
        if question['type'] == 'Options':
            print(f"Options: {question['options']}")
        print(f"Required: {question['required']}")

def read_form_file(form_path):
    try:
        form = yaml.safe_load(open(form_path, 'r'))
        try:
            form['name']
            form['description']
            form['questions']
            form['gen_detail']
        except KeyError:
            return 'Invalid content in YAML file'
    except ParserError:
        return 'Invalid YAML file'
    except FileNotFoundError:
        return 'File not found'
    return form

def try_form():
    form = read_form()
    form_data = {}

    class InputValidator(Validator):
        def validate(self, document):
            try:
                form['questions']
            except KeyError:
                raise ValidationError(
                    message='Invalid content in YAML file',
                    cursor_position=len(document.text)
                )
    for question in form['questions']:
        if question['type'] == 'Text':
            form_data[question['question']] = prompt([
                {
                    'type': 'input',
                    'name': question['question'],
                    'message': question['question'],
                    'validate': lambda val: val != '' and len(val) <= 100
                }
            ])
        elif question['type'] == 'Short Text':
            form_data[question['question']] = prompt([
                {
                    'type': 'input',
                    'name': question['question'],
                    'message': question['question'],
                    'validate': lambda val: val != '' and len(val) <= 20
                }
            ])
        elif question['type'] == 'Number':
            form_data[question['question']] = prompt([
                {
                    'type': 'input',
                    'name': question['question'],
                    'message': question['question'],
                    'validate': NumberValidator
                }
            ])
        elif question['type'] == 'Confirm':
            form_data[question['question']] = prompt([
                {
                    'type': 'confirm',
                    'name': question['question'],
                    'message': question['question'],
                    'default': False
                }
            ])
        elif question['type'] == 'Email':
            form_data[question['question']] = prompt([
                {
                    'type': 'input',
                    'name': question['question'],
                    'message': question['question'],
                    'validate': lambda val: val != '' and len(val) <= 100
                }
            ])
        elif question['type'] == 'Options':
            form_data[question['question']] = prompt([
                {
                    'type': 'list',
                    'name': question['question'],
                    'message': question['question'],
                    'choices': question['options']
                }
            ])