pipeline {
    agent any
     tools {
        git 'Default'  // This refers to the Git installation name configured in Jenkins
    }
    environment {
        DOCKER_IMAGE_FLASK = "adityahub2255/flask-app"
        DOCKER_IMAGE_MYSQL = "adityahub2255/mysql"  // Define MySQL Docker image
        DOCKER_REGISTRY_CREDENTIALS = "dockerhub-creds" // Use your Docker registry credentials
        KUBE_NAMESPACE = "default" // Kubernetes namespace to deploy to
        DOCKER_TAG = "${GIT_COMMIT}" // Tag Docker images with the git commit ID
        KUBE_CONFIG = "/tmp/kubeconfig"
    }

    stages {
        stage('Fetch Code') {
            steps {
                // Checkout code from Git repository
                checkout scm
                sh 'ls -l $WORKSPACE'
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Run unit tests using pytest
                    sh 'pytest test_main.py --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                script {
                    // Build the Flask Docker image
                    docker.build("${DOCKER_IMAGE_FLASK}:${DOCKER_TAG}", ".")
                }
            }
        }

        stage('Docker compose down'){
            steps{
                script {
                    sh 'docker-compose down'
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    // Use Docker Compose to build and start the services defined in docker-compose.yaml
                    sh 'docker-compose -f docker-compose.yaml up --build -d'
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: DOCKER_REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    }

                    // Tag the MySQL image with the commit tag before pushing
                    sh "docker tag mysql:5.7 ${DOCKER_IMAGE_MYSQL}:${DOCKER_TAG}"

                    // Push the Flask Docker image to Docker Hub
                    sh "docker push ${DOCKER_IMAGE_FLASK}:${DOCKER_TAG}"

                    // Push the MySQL Docker image to Docker Hub
                    sh "docker push ${DOCKER_IMAGE_MYSQL}:${DOCKER_TAG}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                withCredentials([usernamePassword(credentialsId: 'aws-credentials-id',
                                                       usernameVariable: 'AWS_ACCESS_KEY_ID',
                                                       passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    // Check if kubeconfig file exists and display first 20 lines to verify it
                    sh 'ls -l $KUBE_CONFIG'
                    sh 'head -n 20 $KUBE_CONFIG'

                    // Set the KUBECONFIG environment variable and apply the Kubernetes manifests
                    sh 'export KUBECONFIG=$KUBE_CONFIG'
                    sh 'KUBECONFIG=$KUBE_CONFIG kubectl config view'
                    sh 'KUBECONFIG=$KUBE_CONFIG kubectl get nodes'

                    sh ' envsubst < $WORKSPACE/mysql-dep.yaml > $WORKSPACE/mysql-deployment-updated.yaml'
                    sh ' envsubst < $WORKSPACE/flask-dep.yaml > $WORKSPACE/flask-deployment-updated.yaml'

                    // Deploy Flask app and MySQL to Kubernetes
                    sh 'KUBECONFIG=$KUBE_CONFIG kubectl apply -f $WORKSPACE/mysql-deployment-updated.yaml -n ${KUBE_NAMESPACE}'
                    sh 'KUBECONFIG=$KUBE_CONFIG kubectl apply -f $WORKSPACE/flask-deployment-updated.yaml -n ${KUBE_NAMESPACE}'
                }
                }
            }
        }
    }

    post {
//         always {
//             // Clean up after the build
//             cleanWs()
//         }

        success {
            // Notify on success
            echo "Build and Deployment Successful!"
        }

        failure {
            // Notify on failure
            echo "Build or Deployment Failed!"
        }
    }
}
