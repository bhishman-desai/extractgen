import os
import json
import boto3
import pandas as pd
import time

# Environment variables
BUCKET_NAME = os.environ["BUCKET_NAME"]
PREFIX = os.environ["PREFIX"]

def lambda_handler(event, context):
    """Main Lambda handler triggered by SNS event."""
    try:
        # Extract JobId from the SNS message
        job_id = json.loads(event["Records"][0]["Sns"]["Message"])["JobId"]

        # Process the Textract response
        page_lines = process_textract_response(job_id)

        # Prepare the CSV file
        csv_key_name = f"{job_id}.csv"
        df = pd.DataFrame(page_lines.items(), columns=["PageNo", "Text"])
        csv_file_path = f"/tmp/{csv_key_name}"
        df.to_csv(csv_file_path, index=False)

        # Upload the CSV file to S3
        upload_to_s3(csv_file_path, BUCKET_NAME, f"{PREFIX}/{csv_key_name}")

        print(df)

        return {"statusCode": 200, "body": json.dumps("File uploaded successfully!")}
    except Exception as e:
        # Handle the exception
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return {"statusCode": 500, "body": json.dumps(error_message)}

def upload_to_s3(file_path, bucket, key):
    """Upload a file to an S3 bucket."""
    s3 = boto3.client("s3")
    s3.upload_file(Filename=file_path, Bucket=bucket, Key=key)

def process_textract_response(job_id):
    """Process the Textract response for a given JobId."""
    try:
        textract = boto3.client("textract")

        # Initialize variables
        pages = []
        page_lines = {}

        # Get the initial response
        response = textract.get_document_text_detection(JobId=job_id)

        # Wait for the Textract job to complete
        while response["JobStatus"] == "IN_PROGRESS":
            print("Waiting for Textract job to complete...")
            time.sleep(5)  # Wait for 5 seconds
            response = textract.get_document_text_detection(JobId=job_id)
        
        # Check the status of the Textract job
        if response["JobStatus"] != "SUCCEEDED":
            raise Exception(f"Textract job {job_id} failed with status {response['JobStatus']}")

        pages.append(response)

        # Get the remaining responses (if any)
        while "NextToken" in response:
            response = textract.get_document_text_detection(JobId=job_id, NextToken=response["NextToken"])
            pages.append(response)

        # Process the responses
        for page in pages:
            if "Blocks" in page:  # Check if 'Blocks' key exists
                for item in page["Blocks"]:
                    if item["BlockType"] == "LINE":
                        if item["Page"] not in page_lines:
                            page_lines[item["Page"]] = []
                        page_lines[item["Page"]].append(item["Text"])

        return page_lines
    except Exception as e:
        error_message = f"An error occurred during processing response: {str(e)}"
        print(error_message)
        raise e  # Re-raise the exception for Lambda to handle it

