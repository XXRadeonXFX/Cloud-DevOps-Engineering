pipeline {
    agent any

    stages {
        stage('Checkout-Repo') {
            steps {
                checkout scm
            }
        }

        stage('Echo-Message') {
            steps {
                echo 'This is an echo message from Jenkins pipeline!'
            }
        }
    }
}
