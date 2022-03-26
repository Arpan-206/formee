from rich import print
from formee.formTools.read import read_form
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from formee.auth.user_jwt import get_user_jwt

transport = AIOHTTPTransport(url="https://hrbt-portal.hasura.app/v1/graphql",
                             headers={'Authorization': 'Bearer ' + get_user_jwt()})

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

initial_form_creation_query = gql("""
mutation CreateForm($description: String!, $title: String!) {
  insert_Form_one(object: {title: $title, description: $description}) {
    id
    description
    title
  }
}
""")

add_confirm_ques = gql("""
mutation AddConfirmQues($title: String!, $form: Int!) {
  insert_ques_confirm(objects: {title: $title, form: $form}) {
    returning {
      form
      id
      title
    }
  }
}
""")

add_number_ques = gql("""
mutation AddNumberQues($title: String!, $form: Int!) {
  insert_ques_number(objects: {title: $title, form: $form}) {
    returning {
      form
      id
      title
    }
  }
}
""")

add_options_ques = gql("""
mutation AddOptionsQues($form: Int!, $title: String!) {
  insert_ques_options(objects: {form: $form, title: $title}) {
    returning {
      form
      id
      title
    }
  }
}
""")

add_text_ques = gql("""
mutation AddTextQues($form: Int!, $title: String!) {
  insert_ques_text(objects: {form: $form, title: $title}) {
    returning {
      form
      title
      id
    }
  }
}
""")

add_choices = gql("""
mutation AddChoices($question: uuid!, $title: String!) {
  insert_option(objects: {title: $title, question: $question}) {
    returning {
      id
      question
      title
    }
  }
}
""")


def deploy():
    form_data = read_form()
    if form_data is None:
        print("[red]No form found. Exiting.")
        return
    print(form_data)
    retured_form_id = client.execute(initial_form_creation_query, variable_values={
        'title': form_data['name'], 'description': form_data['description']})['insert_Form_one']['id']

    for question in form_data['questions']:
        if question['type'] == 'Text' or question['type'] == 'Short Text':
            client.execute(add_text_ques, variable_values={
                           'form': retured_form_id, 'title': question['question']})
        elif question['type'] == 'Options':
            ques_id = client.execute(add_options_ques, variable_values={
                           'form': retured_form_id, 'title': question['question']})
            for choice in question['options']:
                client.execute(add_choices, variable_values={
                               'question': ques_id['insert_ques_options']['returning'][0]['id'], 'title': choice})
        elif question['type'] == 'Number':
            client.execute(add_number_ques, variable_values={
                           'form': retured_form_id, 'title': question['question']})
        elif question['type'] == 'Confirm':
            client.execute(add_confirm_ques, variable_values={
                           'form': retured_form_id, 'title': question['question']})
        else:
            print("[red]Invalid question type.")
            return

    return retured_form_id
