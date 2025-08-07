import csv
import boto3
import io
from mapping import MAPPING
from typing import List, Dict
import logging
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def read_s3_data(bucket, key) -> List[Dict]:
    """
    Read the .csv file added to the s3 bucket and return a list of dictionaries.
    """
    response = s3.get_object(Bucket=bucket, Key=key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    return list(csv.DictReader(lines))


def map_input_to_template(input_data, mapping) -> List[Dict]:
    """Map input data to expected format based on provided mapping."""
    mapped_data = []
    for input_row in input_data:
        mapped_row = {}
        for output_col, input_col in mapping.items():
            mapped_row[output_col] = input_row.get(input_col, '') if input_col in input_row else input_col
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
    fieldnames = list(mapped_data[0].keys())
    type_row = ['text' for f in fieldnames]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    buffer.write(','.join(fieldnames) + '\n')  # header
    buffer.write(','.join(type_row) + '\n')    # type row

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

        logger.info(f"✅ Processed and saved: s3://{bucket}/{output_key}")
        return {
            'statusCode': 200,
            'body': f'Successfully processed {input_key}'
        }

    except Exception as e:
        logger.info(f"❌ Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {str(e)}"
        }
