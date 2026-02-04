pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building Docker Image...'
                // Real logic will be added in the CI Integration phase
                // sh 'docker build -t my-app:${BUILD_NUMBER} .'
            }
        }
        stage('Test') {
            steps {
                echo 'Running Unit Tests...'
                // Source [4]: "Secure CI Pipelines... run in isolation"
            }
        }
    }
}

