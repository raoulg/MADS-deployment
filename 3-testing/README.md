# Code selfstudy guide
## pyproject.toml

- check the `project.script` section. Which function is called? Check this function in the codebase.
- what should happen when you run `calculator` from the command line?
- test your answer by `cd`-ing into `3-testing`, running `uv sync` and then type `calculator` in your terminal.

## src
### __init__.py
- what do you think is the purpose of `__all__`?
- have a look at `tests/test_calculator.py`. Can you relate the imports here to the `__all__` variable?

### calculator.py and api.py
- check `calculator.py` to understand the basic calculator
- now look at `api.py` and trace back how the endpoints are using the calculator functions
- study the `/health` endpoint: what do you think is being catched here? Can you think of errors that might be missed by the healthcheck?

## tests

look at `test_calculator.py`.
    - What is being tested? And what not? First try to think about issues this approach might miss.

Now look at `test_hypothesis.py`.
- What would be the motivation for `@given`?
- Why would we need an additional check with `assume` in python? (hint: it has to do with what type the input is)
- what is being improved by the commutativity and identity tests that was not covered before?
- change the `epsilon` value in the `test_divide` function to `0` and run the tests again. What happens? Why do you think that is? Would you have found that without hypothesis?
- How would you improve the `test_add_zero` function with hypothesis?

study `test_api.py` and `test_integration.py`
- Why do you think using hypothesis in these files is NOT a good idea?


## Makefile
- trace back the dependencies of `test`; what are dependencies doing?
- `wildcard` is a Make function that will find all files matching a pattern. Can you understand what is happening here? Why would we want to have a lot of files as dependencies for the `DOCKER_ID_FILE` target?
- Do you understand the motivation for the DOCKER_ID_FILE test?

Do you understand how `@pytest.mark` interacts with `pytest -m` ?
If not, go back to the testfiles
In addition to that, check the pyproject.toml file to see how the marks are added.

# run the tests
After having studied all the components, run the tests.
First, install with uv all dependencies:
- `cd` into the 3-testing folder and run `uv sync`
- either run `make test`, or, manually build the docker image and then run the pytest commands

Study the outputs of the tests. Check the different types of tests:
1. api
1. caclulator
1. hypothesis

- What do you think about the differences that hypothesis adds?
- Why do you think hypothesis needs things like `epsilon`? If you dont understand why, set `epsilon=0` and run the tests again.

Study hypothesis statistics: why are some tests invalid? Is that an issue?

Study coverage.
- can you increase coverage by adding a new test?

# docker compose
- first do `make compose`
- then check with `docker ps` the healthcheck
- test the api manually with [http://localhost:8000/docs](http://localhost:8000/docs)

# Improve straattaal
You will improve your implementation of straattaal with tests.

## Exercise 1: Basic API Testing
Create a test file tests/test_api.py that tests the basic functionality of the FastAPI endpoints:

1. Test the /health endpoint
2. Test the /generate endpoint with different parameters:
    - Default parameters (10 words, temperature 1.0)
    - Custom number of words
    - Different temperature values
3. Test the starred words functionality:
    - Adding a word
    - Adding a duplicate word (should not duplicate)
    - Removing a word
    - Getting the starred words list

LLMs are pretty good at generating tests; just make sure you read through the tests. Go for quality over quantity. A suggestion for a prompt would be:

```
[insert backend/app.py from the straattaal repo]
I want to generate api tests for the FastAPI app above using FastAPI's TestClient.
Make sure to cover edge cases and error handling in addition to basic functionality.
Dont start testing right away; first, discuss with me what you want to test and why. Discuss your motivation, and give me the chance to learn about how you approach testing.

Only after we have discussed the approach, you can generate the tests
```

Use coverage to find untested parts of the code, and discuss these with the LLM to generate additional tests when relevant.

Learning Goals:

- Understanding API testing with FastAPI's TestClient
- Testing HTTP status codes and response content
- Testing stateful operations (starred words list)

## Exercise 2: Property-Based Testing
Create a test file tests/test_generation.py that uses Hypothesis to test the word generation functionality. Some properties to test:

- Test that generated words are always strings
- Test that the number of generated words matches the requested amount
- Test that generated words do not exceed the maximum length

Learning Goals:

- Understanding property-based testing with Hypothesis
- Testing stochastic processes
- Working with random number generators and seeds

## Exercise 3: Model and Tokenizer Testing
Create a test file tests/test_model.py that tests the model and tokenizer functionality:

Test model loading:
- Test correct loading of tokenizer
- Test correct loading of model configuration
- Test handling of missing files

Test tokenizer properties:
- The tokenizer will encode/decode. Build an additional function that uses the tokenizer to encode and decode a word, and test that the output matches the input (tokenization reversibility), i.e. word == decode(encode(word))
- if you find errors that the user could actually encounter, can you make the code more robust? E.g by adding error handling or by adding constraints to the inputs?

Learning Goals:
- Testing file operations and error handling
- Testing ML model properties
- Understanding model loading and configuration

# Exercise 4: Integration Testing with Docker
Create a test file tests/test_integration.py that tests the entire system running in Docker:

Test the complete workflow:
- Generate words
- Star some words
- Unstar words
- Verify persistence

Test error recovery:
- Invalid inputs

Learning Goals:
Understanding Docker-based testing
Error handling in a containerized environment

## Bonus Exercise: Test Coverage and Quality
- Implement pre-commit hooks for test running
- Add pytest-cov and achieve >70% test coverage
