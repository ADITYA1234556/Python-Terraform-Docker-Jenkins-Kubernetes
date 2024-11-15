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
    }

    stages {
        stage('Fetch Code') {
            steps {
                // Checkout code from Git repository
                checkout scm
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                script {
                    // Build the Flask Docker image
                    docker.build(DOCKER_IMAGE_FLASK, ".")
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

//         stage('Run Unit Tests') {
//             steps {
//                 script {
//                     // Run unit tests using pytest
//                     sh 'pytest tests/ --maxfail=1 --disable-warnings -q'
//                 }
//             }
//         }

        stage('Push Docker Images') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: DOCKER_REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    }

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
                    // Use the kubeconfig stored in Jenkins as the Kubeconfig file
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                        // Set KUBECONFIG environment variable to the location of the kubeconfig file
                        sh 'export KUBECONFIG=$KUBECONFIG_FILE'

                        // Deploy Flask app and MySQL to Kubernetes
                        sh 'kubectl apply -f mysql-deployment.yaml -n ${KUBE_NAMESPACE}'
                        sh 'kubectl apply -f flask-app-deployment.yaml -n ${KUBE_NAMESPACE}'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up after the build
            cleanWs()
        }

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