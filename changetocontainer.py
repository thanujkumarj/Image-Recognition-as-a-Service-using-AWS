import json
import boto3

# Define the AWS region and DynamoDB table name
region_name = 'us-east-1'
table_name = 'students'

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name)

# Open the JSON file and read its contents
with open('student_data.json', 'r') as f:
    data = json.load(f)

# Upload each item in the JSON data to the table
table = dynamodb.Table(table_name)
with table.batch_writer() as batch:
    for item in data:
        batch.put_item(
            Item={
                'id': item['id'],
                'name': item['name'],
                'major': item['major'],
                'year': item['year']
            }
        )
