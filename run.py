#!/usr/bin/env python3
"""
Script de execução para o servidor AWS S3 Presigned URLs
"""

import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adiciona o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Carrega variáveis de ambiente
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Iniciando servidor AWS S3 Presigned URLs")
    print(f"📍 Endereço: http://{host}:{port}")
    print(f"📚 Documentação: http://{host}:{port}/docs")
    print(f"🔧 Região AWS: {os.getenv('AWS_REGION', 'não configurada')}")
    print(f"🗂️  Bucket S3: {os.getenv('S3_BUCKET_NAME', 'não configurado')}")
    print("-" * 50)
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["src", "static"],
        log_level="info"
    )