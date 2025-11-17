# Variables
IMAGE_NAME := test-demo
IMAGE_TAG := latest
PORT := 8000

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

# Docker image ID file to track builds
DOCKER_ID_FILE := .docker_image_id

# Phony targets
.PHONY: all build run train check-wheel clean test test-docker interactive help

# Default target
all: help

# Build Docker image if necessary, and save the image ID to a .docker_image_id file
$(DOCKER_ID_FILE): Dockerfile $(wildcard src/**/*) $(wildcard requirements*.txt)
	@echo "$(YELLOW)Building $(IMAGE_NAME):$(IMAGE_TAG)$(NC)"
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@docker inspect -f '{{.Id}}' $(IMAGE_NAME):$(IMAGE_TAG) > $(DOCKER_ID_FILE)
	@echo "$(GREEN)Build complete!$(NC)"

build: $(DOCKER_ID_FILE)

# Run Docker container
run: $(DOCKER_ID_FILE)
	@echo "$(YELLOW)Starting container $(IMAGE_NAME):$(IMAGE_TAG)...$(NC)"
	@docker stop $(IMAGE_NAME) 2>/dev/null || true
	@docker rm $(IMAGE_NAME) 2>/dev/null || true
	@docker compose down
	@docker run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)Service running on http://localhost:$(PORT)/docs$(NC)"

interactive: $(DOCKER_ID_FILE)
	@echo "$(YELLOW)Entering interactive shell...$(NC)"
	@docker run -it --rm \
		--entrypoint /bin/bash \
		$(IMAGE_NAME):$(IMAGE_TAG)

clean:
	@echo "$(YELLOW)Cleaning up...$(NC)"
	-docker stop $(IMAGE_NAME) 2>/dev/null || true
	-docker rm $(IMAGE_NAME) 2>/dev/null || true
	-docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	-docker compose down
	@rm -f $(DOCKER_ID_FILE)
	@echo "$(GREEN)Cleanup complete!$(NC)"

compose: clean
	@echo "$(YELLOW)Startin docker compose$(NC)"
	@docker compose up -d
	docker compose exec calculator bash -c "curl --version"
	@echo "$(GREEN)Service running on http://localhost:$(PORT)/docs$(NC)"

test: $(DOCKER_ID_FILE)
	@echo "$(YELLOW)Running unit and API tests...$(NC)"
	uv run pytest -v -m "api or unit or hypothesis" --hypothesis-show-statistics
	uv run pytest --cov=src -m "api or unit or hypothesis"
	@echo "$(GREEN)Tests complete!$(NC)"

test-docker:
	@echo "$(YELLOW)Running integration tests...$(NC)"
	uv run pytest -v -m integration
	uv run pytest --cov=src -m integration
	@echo "$(GREEN)Integration tests complete!$(NC)"


check-memory:
	@total_mem=$$(free -m | awk '/^Mem:/{print $$2}'); \
	container_count=$$(docker ps --format '{{.Names}}' | wc -l); \
	used_by_docker=$$(docker stats --no-stream --format "{{.MemUsage}}" | head -n$$container_count | awk '{split($$1,a,".");print a[1]}' | sed 's/[^0-9]//g' | awk '{sum+=$$1}END{print sum}') || echo 0; \
	available_mem=$$(free -m | awk '/^Mem:/{print $$7}'); \
	echo -e "$(YELLOW)Memory Status:$(NC)"; \
	echo -e "Total System Memory: $(GREEN)$$total_mem MB$(NC)"; \
	echo -e "Available Memory: $(GREEN)$$available_mem MB$(NC)"; \
	echo -e "Memory Used by Docker: $(GREEN)$$used_by_docker MB$(NC)"; \
	if [ $$available_mem -lt $(MIN_AVAILABLE_MEMORY) ]; then \
		echo -e "$(YELLOW)Warning: Less than 1GB memory available. System might become unstable.$(NC)"; \
	fi

help:
	@echo "Available targets:"
	@echo "  build        - Build Docker image if necessary"
	@echo "  run          - Run Docker container, build if necessary"
	@echo "  compose      - clean and run compose"
	@echo "  interactive  - Start interactive shell in container"
	@echo "  clean        - Remove container, image, and build artifacts"
	@echo "  test         - Run unit and API tests"
	@echo "  test-docker  - Run integration tests"
	@echo "  help         - Show this help message"
