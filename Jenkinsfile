pipeline {
    agent {
        kubernetes {
            yaml '''
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
                  - name: kaniko-secret
                    mountPath: /kaniko/.docker
              volumes:
                - name: kaniko-secret
                  emptyDir: {}
            '''
        }
    }

    environment {
        // Define the image name
        DOCKER_IMAGE = "jimoh1990/${JOB_BASE_NAME}" 
        // Use the Build Number as the unique tag
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push (Kaniko)') {
            steps {
                // Source [1]: Use ephemeral agents (Kaniko) for secure builds
                container('kaniko') {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        script {
                            // 1. Create the Docker Config file dynamically using your credentials
                            sh """
                                echo "{\\"auths\\":{\\"https://index.docker.io/v1/\\":{\\"auth\\":\\"\$(echo -n ${DOCKER_USER}:${DOCKER_PASS} | base64)\\"}}}" > /kaniko/.docker/config.json
                            """
                            
                            // 2. Run the Kaniko Executor (Replaces 'docker build' and 'docker push')
                            sh """
                                /kaniko/executor --context `pwd` --destination ${DOCKER_IMAGE}:${IMAGE_TAG}
                            """
                        }
                    }
                }
            }
        }

        stage('GitOps Update') {
            // Source [2]: Write-Back loop to update Git
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-pat', passwordVariable: 'GIT_TOKEN', usernameVariable: 'GIT_USER')]) {
                    script {
                        sh """
                            # Configure Git
                            git config user.email "jenkins@sikiru.co.uk"
                            git config user.name "Jenkins CI"
                            
                            # Update the tag in values.yaml
                            sed -i 's/tag: .*/tag: "${IMAGE_TAG}"/' charts/python-app/values.yaml
                            
                            # Commit and Push
                            git add charts/python-app/values.yaml
                            git commit -m "ci: update image tag to ${IMAGE_TAG}"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/JimohAdebayo-DevOps/${JOB_BASE_NAME}-source.git HEAD:main
                        """
                    }
                }
            }
        }
    }
}
