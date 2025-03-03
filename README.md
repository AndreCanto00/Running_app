# Running_app

[![Makefile CI](https://github.com/AndreCanto00/Running_app/actions/workflows/makefile.yml/badge.svg)](https://github.com/AndreCanto00/Running_app/actions/workflows/makefile.yml)

## Description.

Running_app is an application to calculate training load using various metrics such as TRIMP, TRIMP_LT, and HRRS. The application offers both a command-line interface (CLI) and a FastAPI-based web API.

## Installation.

To install the necessary dependencies, run the following command:

``sh
make install
```

## Usage

### CLI

To use the CLI, execute one of the following commands:

``sh
python loadCLI.py trimp
python loadCLI.py trimp_lt
python loadCLI.py hrrs
```

### Web API.

To start the FastAPI server, run:

```sh
uvicorn main:app --host 0.0.0.0 --port 8080
```

The API will be available at `http://localhost:8080`.



#### Endpoint

- `GET /`: Returns a welcome message.
- `POST /trimp/`: Calculates the TRIMP value.
- `POST /trimp_lt/`: Calculates the TRIMP_LT value.
- `POST /hrrs/`: Calculates the HRRS value.

## Tests.

To run tests, use the following command:

``sh
make test
```

## Formatting and Linting

To format the code and check the style, execute:

```sh
make format
make lint
```

## Contributions

Contributions are welcome! Feel free to open issue and pull request.

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.

## AWS App Runner.

For deployment to AWS App Runner, we use the `apprunner.yaml` file. This file contains the configurations needed to run the application on AWS App Runner.

### Configuration.

The `apprunner.yaml` file includes the following sections:

- `version`: The version of the configuration file.
- `runtime`: The runtime used by the application (in this case, Python 3).
- `build`: The commands needed to build the application.
- `run`: The command to run the application and network configuration.

### Example of `apprunner.yaml`.

```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  command: python -m uvicorn main:app --host 0.0.0.0 --port 8080
  network:
    port: 8080
```


### Deployment.

To deploy to AWS App Runner, follow these steps:

1. Log in to the AWS console and navigate to App Runner.
2. Create a new App Runner service.
3. Select the source code repository (e.g., GitHub) and configure the link.
4. Upload the `apprunner.yaml` file as the service configuration.
5. Start the service and wait for the deployment to complete.

Once complete, the application will be available at the address provided by AWS App Runner.
