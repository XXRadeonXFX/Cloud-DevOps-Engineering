pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "sentiment-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        REGISTRY = "xxradeonxfx"  
    }

    stages {
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
                        docker-compose build
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                script {
                    sh '''
                        # Test API health
                        docker-compose up -d
                        sleep 10
                        
                        # Test endpoint
                        curl -X POST http://localhost:8000/predict \
                          -H "Content-Type: application/json" \
                          -d '{"text": "This is great!"}' || exit 1
                        
                        echo "✅ API test passed!"
                    '''
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'  // Only push from main branch
            }
            steps {
                echo 'Pushing to Docker Hub...'
                script {
                    sh '''
                        docker tag sentiment-api:latest ${REGISTRY}/sentiment-api:${DOCKER_TAG}
                        docker tag sentiment-api:latest ${REGISTRY}/sentiment-api:latest
                        
                        # Login and push (add credentials in Jenkins)
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
                echo '🚀 Deploying application...'
                script {
                    sh '''
                        docker-compose down
                        docker-compose up -d
                        echo "Deployment complete!"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
