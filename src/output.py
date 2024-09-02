import csv

import src.config as config
from src.conversion import convert_to_new_format
from src.upload import sanitize_data
from src.util import read_input_data


def store_to_output(input_path: str, output_path: str):
    print("Storing formatted data to output...")

    with open(output_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=config.NEW_FORMAT_ITEM.keys(), quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for item in read_input_data(input_path):
            new_item = convert_to_new_format(item, conversion_map=config.DATA_SCHEMA)
            new_item = sanitize_data(new_item)
            writer.writerow(new_item)

    print("Storing done!")
