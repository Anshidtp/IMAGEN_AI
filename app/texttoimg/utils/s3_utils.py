import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from app.config import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,S3_BUCKET_NAME


def upload_to_s3(file_path: str, key: str) -> str:
        
            try:
                s3_client = boto3.resource('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)
                bucket = s3_client.Bucket(S3_BUCKET_NAME)
                bucket.upload_file(file_path,key)
              
                s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
                return s3_url
            except (NoCredentialsError, ClientError) as e:
                raise Exception(f"Failed to upload to S3: {str(e)}")

def delete_from_s3(key: str):
        try:
            s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=key)
        except ClientError as e:
            raise Exception(f"Failed to delete from S3: {str(e)}")
