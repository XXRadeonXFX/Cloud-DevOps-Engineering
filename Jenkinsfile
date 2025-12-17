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
        
        stage('Test APIs') {
            steps {
                echo 'Testing APIs...'
                script {
                    sh '''
                        # Start containers
                        docker compose up -d
                        echo "Waiting for services to be ready..."
                        sleep 15
                        
                        # Test 1: Check root endpoint
                        echo "Testing root endpoint..."
                        response=$(curl -s http://localhost:8000/)
                        echo "Response: $response"
                        if echo "$response" | grep -q "Sentiment Analysis API is running"; then
                            echo "PASS: Root endpoint working"
                        else
                            echo "FAIL: Root endpoint failed"
                            exit 1
                        fi
                        
                        # Test 2: Positive sentiment prediction
                        echo "Testing positive sentiment..."
                        response=$(curl -s -X POST http://localhost:8000/predict \
                          -H "Content-Type: application/json" \
                          -d '{"text": "This is amazing and wonderful!"}')
                        echo "Response: $response"
                        if echo "$response" | grep -q "sentiment"; then
                            echo "PASS: Predict endpoint working"
                        else
                            echo "FAIL: Predict endpoint failed"
                            exit 1
                        fi
                        
                        # Test 3: Negative sentiment prediction
                        echo "Testing negative sentiment..."
                        response=$(curl -s -X POST http://localhost:8000/predict \
                          -H "Content-Type: application/json" \
                          -d '{"text": "This is terrible and awful"}')
                        echo "Response: $response"
                        
                        # Test 4: Check history endpoint
                        echo "Testing history endpoint..."
                        response=$(curl -s http://localhost:8000/history?limit=5)
                        echo "Response: $response"
                        if echo "$response" | grep -q "predictions"; then
                            echo "PASS: History endpoint working"
                        else
                            echo "FAIL: History endpoint failed"
                            exit 1
                        fi
                        
                        # Test 5: Check second API on port 4000
                        echo "Testing second API..."
                        response=$(curl -s http://localhost:4000/)
                        echo "Response: $response"
                        if echo "$response" | grep -q "Sentiment"; then
                            echo "PASS: Second API working"
                        else
                            echo "WARN: Second API may not be responding"
                        fi
                        
                        echo "All API tests completed successfully"
                        
                        # Stop containers after testing
                        docker compose down
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
