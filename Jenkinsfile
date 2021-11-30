pipeline {
    agent any
    environment {
       registry = "alexeibarabash/moonactive-services"
       container_name = "ma-time-service"
    }
    stages {
        stage('build') {
            steps {
                sh 'docker login '
                sh 'docker build -t ${registry}:${container_name}-$BUILD_NUMBER .'
                sh 'docker push ${registry}:${container_name}-$BUILD_NUMBER'
            }
        }
        // stage('deploy') {
        //     steps {
                
        //     }
        // }
        // stage('test') {
        //     steps {

        //     }
        // }
   }
   post {
        always { 
            cleanWs()
        }
    }
}