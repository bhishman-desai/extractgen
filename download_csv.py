import boto3
import os
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = os.environ['OUTPUT_BUCKET_NAME']
    folder_name = 'csv/'

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        if 'Contents' in response:
            files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.csv')]
            if files:
                urls = [s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file}) for file in files]
                return {
                    'isBase64Encoded': False,
                    'statusCode': 200,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps(urls)
                }
            else:
                return {
                    'isBase64Encoded': False,
                    'statusCode': 200,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps('No CSV files found.')
                }
        else:
            return {
                'isBase64Encoded': False,
                'statusCode': 200,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps('Download not ready yet.')
            }
    except Exception as e:
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps('Error: ' + str(e))
        }
