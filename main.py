import sys, csv

INSERTED_PERSONS = []
CONVERSION_MAP = {
    'ИМЕ И ПРЕЗИМЕ': 'Name',
    'УЛИЦА': 'Address 1 - Formatted',
    'БРОЈ': 'Address 1 - Formatted',
    'БРОЈ ТЕЛЕФОНА': 'Phone 1 - Value',
    'СЛАВА': 'Subject',
    'ДАТУМ': 'Notes',
    'ВОДИЦА': 'Notes',
    'НАПОМЕНА': 'Notes',
}

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
    return {
        **NEW_FORMAT_ITEM,
        'Name': f"{item['ИМЕ И ПРЕЗИМЕ']}",
        'Address 1 - Formatted': f"{item['УЛИЦА']} {item['БРОЈ']}",
        'Phone 1 - Value': f"{item['БРОЈ ТЕЛЕФОНА']}",
        'Subject': f"{item['СЛАВА']}",
        'Notes': f"""
            Датум: {item['ДАТУМ']}
            Водица: {item['ВОДИЦА']}
            НАПОМЕНА: {item['НАПОМЕНА']}
        """
    }


def check_person_inserted(item):
    if f"{item['ИМЕ И ПРЕЗИМЕ']} - {item['БРОЈ ТЕЛЕФОНА']}" in INSERTED_PERSONS:
        return True

    INSERTED_PERSONS.append(f"{item['ИМЕ И ПРЕЗИМЕ']} - {item['БРОЈ ТЕЛЕФОНА']}")

    return False


if __name__ == '__main__':
    new_format_data = []
    load_inserted_persons()
    _, input_path, output_path, *args = sys.argv

    with open(output_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=NEW_FORMAT_ITEM.keys())
        writer.writeheader()

        for item in read_input_data(input_path):
            if check_person_inserted(item):
                continue

            new_item = convert_to_new_format(item)
            writer.writerow(new_item)

    store_inserted_numbers()
