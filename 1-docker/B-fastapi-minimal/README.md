
# Minimal FastAPI with Docker
Because it is cumbersome to use the native python http server, we will use FastAPI to create a minimal web server.

However, this means we will need to install this as as a dependency.

## Dockerfile

We start by doing this as basic as possible. Because we are emulating a computersystem, completely isolated from the host machine, and because it is very easy to recreate the machine from scratch, we dont need to worry about setting up a virtual environment. The environment is already fully isolated, so no risk of dependency conflicts or confusion!

We will do this in the most basic way possible: with a requirements.txt file and a `pip install` command.

You can see in the `Dockerfile` that we:
- COPY the requirements.txt file to the working directory
- RUN `pip install` to install the dependencies listed in requirements.txt
- notice how we COPY the full src directory instead of just a single file
- study the additional arguments in the `pip install` command in the Dockerfile. What do they do? What would be the motivation to use them? Make sure you understand what each argument does. If you are unsure, [read the docs](https://pip.pypa.io/en/stable/cli/pip_install/)

## src/main.py
in the src folder, study the  `main.py` file.

What you see happening here is:
- we create a FastAPI app instance
- we define two routes: `/` and `/items/{item_id}`
- the first route returns a simple JSON response with "Hello": "World"
- the second route takes a path parameter `item_id` and an optional query parameter `q`, returning them in a JSON response
- finally, we run the app with uvicorn, specifying the host and port

## Makefile
The Makefile has become more complex. You can see that we are using variables. This way we can easily define arguments at the start of the file, which will make it easier to change them later.

## Excercise

- Copy the contents of the `Makefile` into your favorite Large Language Model, and ask questions about each part you dont fully understand.
- `make build` and `make run` the container
- test the two routes via your browser:
    - open your browser and go to `http://localhost:8000/` - you should see the JSON response `{"Hello": "World"}`
    - now go to `http://localhost:8000/items/42?q=hi` - you should see the JSON response `{"item_id": 42, "q": "hi"}`
- test it via curl:
    - run `curl http://localhost:8000/` - you should see the JSON response `{"Hello": "World"}`
    - run `curl "http://localhost:8000/items/42?q=hi"` - you should see the JSON response `{"item_id": 42, "q": "hi"}`. Note the quotes around the URL to prevent your shell from misinterpreting the `&` and `?` characters.
- modify the `main.py` file
    - modify the existing `/items` route to run a calculation on one of the parameters (for example, multiply `item_id` by 2 before returning it)
    - add a new route `/users/{username}` that returns a JSON response with the username and a welcome message. Test it via browser and curl.
- run `make interactive` to get a shell inside the running container
    - once inside, run `pip list` to see the installed packages. You should see FastAPI and Uvicorn listed.
    - check the src folder with commands like `ls src` and `cat src/main.py` .
    - test the command by running it manually from inside the container:
        - run `python src/main.py`.
        - stop it with `CTRL+C`
    - exit the interactive shell by typing `exit`
- run `make clean` to stop and remove the container
- check with `docker ps -a` that the container is removed

# More documentation

You can find more documentation about this setup on the [fastapi documentation](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi)
