import boto3

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name[5:]  # Remove "/tmp/" from file name
    s3_client = boto3.client('s3', region_name = 'us-east-2')
    response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"})

    return response


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents