.PHONY: build up down logs clean restart

# Build and start the application
api-up:
	docker-compose up --build -d

# Build the application
api-build:
	docker-compose build

# Stop and remove containers
api-down:
	docker-compose down

# View logs
api-logs:
	docker-compose logs -f api

# Remove all containers and images
api-clean:
	docker-compose down --rmi all --volumes --remove-orphans

# Restart the application
api-restart:
	docker-compose restart api

# Run locust
run-locust:
	locust -f src/locustfile.py
