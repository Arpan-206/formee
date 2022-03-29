import yaml
from PyInquirer import prompt
from rich import print


def create_form() -> None:
    initial_details = prompt([
        {
            'type': 'input',
            'name': 'name',
            'message': 'Enter the name of the form:',
            'validate': lambda val: val != '' and len(val) <= 20
        },
        {
            'type': 'input',
            'name': 'description',
            'message': 'Enter the description of the form:',
            'validate': lambda val: val != '' and len(val) <= 1000
        }
    ])
    questions = create_questions()
    form = {
        'name': initial_details['name'],
        'description': initial_details['description'],
        'gen_detail': 'formee_beta',
        'questions': questions
    }
    yaml.dump(form, open(initial_details['name'].lower(
    ).strip().replace(' ', '-') + '.yaml', 'w'))
    print(f"[green]Form created successfully.")


def create_questions() -> list:
    """
    Returns:
        list: Questions to be asked in the form
    """
    questions = []
    question_prompt = [
        {
            'type': 'input',
            'name': 'question',
            'message': 'Enter the question:',
            'validate': lambda val: val != '' and len(val) <= 100
        },
        {
            'type': 'list',
            'name': 'type',
            'message': 'Enter the type of the question:',
            'choices': ['Text', 'Number', 'Confirm', 'Options']
        },
        {
            'type': 'confirm',
            'name': 'required',
            'message': 'Is this question required?',
            'default': True
        }
    ]

    while True:
        question = prompt(question_prompt)
        if question['type'] == 'Options':
            question['options'] = prompt([
                {
                    'type': 'input',
                    'name': 'options',
                    'message': 'Enter the options [Seperate using *;*]:',
                    'validate': lambda val: val != '' and len(val) <= 100,
                    'filter': lambda val: list(map(lambda x: x.strip(), val.split(';')))
                }
            ])['options']
        questions.append(question)
        confirmation = prompt([
            {
                'type': 'confirm',
                'name': 'continue',
                'message': 'Do you want to add more questions?'
            }
        ])
        if not confirmation['continue']:
            break

    return questions
