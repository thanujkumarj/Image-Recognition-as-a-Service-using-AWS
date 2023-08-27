import boto3
import threading
import hashlib
import time
import json

s3 = boto3.client('s3')

input_bucket = 'input-bucket-23'
output_bucket = 'output-bucket-23'
access_key = 'AKIAYMYGIKNLGX475PGD'
secret_key = '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'
region = 'us-east-1'
processed_files = set()
lambda_client = boto3.client('lambda',aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key, region_name=region)

def process_video(video_key):
    # code to trigger Lambda function to process the video
    payload = {'video_key': video_key}
    response = lambda_client.invoke(
        FunctionName='latest',
        Payload=json.dumps(payload)
    )
    # check the response of the Lambda function
    if response['StatusCode'] != 200:
        print('Failed to trigger Lambda function')


# def process_video(video_key):
#     # code to trigger Lambda function to process the video
#     pass

def hash_file(key):
    obj = s3.get_object(Bucket=input_bucket, Key=key)
    hasher = hashlib.sha256()
    while True:
        chunk = obj['Body'].read(4096)
        if not chunk:
            break
        hasher.update(chunk)
    return hasher.digest()

def monitor_input():
    while True:
        response = s3.list_objects_v2(Bucket=input_bucket)

        if 'Contents' in response:
            for obj in response['Contents']:
                video_key = obj['Key']
                
                file_hash = hash_file(video_key)
                if file_hash not in processed_files:
                    process_video(video_key)
                    print(f'processed video_key is {video_key}')
                    processed_files.add(file_hash)

        # wait for 5 seconds before checking again
        time.sleep(5)

def monitor_output():
    while True:
        response = s3.list_objects_v2(Bucket=output_bucket)

        if 'Contents' in response:
            for obj in response['Contents']:
                academic_info_key = obj['Key']
                academic_info = s3.get_object(Bucket=output_bucket, Key=academic_info_key)['Body'].read().decode('utf-8')

                # print the academic info on the console
                print(academic_info)

                # or save the academic info in a file
                with open('academic_info.txt', 'w') as f:
                    f.write(academic_info)

                # delete the object from the output bucket
                s3.delete_object(Bucket=output_bucket, Key=academic_info_key)

        # wait for 5 seconds before checking again
        time.sleep(5)

# start the monitor_input() and monitor_output() functions in separate threads
input_thread = threading.Thread(target=monitor_input)
output_thread = threading.Thread(target=monitor_output)

input_thread.start()
output_thread.start()

# wait for the threads to finish (this won't happen since they run infinitely)
input_thread.join()
output_thread.join()
