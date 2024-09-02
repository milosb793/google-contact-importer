import json
import src.config as config


def load_conversion_map(json_schema_path):
    with open(json_schema_path, 'r') as f:
        config.DATA_SCHEMA = json.load(f)


def handle_combine_fields(item, new_item: dict, target_field, schema_info: dict):
    if 'combine' in schema_info:
        combine_info = schema_info['combine']
        fields_to_combine = combine_info['fields']
        include_key = combine_info.get('include_key', False)

        # Combine fields based on the schema and the include_key option
        combined_value = ' '.join(item.get(field, '') for field in fields_to_combine)
        if include_key:
            combined_value = ',\n '.join([f"{field}: {item.get(field)}".strip() for field in fields_to_combine])
        new_item[target_field] = combined_value.strip()
    else:
        # Directly map the field
        csv_field = schema_info['csv_field']
        new_item[target_field] = item.get(csv_field, '')

    return new_item


def handle_suffix_fields(item, new_item: dict, target_field, schema_info: dict):
    if 'suffix' in schema_info:
        new_item[target_field] = f"{new_item[target_field]}{schema_info['suffix']}"

    return new_item


def handle_phone_numbers(new_item: dict):
    # split phone number
    if ':' in new_item['Phone 1 - Value']:
        new_item['Phone 1 - Value'] = new_item['Phone 1 - Value'].split(':')
    elif ';' in new_item['Phone 1 - Value']:
        new_item['Phone 1 - Value'] = new_item['Phone 1 - Value'].split(';')
    elif ',' in new_item['Phone 1 - Value']:
        new_item['Phone 1 - Value'] = new_item['Phone 1 - Value'].split(',')
    else:
        new_item['Phone 1 - Value'] = [new_item['Phone 1 - Value']]

    return new_item


def convert_to_new_format(item, conversion_map):
    new_item = {**config.NEW_FORMAT_ITEM}

    for target_field, schema_info in conversion_map.items():
        new_item = handle_combine_fields(item, new_item, target_field, schema_info)
        new_item = handle_suffix_fields(item, new_item, target_field, schema_info)

    new_item = handle_phone_numbers(new_item)

    return new_item
