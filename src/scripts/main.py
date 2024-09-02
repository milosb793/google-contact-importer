from src.output import store_to_output
from src.upload import upload_csv_to_google_contacts
from src.util import setup_arg_parser, set_globals_from_input


def main(*args, **kwargs):
    set_globals_from_input(**kwargs)

    store_to_output(input_path=kwargs['input'], output_path=kwargs['output'])
    upload_csv_to_google_contacts(csv_file_path=kwargs['input'], token_path=kwargs['token'], credentials_path=kwargs['credentials'])
