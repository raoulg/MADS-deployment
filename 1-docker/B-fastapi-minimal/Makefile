# Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

# Variables
IMAGE_NAME := fastapi-app
IMAGE_TAG := latest
PORT := 8000

# Phony targets
.PHONY: build run interactive clean help

# Default target
.DEFAULT_GOAL := help

help:
	@echo "$(YELLOW)Available targets:$(NC)"
	@echo "  $(GREEN)build$(NC)       - Build Docker image"
	@echo "  $(GREEN)run$(NC)         - Run container in detached mode"
	@echo "  $(GREEN)interactive$(NC) - Enter container shell"
	@echo "  $(GREEN)clean$(NC)       - Remove container and image"

build:
	@echo "$(YELLOW)Building Docker image...$(NC)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "$(GREEN)Build complete!$(NC)"

run: build
	@printf "%sStopping and removing existing container...%s\n" "$(YELLOW)" "$(NC)"
	-docker stop $(IMAGE_NAME) 2>/dev/null || true
	-docker rm $(IMAGE_NAME) 2>/dev/null || true
	@echo "$(YELLOW)Starting container...$(NC)"
	docker run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)Service running on http://localhost:$(PORT)$(NC)"

interactive: build
	@echo "$(YELLOW)Entering interactive shell...$(NC)"
	docker run -it --rm \
		--entrypoint /bin/bash \
		$(IMAGE_NAME):$(IMAGE_TAG)

clean:
	@echo "$(YELLOW)Cleaning up...$(NC)"
	-docker stop $(IMAGE_NAME) 2>/dev/null || true
	-docker rm $(IMAGE_NAME) 2>/dev/null || true
	-docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"
