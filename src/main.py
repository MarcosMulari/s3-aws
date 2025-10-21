"""
AWS S3 Presigned URLs - Aplicação Principal
Estudos sobre upload e download de imagens usando presigned URLs
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="AWS S3 Presigned URLs",
    description="API para estudos de upload/download com presigned URLs",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "message": "AWS S3 Presigned URLs API",
        "version": "1.0.0",
        "description": "API para estudos de presigned URLs com AWS S3",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
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

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["src"]
    )