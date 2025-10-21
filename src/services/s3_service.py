import sys
from pathlib import Path
import logging
from botocore.exceptions import ClientError
import requests

# Adiciona o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent.parent))


class S3Service:
    """Serviço para operações com S3"""
    def __init__(self, client, bucket_name):
        self.client = client
        self.bucket_name = bucket_name

    def create_presigned_post(self,
         object_name, fields=None, conditions=None, expiration=3600):
        """Generate a presigned URL S3 POST request to upload a file

        :param object_name: string - Nome do objeto no S3
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """
        bucket_name = self.bucket_name

        # Condições padrão para o upload
        if conditions is None:
            conditions = []
        
        # Adiciona condições essenciais
        conditions.extend([
            ["content-length-range", 1, 10485760],  # 1 byte a 10MB
        ])

        # Campos padrão
        if fields is None:
            fields = {}

        try:
            response = self.client.generate_presigned_post(
                Bucket=bucket_name,
                Key=object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
            
            # Log para debug
            logging.info(f"Presigned POST gerado para: {object_name}")
            return response
            
        except ClientError as e:
            logging.error(f"Erro ao gerar presigned POST: {e}")
            return None
    def post_file(self, presigned_post_data, file_path):
        """Upload a file to S3 using a presigned POST URL

        :param presigned_post_data: Dictionary returned by create_presigned_post
        :param file_path: Path to the file to upload
        :return: True if file was uploaded, else False
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                presigned_post_data['url'], 
                data=presigned_post_data['fields'], 
                files=files
            )
        return response.status_code == 204