from app import app
import boto3
from flask import flash
import io
import datetime


def display_errors(items):
    for field, errors in items():
        for error in errors:
            flash(error, 'warning')


def get_new_image_url(image):
    # Save book image into S3 and set image url
    image_name = datetime.datetime.now().isoformat() + ".jpg"
    body = io.BufferedReader(image).read()
    key = f'books/{image_name}'
    upload_file(body, key, 'image/jpeg')
    image_url = 'https://' + \
        app.config['S3_BUCKET'] + \
        '.s3.us-east-2.amazonaws.com/books/' + image_name

    return image_url


def upload_file(body, key, content_type):
    # Function to upload a file to an S3 bucket
    s3_client = boto3.client('s3', region_name='us-east-2')
    bucket = app.config['S3_BUCKET']
    response = s3_client.put_object(
        Body=body, Bucket=bucket, Key=key, ContentType=content_type,
        ACL='public-read')

    return response
