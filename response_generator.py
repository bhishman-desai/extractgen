import os
import json
import boto3
from urllib.parse import unquote_plus

# Environment variables
OUTPUT_BUCKET_NAME = os.environ["OUTPUT_BUCKET_NAME"]
OUTPUT_S3_PREFIX = os.environ["OUTPUT_S3_PREFIX"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
SNS_ROLE_ARN = os.environ["SNS_ROLE_ARN"]

def lambda_handler(event, context):
    """Main Lambda handler triggered by S3 event."""
    try:
        # Initialize AWS clients
        textract = boto3.client("textract")
        sns = boto3.client("sns")

        # Check if event is not empty
        if event:
            # Extract bucket name and file name from the event
            file_obj = event["Records"][0]
            bucket_name = str(file_obj["s3"]["bucket"]["name"])
            file_name = unquote_plus(str(file_obj["s3"]["object"]["key"]))

            print(f"Bucket: {bucket_name} ::: Key: {file_name}")

            # Start Textract job
            textract_response = textract.start_document_text_detection(
                DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": file_name}},
                OutputConfig={"S3Bucket": OUTPUT_BUCKET_NAME, "S3Prefix": OUTPUT_S3_PREFIX},
            )

            # Check if Textract job was started successfully
            if textract_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                print("Textract job created successfully!")

                # Publish a message to the SNS topic with the Textract response
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=json.dumps(textract_response),
                    Subject='Textract Job Created'
                )

                return {"statusCode": 200, "body": json.dumps("Job created and SNS message sent successfully!")}
            else:
                return {"statusCode": 500, "body": json.dumps("Job creation failed!")}
    except Exception as e:
        # Handle the exception
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return {"statusCode": 500, "body": json.dumps(error_message)}
