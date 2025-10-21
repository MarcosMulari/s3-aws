from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.services.s3_service import S3Service, get_s3_service

router = APIRouter()

@router.post("/upload-url")
async def create_upload_url(request: Request, s3_service: S3Service = Depends(get_s3_service)):
    """Cria uma URL pré-assinada para upload de arquivos"""
    try:
        upload_url = await s3_service.create_presigned_url("put_object", "image/jpeg")
        return {"upload_url": upload_url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
