pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        // Base name used for the Docker image built by the pipeline.
        IMAGE_NAME = 'calculator-web'
        // Jenkins build number used to create a unique image tag.
        IMAGE_TAG = "${BUILD_NUMBER}"
        // Fully qualified image reference used across build and run stages.
        IMAGE_REF = "${IMAGE_NAME}:${IMAGE_TAG}"
        // Container name used for the running application instance.
        APP_CONTAINER = 'calculator-web-app'
        // Temporary container name used to run pytest inside the image.
        TEST_CONTAINER = 'calculator-web-test'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub.'
                // Pull the exact revision referenced by the Jenkins job.
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building the application Docker image.'
                // Build and tag the application image for this pipeline run.
                sh '''
                    echo "Docker build started for ${IMAGE_REF}"
                    docker build -t "$IMAGE_REF" -t "$IMAGE_NAME:latest" .
                    echo "Docker build finished for ${IMAGE_REF}"
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                echo 'Running pytest inside the built Docker image.'
                // Run the test suite inside the built image to verify the package and imports.
                sh '''
                    echo "Removing any old test container: ${TEST_CONTAINER}"
                    docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true
                    echo "Starting test container from image: ${IMAGE_REF}"
                    docker run --name "$TEST_CONTAINER" "$IMAGE_REF" python -m pytest -q
                    echo "Tests completed successfully inside ${TEST_CONTAINER}"
                '''
            }
            post {
                always {
                    // Remove the temporary test container even if the stage fails.
                    sh 'docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true'
                }
            }
        }

        stage('Run Application Container') {
            steps {
                echo 'Starting the application container and checking the health endpoint.'
                // Start the application container and verify the health endpoint.
                sh '''
                    echo "Removing any old application container: ${APP_CONTAINER}"
                    docker rm -f "$APP_CONTAINER" >/dev/null 2>&1 || true
                    echo "Starting application container from image: ${IMAGE_REF}"
                    docker run -d --name "$APP_CONTAINER" -p 5000:5000 "$IMAGE_REF"
                    echo 'Waiting for the app to start before health check.'
                    sleep 5
                    echo 'Checking /health endpoint.'
                    curl --fail http://localhost:5000/health
                    echo 'Health check passed.'
                    echo 'Access the web app at: http://localhost:5000'
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up unused Docker image layers.'
            // Remove unused Docker image layers created during the build.
            sh 'docker image prune -f || true'
        }
    }
}
