import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sm_client = boto3.client('sagemaker')

def lambda_handler(event, context):

    #From the transform ARN, retrieve the job name of the transform. This will
    #be used to query the job status.
    print(event)
    if 'TransformJobArn' in event:
        transform_arn = event['TransformJobArn']

        #Retrieve transform job name from transform ARN
        job_name = transform_arn.rsplit(sep='transform-job/', maxsplit=1)[-1]
    else:
        raise KeyError('TransformJobArn key not found in input! Input to Step' +
            ' Function must include JobName!')

    #Query boto3 API to check transform status.
    try:
        response = sm_client.describe_transform_job(TransformJobName=job_name)
        logger.info("Transform job:{} has status:{}!".format(job_name,
            response['TransformJobStatus']))

    except Exception as e:
        response = 'Failed to read transform status!'
        print(e)
        print('Error querying the status of SageMaker transform' +
            'job name: {}! Check the name of the job.'.format(job_name))

    return {
        'statusCode': 200,
        'transformResponse': response['TransformJobStatus']
    }
