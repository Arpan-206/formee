import json
from formee.auth.check import check_login
from formee.formTools.fill import get_form_details
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from PyInquirer import prompt
from rich import print
from formee.auth.user_jwt import get_user_jwt
from rich.table import Table
import yaml
get_answers_query = gql("""
query GetAnswers($_eq: Int = 16) {
  answers(where: {Form: {id: {_eq: $_eq}}}) {
    data
    filled_by
    form
    form_creator
    id
  }
}
""")


def get_responses() -> None:
    user_data = check_login()
    if not user_data:
        print("[red]You must be logged in to view responses.")
        return
    transport = AIOHTTPTransport(url="https://hrbt-portal.hasura.app/v1/graphql",
                                 headers={'Authorization': 'Bearer ' + get_user_jwt()})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    form_id = prompt([{
        'type': 'input',
        'name': 'form_id',
        'message': 'Enter the form id:',
        'validate': lambda val: val != ''
    }])['form_id']

    form_details = get_form_details(form_id)

    if not form_details:
        print(f"[red]Form with id {form_id} not found.")
        get_responses()

    if user_data['username'] == form_details['User']['username']:
        print(f"[green]Loading response to {form_details['title']}")
        form_responses = client.execute(
            get_answers_query, variable_values={'_eq': form_id})['answers']

        mode_of_display = prompt([{
            'type': 'list',
            'name': 'mode',
            'message': 'Select the mode of display:',
            'choices': ['Table', 'JSON', 'Write to JSON file', 'Write to YAML file', 'Cancel']
        }])['mode']

        if mode_of_display == 'Table':
            table = Table(title=f"{form_details['title']}")
            table.add_column('ID', style='green')
            table.add_column('Filled By', style='green')
            table.add_column('Form', style='green')
            table.add_column('Form Creator', style='green')
            table.add_column('Data', style='green')
            for response in form_responses:
                table.add_row(str(response['id']), response['filled_by'],
                              str(response['form']), response['form_creator'], str(response['data']))
            print(table)
        elif mode_of_display == 'JSON':
            print(json.dumps(form_responses, indent=4))
        elif mode_of_display == 'Write to JSON file':
            file_name = prompt([{
                'type': 'input',
                'name': 'file_name',
                'message': 'Enter the file name:',
                'validate': lambda val: val != ''
            }])['file_name']
            with open(file_name, 'w') as file:
                file.write(json.dumps(form_responses, indent=4))
                print(f"[green]Successfully wrote to {file_name}")
        elif mode_of_display == 'Write to YAML file':
            file_name = prompt([{
                'type': 'input',
                'name': 'file_name',
                'message': 'Enter the file name:',
                'validate': lambda val: val != ''
            }])['file_name']
            with open(file_name, 'w') as file:
                file.write(yaml.dump(form_responses, default_flow_style=False))
                print(f"[green]Successfully wrote to {file_name}")
        else:
            print("[red]Cancelled.")

    else:
        print(f"[red]You can only view responses to your own forms.")
        get_responses()

    return