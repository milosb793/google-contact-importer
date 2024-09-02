import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_BASE_PATH = f"{ROOT_PATH}/data"
RESOURCES_BASE_PATH = f"{ROOT_PATH}/res"

TOKEN_PATH = f"{RESOURCES_BASE_PATH}/token.json"
CREDENTIALS_PATH = f"{RESOURCES_BASE_PATH}/credentials.json"
DATA_SCHEMA_PATH = f"{DATA_BASE_PATH}/schema.json"

APP_DRY_RUN = False
DATA_SCHEMA = {}


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
