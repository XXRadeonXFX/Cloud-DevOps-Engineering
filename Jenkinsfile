pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                    dir('sentiment-api') {
                        sh 'docker build -t sentiment-api:v1 .'
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Replace with your DockerHub credentials and repo
                    sh 'docker tag sentiment-api:v1 xxradeonxfx/sentiment-api:v1'
                    sh 'docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASS'
                    sh 'docker push xxradeonxfx/sentiment-api:v1'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Example deployment step (adjust as needed)
                    echo 'Deploying to server or cloud...'
                }
            }
        }
    }
}