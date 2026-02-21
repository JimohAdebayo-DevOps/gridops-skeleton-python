pipeline {
    agent {
        kubernetes {
            // Ephemeral Agent with Kaniko for building images
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: kaniko
                image: gcr.io/kaniko-project/executor:debug
                command:
                - /busybox/cat
                tty: true
                volumeMounts:
                  - name: docker-config
                    mountPath: /kaniko/.docker
              volumes:
                - name: docker-config
                  secret:
                    secretName: dockerhub-creds-kaniko
                    items:
                      - key: .dockerconfigjson
                        path: config.json
            """
        }
    }

    environment {
        DOCKER_USER = "jimoh1990"
        // Extracts 'inventory-api-source' from 'GridOps-Platform/inventory-api-source/main'
        REPO_NAME = "${env.JOB_NAME.split('/')[1]}" 
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push') {
            steps {
                container('kaniko') {
                    script {
                        echo "🚀 Building Image: ${DOCKER_USER}/${REPO_NAME}:${IMAGE_TAG}"
                        
                        // Build and Push to Docker Hub
                        sh "/kaniko/executor --context `pwd` --destination ${DOCKER_USER}/${REPO_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('GitOps Update') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-pat', passwordVariable: 'GIT_TOKEN', usernameVariable: 'GIT_USER')]) {
                    script {
                        sh """
                            echo "📝 Updating Helm Values..."
                            
                            # Git Configuration
                            git config user.email "jenkins@sikiru.co.uk"
                            git config user.name "Jenkins Bot"
                            
                            # --- THE FIX IS HERE ---
                            # 1. Update the Repository Name (e.g., jimoh1990/payment-service -> jimoh1990/inventory-api-source)
                            sed -i 's|repository: .*|repository: ${DOCKER_USER}/${REPO_NAME}|' k8s/values.yaml
                            
                            # 2. Update the Image Tag (e.g., v1 -> v5)
                            sed -i 's/tag: .*/tag: "${IMAGE_TAG}"/' k8s/values.yaml
                            
                            # 3. Commit and Push Back
                            git add k8s/values.yaml
                            git commit -m "ci: update image to ${REPO_NAME}:${IMAGE_TAG} [skip ci]"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/JimohAdebayo-DevOps/${REPO_NAME}.git HEAD:main
                        """
                    }
                }
            }
        }
    }
}

