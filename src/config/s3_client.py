import boto3
from botocore.config import Config
import os

class S3Client:
    """Configurações para o cliente S3 da AWS"""
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "not-configured")
        self.region = os.getenv("AWS_REGION", "not-configured")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "not-configured")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "not-configured")
        self.signature_version = 's3v4'
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL")

    def get_client(self):
        """Cria e retorna um cliente S3 configurado"""
        s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
            config=Config(
                signature_version=self.signature_version,
                retries={'max_attempts': 3}
            )
        )
        return s3_client
    
        



