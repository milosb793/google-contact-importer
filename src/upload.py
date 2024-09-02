import csv
import json
from googleapiclient.discovery import build

from src.auth import authenticate_with_google
import src.config as config
from src.conversion import convert_to_new_format


def create_contact_api_format(item: dict):
    """
    TODO: make this function be custom and support all other fields
    TODO: and make it correlate properly with given schema.json
    :type item: dict
    :return: dict
    """
    names = [{'givenName': item['Name']}]
    phone_numbers = [{'value': number} for number in item['Phone 1 - Value']]
    addresses = [{'formattedValue': item['Address 1 - Formatted']}]
    email_addresses = [{'value': item['E-mail 1 - Value']}]
    organizations = [{'name': item['Organization 1 - Name'], 'title': item['Organization 1 - Title']}]
    biographies = [{'value': item['Notes']}]

    return {
        'names': names,
        'phoneNumbers': phone_numbers,
        'addresses': addresses,
        'emailAddresses': email_addresses,
        'organizations': organizations,
        'biographies': biographies
    }


def get_total_records(csv_file_path: str) -> int:
    with open(csv_file_path, 'r') as f:
        return sum(1 for _ in csv.DictReader(f))


def sanitize_data(row):
    return row


def upload_csv_to_google_contacts(csv_file_path: str,
                                  token_path: str = config.TOKEN_PATH,
                                  credentials_path: str = config.CREDENTIALS_PATH):

    creds = authenticate_with_google(token_path, credentials_path)
    service = build('people', 'v1', credentials=creds)
    total = get_total_records(csv_file_path)

    print(f"Starting uploading to Google Contacts (total: {total})")

    # Example function to upload contacts from a CSV file
    with (open(csv_file_path, 'r') as csv_file):
        reader = csv.DictReader(csv_file, quoting=csv.QUOTE_ALL)
        for i, row in enumerate(reader):
            print(f"Uploading ({i + 1} of {total})")

            row = convert_to_new_format(row, conversion_map=config.DATA_SCHEMA)
            row = sanitize_data(row)
            row = create_contact_api_format(row)

            print(f"Creating contact (dry mode: {config.APP_DRY_RUN}):  ", row)

            if not config.APP_DRY_RUN:
                service.people().createContact(body=row).execute()
