from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import uuid
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.s3_service import S3Service
from src.config.s3_client import S3Client

router = APIRouter(prefix="/api", tags=["Upload"])

# Inicializa o cliente S3 e serviço
bucket_name = S3Client().bucket_name

s3_client = S3Client().get_client()
s3_service = S3Service(s3_client, bucket_name)

# Modelos de request/response
class PresignedPostRequest(BaseModel):
    filename: str
    content_type: str
    expiration: Optional[int] = 3600

class PresignedPostResponse(BaseModel):
    url: str
    fields: dict
    object_name: str

class UploadFileRequest(BaseModel):
    presigned_data: dict
    file_path: str

@router.post("/presigned-post", response_model=PresignedPostResponse)
async def create_presigned_post(request: PresignedPostRequest):
    """
    Cria uma URL pré-assinada para upload direto ao S3 via POST
    """
    try:
        # Gera um nome único para o arquivo
        file_extension = os.path.splitext(request.filename)[1]
        object_name = f"uploads/{uuid.uuid4()}{file_extension}"
        
        # Condições para o upload
        conditions = [
            ["content-length-range", 1, 10485760],  # 1 byte to 10MB
            ["starts-with", "$Content-Type", request.content_type.split("/")[0]]
        ]
        
        # Campos obrigatórios
        fields = {
            "Content-Type": request.content_type
        }
        
        # Gera o presigned POST
        presigned_data = s3_service.create_presigned_post(
            object_name=object_name,
            fields=fields,
            conditions=conditions,
            expiration=request.expiration
        )
        
        if not presigned_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar URL pré-assinada"
            )
        
        return PresignedPostResponse(
            url=presigned_data["url"],
            fields=presigned_data["fields"],
            object_name=object_name
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.post("/upload-file")
async def upload_file_to_s3(
    file: UploadFile = File(...),
    presigned_url: str = Form(...),
    presigned_fields: str = Form(...)
):
    """
    Upload de arquivo usando presigned POST (para teste local)
    """
    try:
        import json
        import tempfile
        
        # Parse dos campos do presigned POST
        fields = json.loads(presigned_fields)
        
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Prepara dados para o upload
            presigned_data = {
                "url": presigned_url,
                "fields": fields
            }
            
            # Faz o upload
            success = s3_service.post_file(presigned_data, temp_file_path)
            
            if success:
                return {
                    "message": "Upload realizado com sucesso",
                    "filename": file.filename,
                    "size": len(content)
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Falha no upload do arquivo"
                )
                
        finally:
            # Remove arquivo temporário
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no upload: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Verifica se o serviço está funcionando
    """
    try:
        # Testa a conexão com S3
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise Exception("Bucket não configurado")
            
        return {
            "status": "healthy",
            "service": "s3-upload",
            "bucket": bucket_name,
            "region": os.getenv("AWS_REGION", "não configurado")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Serviço indisponível: {str(e)}"
        )
