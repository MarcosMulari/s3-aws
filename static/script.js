// JavaScript para interface do AWS S3 Presigned URLs

class S3UploadManager {
    constructor() {
        this.apiBase = '/api';
        this.initializeEventListeners();
        this.logActivity('Sistema iniciado - pronto para upload', 'info');
    }

    initializeEventListeners() {
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        const refreshBtn = document.getElementById('refreshBtn');
        const uploadArea = document.getElementById('uploadArea');

        // Upload de arquivo
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        uploadBtn.addEventListener('click', () => this.handleUpload());
        
        // Refresh da galeria
        refreshBtn.addEventListener('click', () => this.refreshGallery());

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.validateAndPrepareFile(file);
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }

    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            document.getElementById('fileInput').files = files;
            this.validateAndPrepareFile(file);
        }
    }

    validateAndPrepareFile(file) {
        // Validação de tipo
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            this.logActivity(`Tipo de arquivo não suportado: ${file.type}`, 'error');
            return false;
        }

        // Validação de tamanho (10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            this.logActivity(`Arquivo muito grande: ${(file.size / 1024 / 1024).toFixed(2)}MB`, 'error');
            return false;
        }

        // Habilita botão de upload
        document.getElementById('uploadBtn').disabled = false;
        this.logActivity(`Arquivo selecionado: ${file.name} (${(file.size / 1024).toFixed(2)}KB)`, 'info');
        
        return true;
    }

    async handleUpload() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        
        if (!file) {
            this.logActivity('Nenhum arquivo selecionado', 'error');
            return;
        }

        try {
            this.showProgress(0);
            this.logActivity('Solicitando URL pré-assinada...', 'info');

            // 1. Solicita presigned POST URL
            const presignedResponse = await fetch(`${this.apiBase}/presigned-post`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: file.name,
                    content_type: file.type,
                    expiration: 3600
                })
            });

            if (!presignedResponse.ok) {
                throw new Error(`Erro ao obter URL pré-assinada: ${presignedResponse.statusText}`);
            }

            const presignedData = await presignedResponse.json();
            this.logActivity('URL pré-assinada obtida com sucesso', 'success');
            this.showProgress(30);

            // 2. Upload direto para S3
            this.logActivity('Iniciando upload para S3...', 'info');
            const uploadSuccess = await this.uploadToS3(presignedData, file);

            if (uploadSuccess) {
                this.showProgress(100);
                this.logActivity(`Upload concluído: ${file.name}`, 'success');
                
                // Reset form
                fileInput.value = '';
                document.getElementById('uploadBtn').disabled = true;
                
                // Refresh gallery
                setTimeout(() => {
                    this.hideProgress();
                    this.refreshGallery();
                }, 1000);
            } else {
                throw new Error('Falha no upload para S3');
            }

        } catch (error) {
            this.logActivity(`Erro no upload: ${error.message}`, 'error');
            this.hideProgress();
        }
    }

    async uploadToS3(presignedData, file) {
        try {
            const formData = new FormData();
            
            // Adiciona os campos obrigatórios primeiro
            Object.keys(presignedData.fields).forEach(key => {
                formData.append(key, presignedData.fields[key]);
            });
            
            // Adiciona o arquivo por último
            formData.append('file', file);

            const response = await fetch(presignedData.url, {
                method: 'POST',
                body: formData
            });

            this.showProgress(80);
            return response.status === 204; // S3 retorna 204 para upload bem-sucedido

        } catch (error) {
            console.error('Erro no upload direto para S3:', error);
            return false;
        }
    }

    async refreshGallery() {
        this.logActivity('Atualizando galeria...', 'info');
        
        try {
            // Lista arquivos do S3
            const response = await fetch(`${this.apiBase}/files`);
            if (!response.ok) {
                throw new Error(`Erro ao carregar galeria: ${response.statusText}`);
            }
            
            const data = await response.json();
            const files = data.files || [];
            
            // Atualiza contador
            document.getElementById('imageCount').textContent = `${files.length} imagens`;
            
            // Atualiza galeria
            await this.renderGallery(files);
            
            this.logActivity(`Galeria atualizada: ${files.length} imagens encontradas`, 'success');
            
        } catch (error) {
            this.logActivity(`Erro ao atualizar galeria: ${error.message}`, 'error');
            document.getElementById('imageCount').textContent = 'Erro ao carregar';
        }
    }

    async renderGallery(files) {
        const galleryContainer = document.getElementById('gallery');
        galleryContainer.innerHTML = '';
        
        if (files.length === 0) {
            return; // CSS já mostra "Nenhuma imagem encontrada"
        }
        
        for (const file of files) {
            try {
                // Gera URL de visualização
                const viewResponse = await fetch(`${this.apiBase}/view-url/${encodeURIComponent(file.key)}`);
                if (!viewResponse.ok) continue;
                
                const viewData = await viewResponse.json();
                
                // Cria elemento da imagem
                const imageItem = document.createElement('div');
                imageItem.className = 'gallery-item';
                
                const img = document.createElement('img');
                img.src = viewData.view_url;
                img.alt = file.key;
                img.title = `${file.key}\nTamanho: ${this.formatFileSize(file.size)}\nUpload: ${new Date(file.last_modified).toLocaleString()}`;
                
                const info = document.createElement('div');
                info.className = 'image-info';
                info.innerHTML = `
                    <span class="filename">${file.key.split('/').pop()}</span>
                    <span class="filesize">${this.formatFileSize(file.size)}</span>
                `;
                
                imageItem.appendChild(img);
                imageItem.appendChild(info);
                galleryContainer.appendChild(imageItem);
                
            } catch (error) {
                console.error(`Erro ao renderizar ${file.key}:`, error);
            }
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showProgress(percent) {
        const progressContainer = document.getElementById('uploadProgress');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        progressContainer.style.display = 'block';
        progressFill.style.width = `${percent}%`;
        progressText.textContent = `${percent}%`;
    }

    hideProgress() {
        const progressContainer = document.getElementById('uploadProgress');
        progressContainer.style.display = 'none';
    }

    logActivity(message, type = 'info') {
        const logsContainer = document.getElementById('logs');
        const timestamp = new Date().toLocaleTimeString();
        
        const logItem = document.createElement('p');
        logItem.className = `log-item ${type}`;
        logItem.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
        
        logsContainer.appendChild(logItem);
        logsContainer.scrollTop = logsContainer.scrollHeight;

        // Limita logs a 50 itens
        const logs = logsContainer.querySelectorAll('.log-item');
        if (logs.length > 50) {
            logs[0].remove();
        }
    }
}

// Inicializa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new S3UploadManager();
});