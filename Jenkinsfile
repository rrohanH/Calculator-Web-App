pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME = 'calculator-web'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_REF = "${IMAGE_NAME}:${IMAGE_TAG}"
        APP_CONTAINER = 'calculator-web-app'
        TEST_CONTAINER = 'calculator-web-test'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t "$IMAGE_REF" -t "$IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                sh '''
                    docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true
                    docker run --name "$TEST_CONTAINER" -e PYTHONPATH=/app "$IMAGE_REF" pytest -q
                '''
            }
            post {
                always {
                    sh 'docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true'
                }
            }
        }

        stage('Run Application Container') {
            steps {
                sh '''
                    docker rm -f "$APP_CONTAINER" >/dev/null 2>&1 || true
                    docker run -d --name "$APP_CONTAINER" -p 5000:5000 "$IMAGE_REF"
                    sleep 5
                    curl --fail http://localhost:5000/health
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}
