"""
AWS S3 Presigned URLs - Aplicação Principal
Estudos sobre upload e download de imagens usando presigned URLs
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Importa as rotas
from src.routes.upload_routes import router as upload_router

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="AWS S3 Presigned URLs",
    description="API para estudos de upload/download com presigned URLs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(upload_router)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Endpoint raiz - redireciona para a interface"""
    return FileResponse("static/index.html")

@app.get("/info")
async def api_info():
    """Endpoint com informações da API"""
    return {
        "message": "AWS S3 Presigned URLs API",
        "version": "1.0.0",
        "description": "API para estudos de presigned URLs com AWS S3",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "api_health": "/api/health",
            "presigned_post": "/api/presigned-post",
            "upload_file": "/api/upload-file",
            "list_files": "/api/files",
            "view_url": "/api/view-url/{object_key}"
        },
        "configuration": {
            "aws_region": os.getenv("AWS_REGION", "not-configured"),
            "bucket": os.getenv("S3_BUCKET_NAME", "not-configured"),
            "port": os.getenv("PORT", "8000")
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "s3-presigned-urls",
        "aws_region": os.getenv("AWS_REGION", "not-configured"),
        "bucket": os.getenv("S3_BUCKET_NAME", "not-configured")
    }