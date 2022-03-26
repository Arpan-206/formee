from PyInquirer import prompt
from rich import print
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from formee.auth.user_jwt import get_user_jwt
import json
from formee.auth.check import check_login
from formee.formTools.validators import NumberValidator
transport = AIOHTTPTransport(url="https://hrbt-portal.hasura.app/v1/graphql",
                             headers={'Authorization': 'Bearer ' + get_user_jwt()})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

get_form_details_query = gql("""
query GetForm($id: Int!) {
  Form_by_pk(id: $id) {
    User {
      username
    }
    id
    description
    title
    ques_confirms {
      title
    }
    ques_numbers {
      title
    }
    ques_options {
      title
      options {
        title
      }
    }
    ques_texts {
      title
    }
  }
}
""")

answer_mutation = gql("""
mutation AnswerForm($data: json!, $form: Int!, $filled_by: String) {
  insert_answers_one(object: {data: $data, form: $form, filled_by: $filled_by}) {
    data
    filled_by
    form
    id
  }
}""")


def get_form_details(id):
    return client.execute(get_form_details_query, variable_values={"id": id})['Form_by_pk']


def fill_prompt():
    questions = [
        {
            'type': 'input',
            'name': 'form_id',
            'message': 'Enter the form id:',
            'validate': lambda val: val != ''
        },
    ]
    answers = prompt(questions)
    form_details = get_form_details(answers['form_id'])
    if not form_details:
        print(f"[red]Form with id {answers['form_id']} not found.")
        fill_prompt()
    print("\n")
    print(f"[blue] Filling form {form_details['title']}")
    print(f"[yellow] Created by {form_details['User']['username']}")
    print(f"[green] Description: {form_details['description']}")

    ques_answers = {}
    for ques in form_details['ques_texts']:
        ques_answers[ques['title']] = prompt([{
            'type': 'input',
            'name': ques['title'],
            'message': ques['title'],
            'validate': lambda val: val != '' and len(val) <= 1000
        }])[ques['title']]
    for ques in form_details['ques_numbers']:
        ques_answers[ques['title']] = prompt([{
            'type': 'input',
            'name': ques['title'],
            'message': ques['title'],
            'validate': NumberValidator
        }])[ques['title']]
    for ques in form_details['ques_options']:
        ques_answers[ques['title']] = prompt([{
            'type': 'list',
            'name': ques['title'],
            'message': ques['title'],
            'choices':  [opt['title'] for opt in ques['options']]
        }])[ques['title']]
    for ques in form_details['ques_confirms']:
        ques_answers[ques['title']] = prompt([{
            'type': 'confirm',
            'name': ques['title'],
            'message': ques['title']
        }])[ques['title']]

    print("\n")
    usr_data = check_login()

    if usr_data is None:
        usrname = 'Anonymous'
    else:
        usrname = usr_data['username']
    answer_return = client.execute(answer_mutation, variable_values={"data": json.dumps(
        ques_answers), "form": form_details['id'], "filled_by": usrname})['insert_answers_one']
    print(f"[green] Form filled successfully.")

    return answer_return
