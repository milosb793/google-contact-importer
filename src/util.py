import csv

import src.config as config
from src.conversion import load_conversion_map


def read_input_data(input_path):
    with open(input_path) as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_ALL)
        for line in reader:
            yield dict(line)


def setup_arg_parser(parser):
    parser.description = "Convert custom CSV to Google Contacts format and upload it."

    parser.add_argument('--input',
                        required=True,
                        help="Path to the input CSV file.")

    parser.add_argument('--output',
                        required=True,
                        help="Path to the output CSV file.")

    parser.add_argument('--dry',
                        required=False,
                        default=False,
                        action='store_true',
                        help="Run script in dry mode, without uploading contacts to Google")

    parser.add_argument('--schema',
                        required=False,
                        help="Path to the JSON schema for mapping fields.",
                        default=config.DATA_SCHEMA_PATH)

    parser.add_argument('--token',
                        required=False,
                        help="Path to the token.json file.",
                        default=config.TOKEN_PATH)

    parser.add_argument('--credentials',
                        required=False,
                        help="Path to the credentials.json file.",
                        default=config.CREDENTIALS_PATH)

    return parser


def set_globals_from_input(**kwargs):
    config.TOKEN_PATH = kwargs['token']
    config.CREDENTIALS_PATH = kwargs['credentials']
    config.APP_DRY_RUN = kwargs['dry']

    load_conversion_map(kwargs['schema'])

