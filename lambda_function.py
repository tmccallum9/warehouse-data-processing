import csv
import boto3
import io
from mapping import MAPPING

s3 = boto3.client('s3')

# Template path in S3
TEMPLATE_KEY = 'templates/Parts_Template.csv'


def read_s3_data(bucket, key) -> list[dict]:
    """
    Read the .csv file added to the s3 bucket and return a list of dictionaries.
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    return list(csv.DictReader(lines))


def read_template_headers(bucket, key):
    """
    Read the Parts_Template.csv and extract the headers for the output .csv.
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    header = lines[0]
    type_row = lines[1]
    reader = csv.DictReader(lines[2:])
    return list(reader), header, type_row


def map_input_to_template(input_data, parts_template, mapping):
    """
    Map input data to parts template columns according to mapping logic.
    Returns a list of dictionaries in the Parts_Template format.
    """
    mapped_data = []
    if not parts_template:
        return mapped_data
    parts_columns = list(parts_template[0].keys())
    for input_row in input_data:
        mapped_row = {}
        for col in parts_columns:
            if col in mapping:
                input_col = mapping[col]
                mapped_row[col] = input_row.get(input_col, '') if input_col in input_row else input_col
            else:
                mapped_row[col] = ''
        mapped_data.append(mapped_row)
    return mapped_data


def write_output_to_s3(mapped_data, bucket, key, header, type_row):
    """
    Write the mapped data to a new CSV file, using the first two rows from
    Parts_Template.csv as the header and type rows.
    """
    if not mapped_data:
        return
    buffer = io.StringIO()
    buffer.write(header + '\n')
    buffer.write(type_row + '\n')
    writer = csv.DictWriter(buffer, fieldnames=mapped_data[0].keys())
    for row in mapped_data:
        writer.writerow(row)
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())


def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        input_key = record['s3']['object']['key']  # input/clientA/SomeFile.csv

        # Extract username from S3 key
        parts = input_key.split('/')
        if len(parts) < 3 or parts[0] != 'input':
            raise ValueError("Unexpected key format, expected input/{username}/{file.csv}")
        username = parts[1]

        # Read input file and template
        input_data = read_s3_data(bucket, input_key)
        template_data, header, type_row = read_template_headers(bucket, TEMPLATE_KEY)

        # Apply mapping
        mapped_data = map_input_to_template(input_data, template_data, MAPPING)

        # Write output to S3
        output_key = f'output/{username}/Parts_Output.csv'
        write_output_to_s3(mapped_data, bucket, output_key, header, type_row)

        print(f"✅ Processed and saved: s3://{bucket}/{output_key}")
        return {
            'statusCode': 200,
            'body': f'Successfully processed {input_key}'
        }

    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {str(e)}"
        }
