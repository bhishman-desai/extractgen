# ExtractGen

## Introduction
This project is designed to extract text from multi-page PDF files and store the extracted data as key-value pairs in a CSV file. The primary functionality is to convert unstructured data (text in PDF files) into structured data (CSV files), which can be easily manipulated and analyzed.

## Technologies Used
- **AWS Lambda**: Runs serverless functions for text extraction and data formatting.
- **AWS EC2**: Hosts the frontend application for uploading PDF files and downloading the converted CSV files.
- **AWS S3**: Stores the PDF and CSV files.
- **AWS API Gateway**: Creates a RESTful API for user interaction.
- **AWS SNS (Simple Notification Service)**: Sends notifications when the text extraction process is completed.
- **Amazon Textract**: Extracts text and data from the PDF files.

## Application Flow
1. **User Interaction**: Users interact with the EC2-hosted frontend application to upload PDF files and download the converted CSV files.
2. **File Upload**: Users upload a PDF to an S3 bucket using the /upload API Gateway.
3. **Text Extraction**: A Lambda function is triggered to extract text from the uploaded PDF using Amazon Textract.
4. **Notification**: When text extraction is complete, SNS sends a notification to another Lambda function.
5. **Data Formatting**: The notified Lambda function reads the extracted text response from the S3 bucket and converts it into a structured CSV file.
6. **File Storage**: The CSV file is uploaded back to the S3 bucket by the Lambda function.
7. **File Download**: Users can call the /download API Gateway to trigger a Lambda function that fetches the CSV file, generates a pre-signed URL, and returns the response to the EC2 instance for download.

This project can be particularly useful in scenarios where large amounts of data are locked in PDF files, and there is a need to extract this data for further analysis or processing.

## Getting Started

To get started with this project, you can follow the instructions in the [video](https://www.youtube.com/watch?v=wTmT9deo9dU) to set up the environment and get going. To get an in depth understanding of the project including the Deployment model, Delivery Model, Architecture, Security, Reproducing cost, Monitoring, and further development, please refer this [report](B00945177_BhishmanDesai_FinalReport.pdf).

## Contributing

Contributions to enhance the app's functionality or address any issues are welcome. Feel free to use the provided source code as a reference for creating similar applications for your institution.

## License

This project is licensed under the [MIT License](LICENSE).