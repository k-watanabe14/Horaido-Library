from app import app
import boto3

def upload_file(body, key, content_type):
    """
    Function to upload a file to an S3 bucket
    """
    s3_client = boto3.client('s3', region_name = 'us-east-2')
    bucket = app.config['S3_BUCKET']
    response = s3_client.put_object(Body=body, Bucket=bucket, Key=key, ContentType=content_type, ACL='public-read')

    return response
