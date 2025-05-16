# ZenML project configuration and pipeline execution
.PHONY: configure-zenml run-cloud run-local clean start-local-qdrant stop-local-qdrant

# Configure ZenML project and stack
configure-zenml:
	@echo "Configuring ZenML project..."
	cd src && zenml init && zenml stack set default
	@echo "Deleting existing ZenML secrets..."
	PYTHONPATH=src python src/vector_twin/scripts/delete_zenml_secrets.py
	@echo "Creating new ZenML secrets..."
	PYTHONPATH=src python src/vector_twin/scripts/create_zenml_secrets.py	

# Run local app
start-local-app: configure-zenml
	@echo "Starting local Qdrant instance..."
	docker compose -f docker-compose.yml up -d
	@echo "Running embedding pipeline with local Qdrant..."
	PYTHONPATH=src python src/embedding_pipeline/run.py

# Stop local app
stop-local-app:
	@echo "Stopping local Qdrant instance..."
	docker compose -f docker-compose.yml down
 
 # Run prod app
insert-embeddings-qdrant-cloud: configure-zenml
	@echo "Running embedding pipeline with Qdrant Cloud..."
	PYTHONPATH=src python src/embedding_pipeline/run.py --use-qdrant-cloud
