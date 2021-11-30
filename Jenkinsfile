// pipeline {
//     agent any
//     environment {
//        registry = "alexeibarabash/moonactive-services"
//        container_name = "ma-time-service"
//     }
//     stages {
//         stage('build') {
//             steps {
//                 sh 'docker login '
//                 sh 'docker build -t ${registry}:${container_name}-$BUILD_NUMBER .'
//                 sh 'docker push ${registry}:${container_name}-$BUILD_NUMBER'
//             }
//         }
//         // stage('deploy') {
//         //     steps {
                
//         //     }
//         // }
//         // stage('test') {
//         //     steps {

//         //     }
//         // }
//    }
//    post {
//         always { 
//             cleanWs()
//         }
//     }
// }
#!groovy

def podLabel = "kaniko-${UUID.randomUUID().toString()}"

pipeline {
    agent {
        kubernetes {
            label podLabel
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins-build: app-build
    some-label: "build-app-${BUILD_NUMBER}"
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.5.1-debug
    imagePullPolicy: IfNotPresent
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: jenkins-docker-cfg
        mountPath: /kaniko/.docker
  volumes:
  - name: jenkins-docker-cfg
    projected:
      sources:
      - secret:
          name: docker-credentials
          items:
            - key: .dockerconfigjson
              path: config.json
"""
        }
    }

    environment {
      registry = "alexeibarabash/moonactive-services"
      container_name = "ma-time-service"
    }

    stages {

        stage('Checkout Code') {
            steps {
              checkout scm
            }
        }

        stage('Build with Kaniko') {
          steps {
            container(name: 'kaniko', shell: '/busybox/sh') {
              withEnv(['PATH+EXTRA=/busybox']) {
                sh '''#!/busybox/sh -xe
                  /kaniko/executor \
                    --dockerfile Dockerfile \
                    --context `pwd`/ \
                    --verbosity debug \
                    --insecure \
                    --skip-tls-verify \
                    --destination ${registry}:${container_name}-$BUILD_NUMBER
                '''
              }
            }
          }
        }

    }
}