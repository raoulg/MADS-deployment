# MADS deployment

## dependencies
### install docker

We need docker on the system where we want to deploy MADS.
On the VMs, you can run this command:
```bash
curl -sSL https://raw.githubusercontent.com/raoulg/serverinstall/refs/heads/master/install-docker.sh | bash
```

It will run the install-docker.sh script from my `serverinstall` repo. You can also find a copy of it in this repo.

1. Connect to the VM and clone this repo
2. Run the above command to install docker and docker-compose

For installing docker and docker-compose on other machines, please go to the [docker website](https://docs.docker.com) to check how you can install docker on your machine.

### install uv and sync the environment
We will be using `uv`.
On macOS and Linux you can use:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other options, please check the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/)

Use `uv sync` to sync the environment in the `pyproject.toml` file.

## Preparation and exercises
Watch this video for an intro to docker: https://www.youtube.com/watch?v=pg19Z8LL06w
It is about an hour, but it will answer all the beginners questions about docker.

# lesson 1
Make sure you have installed, before the lesson starts, all dependencies and test this by running the `1-docker/A-minimal` example.
Start with the [README.md](./1-docker/README.md) file and follow the instructions there.

During the lesson, there will be time to work on the other examples and we will cover questions on the exercises. You should finish exercise E before the next lesson.

# lesson 2
The uv-example folder just shows how you can use `uv` in a container. You can also use my own images, see [2-frontend/straattaal/README.md](./2-frontend/straattaal/README.md) for more details on that.

The 2-frontend/straattaal folder contains a small project that uses a trained language model to generate "street language" words. It contains both a frontend and a backend. The backend is a FastAPI application that serves the model, and the frontend is a simple HTML page that allows users to interact with the model. The `src` folder contains the model and training code; you will NOT need to publish the training code! Instead, train the model locally, and deploy the artefacts (the model weights) to the docker container; the backend will simply load the weights.

For your portfolio, you will need to deploy the straattaal application, trained on your own dataset, on SURF.

# lesson 3
This lesson focusses on building tests in general, and using hypothesis for property-based testing in particular.



