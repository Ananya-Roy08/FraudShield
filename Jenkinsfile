pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                sh '''
                    python3 -m venv .ci-venv
                    . .ci-venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install fastapi uvicorn scikit-learn joblib numpy pandas pytest httpx build
                '''
            }
        }

        stage('Automated Tests (pytest)') {
            steps {
                sh '''
                    . .ci-venv/bin/activate
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    . .ci-venv/bin/activate
                    python -m build
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'FraudShield CI pipeline succeeded and .whl artifact was archived.'
        }
        failure {
            echo 'FraudShield CI pipeline failed. Check console output for details.'
        }
    }
}