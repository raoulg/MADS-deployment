# Explore the files
## src
- how does the src/calculator work?
    - check `__init__.py` to see how `__all__` works
    - check `calculator.py` to understand the basic calculator 
    - check `main.py` to see how I setup `main()` to run the server 

## pyproject.toml
- check how I add `project.script`. Do you understand what the script does?

## run the tests
First, install with uv (you already have that if you have rye)
- make sure you have >0.5.2 with `uv --version`, else do `uv self update`
- run `uv sync`
- now, run `make test`

Study the outputs of the tests. Check the different types of tests: 
- api
- caclulator
- hypothesis

What do you think about the differences that hypothesis adds?
Why do you think hypothesis needs things like `epsilon`? If you dont understand why, set `epsilon=0` and run the tests again.
Can you understand what is going on?

Study hypothesis statistics: why are some tests invalid?

Study coverage. 
- can you increase coverage by adding a new test?

## Makefile
Study the makefile. 
Do you understand the motivation for the DOCKER_ID_FILE test?

Do you understand how `@pytest.mark` interacts with `pytest -m` ? 
If not, study the testfiles 
In addition to that, check the pyproject.toml file to see how the marks are added.

## run compose
- first do `make compose`
- then check with `docker ps` the healthcheck
- test the api with [http://localhost:8000/docs](http://localhost:8000/docs)
# Build your own tests
Now, add tests to `straattaal` from lesson 2

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

Learning Goals:

Understanding API testing with FastAPI's TestClient
Testing HTTP status codes and response content
Testing stateful operations (starred words list)

## Exercise 2: Property-Based Testing
Create a test file tests/test_generation.py that uses Hypothesis to test the word generation functionality:

- Test that generated words are always strings
- Test that the number of generated words matches the requested amount
- Test that temperature affects word diversity (higher temperature = more diverse words)
- Test that generated words are within reasonable length limits

Learning Goals:

Understanding property-based testing with Hypothesis
Testing stochastic processes
Working with random number generators and seeds

## Exercise 3: Model and Tokenizer Testing
Create a test file tests/test_model.py that tests the model and tokenizer functionality:

Test model loading:
- Test correct loading of tokenizer
- Test correct loading of model configuration
- Test handling of missing files

Test tokenizer properties:
- Test tokenization reversibility
- Test handling of unknown characters
- Test maximum sequence length handling

Learning Goals:
Testing file operations and error handling
Testing ML model properties
Understanding model loading and configuration

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
- Add pytest-cov and achieve >90% test coverage
- Implement pre-commit hooks for test running
