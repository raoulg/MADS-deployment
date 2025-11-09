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

Start with the [README.md](./1-docker/README.md) file and follow the instructions there.


