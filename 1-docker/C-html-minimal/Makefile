# Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

# Variables
IMAGE_NAME := imgshow
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

# you will first need to run the 3.model notebook to save the image
# then, we can create a directory and copy the image to it
# this will check if img/clustering.png exists, if not, it will run the command
# this recipe depends on ../img/clustering.png, and if that file changes, this will run
# it uses automatic variables ($< for the first prerequisite and $@ for the target name)
img/clustering.png: ../img/clustering.png
	mkdir -p img
	cp $< $@

build: img/clustering.png
	@echo "$(YELLOW)Building Docker image...$(NC)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "$(GREEN)Build complete!$(NC)"

run: clean build
	@echo "$(YELLOW)Starting container...$(NC)"
	docker run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)Service running on http://localhost:$(PORT)$(NC)"
	@echo "$(GREEN)View image on on http://localhost:$(PORT)/show$(NC)"

interactive: build
	@echo "$(YELLOW)Entering interactive shell...$(NC)"
	docker run -it --rm \
		--entrypoint /bin/bash \
		$(IMAGE_NAME):$(IMAGE_TAG)

stop:
	@echo "$(YELLOW)Stopping container...$(NC)"
	-docker stop $(IMAGE_NAME) 2>/dev/null || true
	@echo "$(GREEN)Container stopped!$(NC)"

clean: stop
	@echo "$(YELLOW)Cleaning up...$(NC)"
	-docker rm $(IMAGE_NAME) 2>/dev/null || true
	-docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	-rm -rf img
	@echo "$(GREEN)Cleanup complete!$(NC)"