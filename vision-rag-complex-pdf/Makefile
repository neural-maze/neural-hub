.PHONY: setup-vision-rag pre-setup pdf2png png2qdrant setup-pod ssh ollama lint

setup-vision-rag:
	@bash infrastructure/bash_scripts/setup.sh

pre-setup:
	@bash infrastructure/bash_scripts/pre_setup.sh

pdf2png:
	@echo "Processing .pdf files to .png"
	@python document_processor/pdf_to_png.py

png2qdrant:
	@echo "Transforming .png files into tensors and indexing in Qdrant collection."
	@python document_processor/png_to_qdrant.py

setup-pod:
	@echo "🔑 Verificando claves SSH..."
	@bash infrastructure/bash_scripts/ssh_keys.sh
	@echo "🚀 Creando pod..."
	@python infrastructure/python_scripts/create_runpod.py
	@echo "⏳ Esperando que el pod inicie..."
	@sleep 30
	@echo "⚙️  Configurando SSH..."
	@python infrastructure/python_scripts/config_ssh.py
	@echo "📦 Instalando y configurando runpodctl..."
	@bash infrastructure/bash_scripts/install_runpodctl.sh
	@echo "🖥️ Abriendo VSCode conectado al pod remoto..."
	@positron --remote ssh-remote+runpod-pytorch
	@echo "Send code"
	@bash infrastructure/bash_scripts/send_code.sh

ssh:
	@ssh runpod-pytorch

ollama:
	@bash infrastructure/bash_scripts/ollama.sh











