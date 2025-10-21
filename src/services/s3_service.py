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

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """
        bucket_name=self.bucket_name

        try:
            response = self.client.generate_presigned_post(
                bucket_name,
                object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None
        
        return response
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

    def get_all(self, prefix="", max_keys=1000):
        """Lista todos os objetos do bucket S3
        
        :param prefix: Prefixo para filtrar objetos (ex: "uploads/")
        :param max_keys: Número máximo de objetos a retornar
        :return: Lista de objetos ou None se erro
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            # Se não há objetos no bucket
            if 'Contents' not in response:
                return []
            
            # Formatar lista de objetos
            objects = []
            for obj in response['Contents']:
                objects.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'].strip('"')
                })
            
            logging.info(f"Listados {len(objects)} objetos do bucket {self.bucket_name}")
            return objects
            
        except ClientError as e:
            logging.error(f"Erro ao listar objetos: {e}")
            return None

    def generate_presigned_get_url(self, object_key, expiration=3600):
        """Gera uma URL pré-assinada para visualizar/baixar um objeto
        
        :param object_key: Chave do objeto no S3
        :param expiration: Tempo de expiração em segundos
        :return: URL pré-assinada ou None se erro
        """
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            
            logging.info(f"URL pré-assinada gerada para: {object_key}")
            return response
            
        except ClientError as e:
            logging.error(f"Erro ao gerar URL pré-assinada: {e}")
            return None