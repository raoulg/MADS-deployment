# slanggen

First, build the environment with
```bash
uv sync --all-features
```
We use `--all-features` because we also want to install the optional packages (`fastapi`,` beautifulsoup4`.)

and activate on UNIX systems with
```bash
source .venv/bin/activate
```

Note how I added to the pyproject.toml:
```toml
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

This makes sure that you dont download an additional 2.5GB of GPU dependencies, if you dont need them. This can be essential in keeping the container within a manageable size.

Another option for the Dockerfile is to use one of my prebuilt containers:
```docker
FROM raoulgrouls/torch-python-slim:py3.11-torch2.7.1-arm64-uv0.8.13
```

This will download a small container with python 3.11, torch 2.7.1 and uv 0.8.13 installed.

check my [hub.docker](https://hub.docker.com/r/raoulgrouls/torch-python-slim/tags) for the most recent builds. If you want to build images yourself, you can use my repository [here](https://github.com/raoulg/minimal-torch-docker)

train the model:
```bash
python src/slanggen/main.py
```

This should fill the `assets` folder with a file `straattaal.txt` and fill the `artefacts` folder with a trained model.
Check this with `ls`

If everything works as expected, you can build the `src/slanggen` package into a wheel:
```bash
uv build --clean
```

I published slanggen at [pypi](https://pypi.org/project/slangpy/) which you can do with
`uv publish` after making an account on pypi.org and generating an API token.

`uv build` should produce a `dist` folder, and shoud add these two files:
```bash
❯ lsd dist
.rw-r--r--@ 9.5k username  4 Dec 14:35  slanggen-0.3.1.tar.gz
.rw-r--r--@ 6.0k username  4 Dec 14:35  slanggen-0.3.1-py3-none-any.whl
```

With this, you can now run

```bash
cd backend
python app.py
```
And this will start an api at http://127.0.0.1:80
Test if everything works as expected.

# Exercise
- split up straattaal into multiple dockerfiles
create Dockerfiles that:
- uses small builds (for example, of torch)
- installs the requirements with uv
- copies all necessary backend files. Pay special attention to required paths!
- study `backend/app.py` to see what is expected
- install the slanggen from the wheel
- expose port 80

create a Makefile that:
- checks for the wheel. If the wheel doesnt exist, use `uv` to build it
- checks if the trained model is present. If not, train the file.
- builds the docker image, if the wheel and model exist
- runs the docker on port 80
- test if you can access the application via SURF

Finally:
- implement docker-compose.yml for straattaal
