# Calculator Web App (Python + Docker + Jenkins)

A Python calculator web application built with Flask, containerized with Docker, and delivered through a Jenkins pipeline.

## Features

- Safe server-side expression evaluation (+, -, *, /, %, **, parentheses)
- Browser UI with keypad and expression input
- Health endpoint for container smoke checks
- Unit tests with pytest

## Run with Docker

```bash
docker build -t calculator-web:latest .
docker run --rm -p 5000:5000 calculator-web:latest
```

Open http://localhost:5000

## Run Tests

```bash
docker run --rm -e PYTHONPATH=/app calculator-web:latest pytest -q
```

## Jenkins Pipeline

The `Jenkinsfile` orchestrates the following stages:

1. Checkout source from SCM.
2. Build Docker image and tag with `BUILD_NUMBER` and `latest`.
3. Run unit tests with `pytest` inside the built Docker image.
4. Start the application container and call `/health`.

### Jenkins Prerequisites

- Jenkins agent with Docker and curl installed
- Docker daemon accessible to Jenkins user
- Pipeline job configured from this repository

After a successful run, the app is available at http://<jenkins-agent-host>:5000
