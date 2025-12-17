pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "sentiment-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        REGISTRY = "xxradeonxfx"  
    }
    
    stages {
        stage('Initial Cleanup') {
            steps {
                echo 'Cleaning up old Docker resources...'
                script {
                    sh '''
                        docker compose down || true
                        docker container prune -f || true
                        docker image prune -f || true
                        docker volume prune -f || true
                        docker network prune -f || true
                        docker system prune -f || true
                        
                        echo "Initial cleanup complete"
                        docker system df
                    '''
                }
            }
        }
        
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                script {
                    sh '''
                        docker compose build
                    '''
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                echo 'Pushing to Docker Hub...'
                script {
                    sh '''
                        docker tag sentiment-api:latest ${REGISTRY}/sentiment-api:${DOCKER_TAG}
                        docker tag sentiment-api:latest ${REGISTRY}/sentiment-api:latest
                        
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker push ${REGISTRY}/sentiment-api:${DOCKER_TAG}
                        docker push ${REGISTRY}/sentiment-api:latest
                    '''
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying application...'
                script {
                    sh '''
                        docker compose down
                        docker compose up -d
                        echo "Deployment complete"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Final cleanup...'
            script {
                sh '''
                    docker compose down || true
                    docker image prune -f || true
                    docker container prune -f || true
                    docker system prune -f || true
                    
                    echo "Disk usage after cleanup:"
                    docker system df
                    
                    echo "Cleanup complete"
                '''
            }
        }
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
