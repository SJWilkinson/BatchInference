import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):

    #Read object from S3 bucket
    cid = read_s3(event["CustomerID"])
    cid = cid.read().decode()

    cid_list = cid.split(sep='\n')
    if cid_list[-1] == '':
        cid_list.pop()

    #Retrieve churner list
    churner_list = json.loads(event['Churners'])

    churner_cids = []
    for churner in churner_list:
        churner_cids.append(cid_list[churner])

    print(json.JSONEncoder().encode(churner_cids))
    return {
        'statusCode': 200,
        'churner_cids': json.dumps(churner_cids)
    }

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
