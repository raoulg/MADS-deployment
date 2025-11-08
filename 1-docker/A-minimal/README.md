# 1. minimal example

## 1.1.Dockerfile
I wanted to make a docker file that is as minimal as possible, while still being functional.

What you see happening in the Dockerfile is:
- Using a minimal base image (python:3.12-slim)
- changing the working directory to /app
- copying the app.py file to the working directory
- exposing port 8000 (to be able to access the app from outside the container via port 8000)
- finally, running the app with python app.py

You can see this as an isolated computer. This Dockerfile will emulate a linux machine with python 3.12 preinstalled, and the app.py file. This computer is completely isolated from your host machine, and it has just enough installed to run the app.py file.

## 1.2 app.py
This is a minimal web server. It is created without external dependencies, using only the built-in http.server module.

the SimpleHTTPRequestHandler class handles incoming GET requests, sending back a simple HTML response with the message "Hello from Python Container!".

When you run this app inside the docker container, it will start a web server listening on port 8000.

# 2. excercises

## 2.1 Build and run the container
- cd into the `1-docker/A-minimal` directory
- have a look at the Makefile. Either execute `make build` or run the commands manually by typing `docker build -t my-python-app:latest .`
- once it is built, run it with `make run` (or, run the command manually)
- for run `docker ps` to see all your running containers. This should include your `my-python-app:latest` container.
- test it:
    - the container should be running. Open your browser and go to `http://localhost:8000`.
    - test the container without browser from the cli by running `curl http://localhost:8000`
    - you should see the message "Hello from Python Container!" in both cases

# 2.2 cleanup
- run `docker ps -a` to see all your containers (running and stopped). Under CONTAINER_ID and NAMES you will see the id and name of your container.
- stop the container if it is still running: `docker stop <CONTAINER_ID or NAME>`
- now remove the container: `docker rm <CONTAINER_ID or NAME>`

The NAMES are randomly generated if you don't specify a name when running the container. To make it easier to stop and remove, you can name a container when running it with the `--name` flag:

```bash
docker run -d -p 8000:8000 --name my-python-container my-python-app:latest
```

- run the container with a specific name
- now stop and remove it, using the name you just specified.

# tip
Have a look at `lazydocker` (you can find the docs here [https://github.com/jesseduffield/lazydocker](https://github.com/jesseduffield/lazydocker)). This gives you a terminal UI to manage your docker containers and images. It makes it easy to see what is running, stop and remove containers, and see logs.


