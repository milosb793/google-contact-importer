import sys, csv, json
import requests
import argparse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

INSERTED_PERSONS = []
CONVERSION_MAP = {}


def load_conversion_map(json_schema_path):
    global CONVERSION_MAP
    with open(json_schema_path, 'r') as f:
        CONVERSION_MAP = json.load(f)


NEW_FORMAT_ITEM = {'Name': '', 'Given Name': '', 'Additional Name': '', 'Family Name': '', 'Yomi Name': '',
                   'Given Name Yomi': '', 'Additional Name Yomi': '', 'Family Name Yomi': '', 'Name Prefix': '',
                   'Name Suffix': '', 'Initials': '', 'Nickname': '', 'Short Name': '', 'Maiden Name': '',
                   'Birthday': '',
                   'Gender': '', 'Location': '', 'Billing Information': '', 'Directory Server': '', 'Mileage': '',
                   'Occupation': '', 'Hobby': '', 'Sensitivity': '', 'Priority': '', 'Subject': '', 'Notes': ' ',
                   'Language': '', 'Photo': '', 'Group Membership': '* myContacts', 'E-mail 1 - Type': '* ',
                   'E-mail 1 - Value': '', 'Phone 1 - Type': '', 'Phone 1 - Value': '', 'Address 1 - Type': '',
                   'Address 1 - Formatted': '', 'Address 1 - Street': '', 'Address 1 - City': '',
                   'Address 1 - PO Box': '',
                   'Address 1 - Region': '', 'Address 1 - Postal Code': '', 'Address 1 - Country': 'RS',
                   'Address 1 - Extended Address': '', 'Organization 1 - Type': '', 'Organization 1 - Name': '',
                   'Organization 1 - Yomi Name': '', 'Organization 1 - Title': '', 'Organization 1 - Department': '',
                   'Organization 1 - Symbol': '', 'Organization 1 - Location': '',
                   'Organization 1 - Job Description': ''}


def load_inserted_persons():
    global INSERTED_PERSONS

    with open('./data/inserted_numbers', 'a+') as f:
        lines = f.readlines()
        INSERTED_PERSONS = list(set(filter(lambda x: len(x) == 0, map(lambda x: x.strip(), lines))))


def read_input_data(input_path):
    with open(input_path) as f:
        reader = csv.DictReader(f)
        for line in reader:
            yield dict(line)


def store_inserted_numbers():
    with open('./data/inserted_numbers', 'w') as f:
        for line in INSERTED_PERSONS:
            f.write(f"{line}\n")


def convert_to_new_format(item):
    new_item = NEW_FORMAT_ITEM.copy()

    for old_key, new_key in CONVERSION_MAP.items():
        if old_key in item and new_key in new_item:
            new_item[new_key] = item[old_key]

    return new_item


def check_person_inserted(item):
    if f"{item['ИМЕ И ПРЕЗИМЕ']} - {item['БРОЈ ТЕЛЕФОНА']}" in INSERTED_PERSONS:
        return True

    INSERTED_PERSONS.append(f"{item['ИМЕ И ПРЕЗИМЕ']} - {item['БРОЈ ТЕЛЕФОНА']}")

    return False


def authenticate_with_google(token_path, credentials_path):
    SCOPES = ['https://www.googleapis.com/auth/contacts']

    creds = None
    # Load token.json if it exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def upload_csv_to_google_contacts(csv_file_path, token_path, credentials_path):
    creds = authenticate_with_google(token_path, credentials_path)
    service = build('people', 'v1', credentials=creds)

    # Example function to upload contacts from a CSV file
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            contact = {
                'names': [{'givenName': row['Given Name'], 'familyName': row['Family Name']}],
                'phoneNumbers': [{'value': row['Phone 1 - Value']}],
                'addresses': [{'formattedValue': row['Address 1 - Formatted']}],
                'emailAddresses': [{'value': row['E-mail 1 - Value']}],
                'organizations': [{'name': row['Organization 1 - Name'], 'title': row['Organization 1 - Title']}],
                'biographies': [{'value': row['Notes']}]
            }

            service.people().createContact(body=contact).execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert custom CSV to Google Contacts format and upload it.")
    parser.add_argument('--input', required=True, help="Path to the input CSV file.")
    parser.add_argument('--output', required=True, help="Path to the output CSV file.")
    parser.add_argument('--schema', required=True, help="Path to the JSON schema for mapping fields.")
    parser.add_argument('--token', required=False, help="Path to the token.json file.", default="res/token.json")
    parser.add_argument('--credentials', required=False, help="Path to the credentials.json file.", default="res/credentials.json")

    args = parser.parse_args()

    new_format_data = []
    load_inserted_persons()

    load_conversion_map(args.schema)

    with open(args.output, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=NEW_FORMAT_ITEM.keys())
        writer.writeheader()

        for item in read_input_data(args.input):
            if check_person_inserted(item):
                continue

            new_item = convert_to_new_format(item)
            writer.writerow(new_item)

    store_inserted_numbers()

    upload_csv_to_google_contacts(args.output, args.token, args.credentials)
