# MADS deployment

## dependencies
### install docker

We need docker on the system where we want to deploy MADS.
Please go to the [docker website](https://docs.docker.com) to check how you can install docker on your machine.

For a ubuntu system like the VMs we use, you can run the script:

1. Following [SURF setup](./presentations/00-SURF-lab-setup.pdf), create an 'Ubuntu 22.04' VM with 1 core, 8GB of RAM.
2. Connect to the VM and clone this repo
3. run `./install-docker.sh`

### install uv
We will be using `uv`.
On macOS and Linux you can use:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
For other options, please check the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
