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
        stage('Deploy Helm') {
          agent {
           kubernetes {
              containerTemplate {
                   name 'helm'
                   image 'alexeibarabash/moonactive-services:jenkins-custom-slave-v1'
                   ttyEnabled true
                   command 'cat'
              }
            }
          }
          steps {
            container('helm') { 
                 checkout scm
                 sh "helm upgrade -i ${container_name} ./k8s/ma-services --namespace default --set image.repository=${registry},image.tag=${container_name}-$BUILD_NUMBER --wait"
               } 
          }
        }
    }
}