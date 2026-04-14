# Calculator Web App - Project Documentation

## 1. Project Overview

This project is a Python-based calculator web application built with Flask.
The application is containerized with Docker and automated through a Jenkins pipeline.

Primary goals:
- Provide a simple browser calculator UI
- Evaluate expressions safely on the server side
- Run tests in CI before starting the application container
- Keep deployment flow simple and reproducible with Docker

## 2. Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Testing: pytest
- Runtime server: gunicorn
- Containerization: Docker
- CI/CD: Jenkins Pipeline

## 3. Project Structure

- app.py: Flask routes and API endpoints
- calculator.py: Safe expression evaluation logic
- templates/index.html: Calculator page UI
- static/style.css: Styling
- static/script.js: Browser behavior and API calls
- tests/test_calculator.py: Unit tests
- Dockerfile: Container image definition
- Jenkinsfile: CI/CD pipeline stages
- requirements.txt: Python dependencies

## 4. Application Flow

1. User opens the calculator page in a browser.
2. User submits an expression.
3. Frontend sends expression to POST /api/calculate.
4. Backend validates and evaluates expression using AST-safe parser.
5. Backend returns result JSON or error JSON.

## 5. API Endpoints

- GET /
  - Serves calculator UI page.

- GET /health
  - Returns service health status.
  - Example response: {"status":"ok"}

- POST /api/calculate
  - Request body: {"expression":"(12 + 8) * 4 / 2"}
  - Success response: {"result":40.0}
  - Error response: {"error":"Invalid expression."}

## 6. Safe Expression Evaluation

The evaluator in calculator.py uses Python AST and allows only:
- Numeric constants
- Binary operators: +, -, *, /, %, **
- Unary operators: + and -
- Parentheses

Any unsupported syntax or unsafe pattern is rejected with a controlled error.

## 7. Docker

### 7.1 Build Image

Run from project root:

docker build -t calculator-web:latest .

### 7.2 Run Container

docker run --rm -p 5000:5000 calculator-web:latest

Access app at:
http://localhost:5000

### 7.3 Run Tests in Container

docker run --rm calculator-web:latest python -m pytest -q

## 8. Jenkins Pipeline

The Jenkins pipeline in Jenkinsfile performs:

1. Checkout source from GitHub
2. Build Docker image tagged with build number and latest
3. Run pytest inside the built image
4. Start the application container
5. Run health check on http://localhost:5000/health
6. Prune unused Docker images in post actions

## 9. Jenkins Setup Steps

1. Install Jenkins on a machine with Docker and Git.
2. Ensure Jenkins user has permission to run Docker.
3. Create a Pipeline job.
4. Select Pipeline script from SCM.
5. Choose Git and set repository URL:
   https://github.com/rrohanH/Calculator-Web-App.git
6. Set branch to main.
7. Save and run Build Now.

Optional:
- Add GitHub webhook to trigger builds on push.

## 10. Common Issues and Fixes

- ModuleNotFoundError during pytest in container:
  - Use python -m pytest -q inside container (already configured in Jenkinsfile).

- Port 5000 already in use:
  - Stop old container or run with a different host port.

- Jenkins can clone but cannot run Docker:
  - Add Jenkins user to docker group (Linux) or ensure Docker Desktop permissions (Windows).

## 11. Expected Successful Pipeline Output

- Docker image build completes
- Tests pass
- Health check returns status ok
- Console shows app access URL

## 12. Future Improvements

- Push Docker images to a registry (Docker Hub or ECR)
- Add stage for security scanning
- Add integration tests for API endpoints
- Parameterize port and container name via Jenkins build parameters
