The student understands:

- what the motivation is for docker-compose
- how docker compose can specify dependencies
- what basic commands (compose up, compose down, ps) do
- what the tradeoff is between using pip and rye/uv
- what the syntax is of a Makefile (target, prerequisites, recipe) and how this works with a chain of dependencies
- what a `.whl` file is and why/how it is used

The student can:
- use `uv` in a container
- move from a sequence of manual building steps (install dependencies, ingest data, train model, build wheel) to a Makefile that automates these steps 
- separate the training code (train, save weights) from the code necessary for inference (import weights and trained model), and deploy that in a container
- create a small container with cpu only torch

