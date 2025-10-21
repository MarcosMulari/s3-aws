# AWS S3 Presigned URLs com Signature V4 - Estudos

Este repositório contém exemplos e estudos sobre como implementar upload e download de imagens usando AWS S3 com presigned URLs e AWS Signature Version 4.

## 🎯 Objetivos do Projeto

- [x] Configurar conexão com AWS S3
- [ ] Gerar presigned URLs para upload
- [ ] Implementar upload de imagens via presigned URL
- [ ] Gerar presigned URLs para download/visualização
- [ ] Criar interface para renderizar imagens

## 📋 Funcionalidades Planejadas

### 1. Conexão com AWS S3
- Configuração de credenciais AWS
- Inicialização do cliente S3
- Configuração de bucket e região

### 2. Geração de Presigned URLs
- **Upload URLs**: Para permitir upload direto de arquivos
- **Download URLs**: Para visualização segura de imagens
- Implementação de AWS Signature V4
- Configuração de tempo de expiração

### 3. Upload de Imagens
- Interface para seleção de arquivos
- Upload via presigned URL
- Validação de tipos de arquivo
- Feedback de progresso

### 4. Visualização de Imagens
- Listagem de imagens do bucket
- Renderização via presigned URLs
- Interface responsiva

## 🛠️ Stack Tecnológica

- **Backend**: Python 3.8+
- **AWS SDK**: boto3
- **Framework Web**: Flask/FastAPI
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Ferramentas**: uvicorn para servidor ASGI

## 📁 Estrutura do Projeto

```
s3-aws/
├── src/
│   ├── config/
│   │   └── aws_config.py     # Configurações AWS
│   ├── services/
│   │   └── s3_service.py     # Serviços do S3
│   ├── routes/
│   │   └── upload_routes.py  # Rotas para upload
│   ├── models/
│   │   └── response_models.py # Modelos de resposta
│   └── main.py               # Aplicação principal
├── static/
│   ├── index.html            # Interface principal
│   ├── styles.css            # Estilos
│   └── script.js             # JavaScript frontend
├── examples/
│   ├── basic_upload.py       # Exemplo básico de upload
│   ├── presigned_url.py      # Geração de URLs
│   └── signature_v4.py       # Implementação manual da assinatura
├── tests/
│   ├── test_s3_service.py    # Testes do serviço S3
│   └── test_routes.py        # Testes das rotas
├── docs/
│   └── aws-signature-v4.md   # Documentação sobre Signature V4
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore
├── requirements.txt          # Dependências Python
└── README.md
```

## 🚀 Como Usar

### Pré-requisitos

1. **Conta AWS** com acesso ao S3
2. **Python 3.8+** 
3. **pip** (gerenciador de pacotes Python)
4. **Credenciais AWS** configuradas

### Configuração Inicial

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd s3-aws
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
copy .env.example .env
# Edite o arquivo .env com suas credenciais AWS
```

5. Execute o projeto:
```bash
python src/main.py
# ou
uvicorn src.main:app --reload
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=seu-bucket-name
PORT=3000
```

## 📚 Conceitos Estudados

### AWS Signature Version 4
- Processo de assinatura de requisições AWS
- Geração de chaves derivadas
- Construção do string-to-sign
- Headers de autorização

### Presigned URLs
- Mecanismo de autorização temporária
- Segurança e controle de acesso
- Configuração de expiração
- Políticas de upload

### S3 Security Best Practices
- Configuração de CORS
- Políticas de bucket
- Encryption em trânsito e em repouso
- Controle de acesso granular

## 🔧 Exemplos de Uso

### Gerar Presigned URL para Upload
```python
from src.services.s3_service import S3Service

s3_service = S3Service()
upload_url = s3_service.generate_presigned_upload_url('image.jpg', 'image/jpeg')
print(f'Upload URL: {upload_url}')
```

### Upload de Arquivo via API
```python
# Via requisição POST
import requests

response = requests.post('/api/generate-upload-url', json={
    'filename': 'image.jpg',
    'content_type': 'image/jpeg'
})
upload_url = response.json()['upload_url']
```

### Gerar Presigned URL para Visualização
```python
view_url = s3_service.generate_presigned_view_url('image.jpg')
print(f'View URL: {view_url}')
```

## 📖 Recursos de Aprendizado

- [AWS S3 Developer Guide](https://docs.aws.amazon.com/s3/)
- [AWS Signature Version 4 Documentation](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
- [Presigned URLs Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)

## 🤝 Contribuindo

Este é um projeto de estudos, mas sugestões e melhorias são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📝 Notas de Desenvolvimento

### Próximos Passos
- [ ] Configurar boto3 e credenciais AWS
- [ ] Criar serviço S3 com presigned URLs
- [ ] Implementar API REST com FastAPI
- [ ] Desenvolver interface web para upload
- [ ] Implementar galeria de imagens
- [ ] Adicionar testes com pytest
- [ ] Documentar API com Swagger

### Desafios Técnicos
- Compreender o processo completo de AWS Signature V4
- Gerenciar CORS adequadamente
- Implementar feedback de upload em tempo real
- Otimizar performance para múltiplos uploads

---

**Autor**: Estudos em AWS S3 e Presigned URLs  
**Data de Criação**: Outubro 2024  
**Última Atualização**: Outubro 2024