pipeline{
    agent any
    stages{
    stage('Checkout-Repo'){
        checkout scm
    }
    stage('Echo-Message') {
        steps {
            echo 'This is an echo message from Jenkins pipeline!'
        }
    }
    }

}