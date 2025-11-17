# slanggen

## train the model

First, build the environment with
```bash
uv sync --all-extras
```
We use `--all-extras` because we also want to install the optional packages (`fastapi`,` beautifulsoup4`.)

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

For the Dockerfile, you can use one of my prebuilt containers:
```docker
FROM raoulgrouls/torch-python-slim:py3.12-torch2.8.0-arm64-uv0.9.8
```

This will download a small container with python 3.12, torch 2.8.0 and uv 0.9.8 installed. Check my [hub.docker](https://hub.docker.com/r/raoulgrouls/torch-python-slim/tags) for the most recent builds. If you want to build images yourself, you can use my repository [here](https://github.com/raoulg/minimal-torch-docker)

Have a look at the [slanggen.toml](slanggen.toml) file; this contains the configuration for the data and model.
Modify the url to download your own dataset; probably the scraper will work for all dictionaries on [mijnwoordenboek.nl](https://www.mijnwoordenboek.nl),  but you might need to modify the scraper if you want to use a different source. Note that you need a dataset with at least about 400 words for the model to train properly.

train the model:
```bash
python src/slanggen/main.py
```

This should fill the `assets` folder with a file `straattaal.txt` and fill the `artefacts` folder with a trained model.

# Build and publish your artefact
Design science centers around creating an **artefact**. Off course, you could argue that a jupyter notebook is an artefact too, but it has a lot of downsides in terms of reproducibility, version control and deployment. A superior way is to package your code as a wheel file that can be installed via pip or uv.

You can build the `src/slanggen` package into a wheel with `uv` very easily, you just run:
```bash
uv build --clean
```
## What is a wheel and why use it?
A Python wheel is a pre-built package format (ending in `.whl`) that contains your code and metadata in a ready-to-install format, like a zip file specifically designed for Python packages. Unlike source distributions that need to be compiled during installation, wheels are already built, making installation much faster and more reliable—especially important when you're deploying to Docker containers where you want quick, reproducible builds.

When you run `uv build --wheel`, you're creating a single portable file that bundles your entire project with all its dependencies resolved, which you can simply copy into a Docker image or upload to PyPI for others to use. This means your data science models and pipelines become distributable artifacts that anyone (including your future self) can install with a single uv (or pip) command, without worrying about compilation errors or missing dependencies.

## Publish your wheel
You could simply share your wheel file by sending it to someone, but you have been using wheels since the first moment you did `pip install package`: in that case, a wheel is downloaded from an online repository like pypi or the conda channels.

`uv build` should produce a `dist` folder, and shoud add these two files:
```bash
❯ lsd dist
.rw-r--r--@ 9.5k username  4 Dec 14:35  slanggen-0.4.tar.gz
.rw-r--r--@ 6.0k username  4 Dec 14:35  slanggen-0.4-py3-none-any.whl
```

I published slanggen at [pypi](https://pypi.org/project/slangpy/) with uv (see `uv publish --help` for more info).
You could do the same after building the wheel, making an account on [pypi.org](https://pypi.org/) and generating an API token from pypi to publish. However, it is also possible to directly install from the wheelfile; with `uv` you could do this with `uv add /path/to/slanggen-0.4-py3-none-any.whl` in a new environment. So, for example, you could:

- create a Dockerfile
- mount or copy the wheel file into the container
- inside the dockerfile, you would like to have slanggen as a package, so you can `RUN uv add /path/to/slanggen-0.4-py3-none-any.whl` pointing to the location in the container.

Or, alternatively, you could copy the wheel file to some central location where your colleagues can access it (a webserver, an S3 bucket, a file share) and install it from there with `uv add http://path/to/slanggen-0.4-py3-none-any.whl`.

# test the backend
now test the `app.py` file:

```bash
python backend/app.py
```

This will show a webpage at http://127.0.0.1:80 and you should see a blue button "generate words" and a slider for temperatur. Click the button and see if it generates some words.

# Exercise
Create one (or more) Dockerfiles inside the `straataal` directory to dockerize the backend application, such that you can run it in a docker container and deploy it on SURF.
Use your own dataset that focusses on token-level prediction (eg some dialect words, medical terms, babynames, chemical names, etc)

create Dockerfiles that:
- [ ] uses small builds (eg use my torch-python-slim images)
- [ ] installs the requirements with uv for speed
- [ ] copies all necessary backend files. Pay special attention to required paths!
- [ ] study `backend/app.py` to see what is expected
- [ ] install the slanggen from the wheel instead of copying the full src folder
- [ ] expose port 80 in the Dockerfile (this way you can access it via SURF without the need to open additional ports)

create a Makefile that:
- [ ] checks for the wheel. If the wheel doesnt exist, use `uv` to let Make automatically create it
- [ ] checks if the trained model is present. If not, late Make train the file and create the model
- [ ] builds the docker image, if the wheel and model exist.
- [ ] runs the docker on port 80
- [ ] test if you can access the application via SURF

Finally:
- [ ] implement a `docker-compose.yml` file; this way you can make sure that the service starts up automatically after you pause and resume the instance on SURF.
- [ ] publish your artefact on SURF, and hand in the URL

Optionally:
- [ ] try to improve the frontend GUI; for example, add a dropdown with starting letters, or add some nice CSS styling
- [ ] play around with your favorite dataset to generate some nice words
