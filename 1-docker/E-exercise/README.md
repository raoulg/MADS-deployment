# Dockerizing a data science algorithm pipeline

In this folder, you will find inside the `notebooks/` folder three notebooks. The algorithm is not relevant right now; this is just an example of a typical data science project.

This is also a typical product of a data science project: you started with data ingestion, did some preprocessing, designed and tested an algorithm, and now you have 3 notebooks (or more) that are the elements of your datascience pipeline.

However, there is a major issue if you stop here. Sure, some data scientists proudly say "yeah i do data science, someone else should put it in production" but i firmly believe that this will reduce your value as a data scientist. Sure, there are lots of companies that let you get away with this attitude. However, having at least some idea of how this process works will make collaborating with colleagues that do deployment much easier.

## Split up the process
A main idea is, to split up the process in different steps. We can identify:
- collecting the raw data
- preprocessing the raw data
- running the algorithm on the preprocessed data and visualizing the results

If we isolate these steps into docker containers, we have a few advantages in prodcution:
- for each step, it doesnt really matter what happens inside the container; we only care about input and output, and some API endpoints. This makes it easier to improve, change or modify each step without breaking the entire pipeline.
- each step can be scaled independently. For example, if data ingestion is slow, we can run multiple instances of the ingestion container in parallel.
- each step can be monitored independently. If one step fails, it is easier to identify and fix the issue.

## Exercise

focus on creating three dockerfiles, one for each step of the pipeline. You can use the existing notebooks as a starting point.

The get you started, i created a `docker-compose.yml` file that defines three services: `ingest`, `preprocess` and `model`.

- create folders for every step of the process
- for every folder, create a python file based on the notebook that implements the logic of that step
- make sure to install the necessary dependencies for python in each container
- create a dockerfile for each step that installs the necessary dependencies and runs the python script

While developing, you could use docker to test individual steps by specifying a specific dockerfile with the `-f` flag, for example:

```bash
docker build -t mads-ingest -f ingest/ingest.Dockerfile .
```

and when running the example, you can use the `-v` flag to mount local directories for data and logs, for example:
```bash
docker run \
    -v ./data:/app/data \
    -v ./logs:/app/logs mads-ingest
```

However, in the end you should be able to connect everything with `docker compose`, so that you can run the entire pipeline in a network.
