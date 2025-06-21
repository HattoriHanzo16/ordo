.PHONY: help build up down logs clean restart shell

help: ## Show this help message
	@echo "Ordo App - Docker Commands"
	@echo "=========================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build all containers
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs from all services
	docker-compose logs -f

frontend-logs: ## View frontend logs only
	docker-compose logs -f frontend

backend-logs: ## View backend logs only
	docker-compose logs -f backend

restart: ## Restart all services
	docker-compose restart

frontend-shell: ## Get shell access to the frontend container
	docker-compose exec frontend sh

backend-shell: ## Get shell access to the backend container
	docker-compose exec backend bash

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all

dev: ## Start development environment
	@make build
	@make up
	@echo "Starting development environment..."
	@echo "Frontend will be available at: http://localhost:3000"
	@echo "Backend will be available at: http://localhost:8000"
	@make logs

setup: ## Initial setup - copy env file and start
	@if [ ! -f server/.env ]; then \
		cp server/env.example server/.env; \
		echo "Created server/.env from env.example"; \
		echo "Please edit server/.env with your configuration"; \
	fi
	@make dev 