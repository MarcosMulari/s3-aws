# AWS S3 Presigned URLs com Signature V4 - Estudos

Este repositório contém exemplos e estudos sobre como implementar upload e download de imagens usando AWS S3 com presigned URLs e AWS Signature Version 4.

## Objetivos do Projeto

- [x] Configurar conexão com AWS S3
- [x] Gerar presigned URLs para upload
- [x] Implementar upload de imagens via presigned URL
- [x] Gerar presigned URLs para download/visualização
- [x] Criar interface para renderizar imagens

## Funcionalidades Implementadas

- **Conexão AWS S3**: Cliente configurado com credenciais e região
- **Presigned URLs**: Geração para upload e download com Signature V4
- **Upload de Imagens**: Interface drag & drop com validação e progresso
- **Galeria de Imagens**: Listagem e visualização via presigned URLs
- **API RESTful**: Endpoints para upload, listagem e visualização

## Stack Tecnológica

- **Backend**: Python + FastAPI + boto3
- **Frontend**: HTML/CSS/JavaScript
- **AWS**: S3 com Presigned URLs e Signature V4

## Como Usar

### Pré-requisitos
- **Python 3.8+** 
- **Conta AWS** com acesso ao S3

### Configuração
1. Clone e acesse o repositório
2. Configure ambiente virtual: `python -m venv venv` e ative
3. Configure credenciais no arquivo `.env` (use `.env.example` como base)
4. Execute: `python run.py`
5. Acesse: http://localhost:3000

## Próximos Passos

- [ ] **Migração de Arquivos entre Buckets**: Implementar endpoint para mover arquivos de um bucket S3 para outro
- [ ] **Validação de Arquivos**: Adicionar verificação de integridade e tipo de arquivo antes da migração
- [ ] **Integração Antivírus**: Implementar verificação de malware usando serviços como AWS GuardDuty ou ClamAV
- [ ] **Pipeline de Segurança**: Criar fluxo automatizado: upload → validação → antivírus → migração para bucket final
- [ ] **Monitoramento**: Adicionar logs e métricas para acompanhar o processo de migração
- [ ] **Interface de Migração**: Criar interface para gerenciar e monitorar transferências entre buckets

## Endpoints da API

- **POST /api/presigned-post**: Gera URL para upload
- **GET /api/files**: Lista arquivos do bucket  
- **GET /api/view-url/{key}**: Gera URL para visualização
- **GET /api/health**: Status da aplicação
- **GET /docs**: Documentação Swagger da API

---

**Estudos AWS S3 • Presigned URLs • Signature V4**
