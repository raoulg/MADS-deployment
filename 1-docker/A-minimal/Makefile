PHONY: build run

build:
	@echo "building docker image"
	docker build -t my-python-app:latest .

run:
	docker run -d -p 8000:8000 my-python-app:latest
	@echo "running on http://localhost:8000"
