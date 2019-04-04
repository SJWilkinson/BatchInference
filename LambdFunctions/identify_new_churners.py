import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
THRESHOLD = float(os.environ['THRESHOLD'])

def lambda_handler(event, context):
    #Try to retrieve the file put in S3
    try:
        obj = read_s3(event)
        obj = obj.read().decode()

    except Exception as e:
        print(e)
        print('Error reading the files from S3.')
        raise e

    #Split the string in to a list with one result per customer
    obj = obj.split('\n')

    #Remove the last item as it contains only whitespace
    if obj[-1] == '':
        obj.pop(-1)

    #Create a list that will track the new churners
    churners = []
    for index, result in enumerate(obj):
        if float(result) > THRESHOLD:
            churners.append(index)

    return {
        'statusCode': 200,
        'body': json.dumps('{} new churners identified!'.format(len(churners))),
        'churners': json.dumps(churners)
    }

#function to read an object from s3
def read_s3(event):
    try:
        bucket_name = event["Bucket"]
        key = event["Key"]
        logger.info('Retrieving Bucket: {} Key: {}'.format(bucket_name, key))
        obj = s3.get_object(Bucket=bucket_name, Key=key)['Body']

    except Exception as e:
        print(e)
        print('Error reading the file from bucket!')
        raise e

    return obj
