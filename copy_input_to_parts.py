import csv
from mapping import MAPPING
# Path to the source and template files
TEEMA_CSV = 'sample-data/Teema_Sample_Data.csv'
PARTS_TEMPLATE_CSV = 'sample-data/Parts_Template.csv'
# Output file for the mapped data
OUTPUT_CSV = 'sample-data/Parts_Output.csv'


def read_teema_data(teema_csv_path) -> list[dict]:
    """
    Read the Teema_Sample_Data.csv and return a list of dictionaries.
    """
    data = []
    with open(teema_csv_path, mode='r', newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data


def read_parts_template(parts_template_csv_path) -> list[dict]:
    """
    Read the Parts_Template.csv and extract mapping/business logic.
    """
    data = []
    with open(parts_template_csv_path, mode='r',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data


def map_teema_to_parts(teema_data, parts_template, mapping):
    """
    Map Teema data to Parts template columns according to mapping logic.
    Returns a list of dictionaries in the Parts_Template format.
    """
    mapped_data = []
    if not parts_template:
        return mapped_data
    parts_columns = list(parts_template[0].keys())
    for teema_row in teema_data:
        mapped_row = {}
        for col in parts_columns:
            if col in mapping:
                teema_col = mapping[col]
                mapped_row[col] = teema_row.get(teema_col, '')
            else:
                mapped_row[col] = ''
        mapped_data.append(mapped_row)
    return mapped_data


def write_output(mapped_data, output_csv_path):
    """
    Write the mapped data to a new CSV file with headers from mapped_data.
    """
    if not mapped_data:
        return
    with open(output_csv_path, mode='w', newline='',
              encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=mapped_data[0].keys())
        writer.writeheader()
        for row in mapped_data:
            writer.writerow(row)


def main():
    # Read source data
    teema_data = read_teema_data(TEEMA_CSV)
    # Read template
    parts_template = read_parts_template(PARTS_TEMPLATE_CSV)
    # Get the mapping rules
    mapping = MAPPING
    # Map data according to mapping rules
    mapped_data = map_teema_to_parts(teema_data, parts_template, mapping)
    # Write output
    write_output(mapped_data, OUTPUT_CSV)


if __name__ == '__main__':
    main()
