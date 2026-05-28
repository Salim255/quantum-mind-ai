pipeline {

    // ===========================================================
    // AGENT
    // ===========================================================
    // WHY:
    // "any" allows Jenkins to run on any available executor node.
    // Good for simple VPS or single Jenkins setups.
    // ===========================================================
    agent any


    // ===========================================================
    // TOOLS (OPTIONAL)
    // ===========================================================
    // Only needed if you build frontend inside Jenkins.
    // Keep NodeJS tool for Angular builds if required.
    // ===========================================================
    tools {
        nodejs "NODE20.19"
    }


    // ===========================================================
    // GLOBAL VARIABLES
    // ===========================================================
    environment {

        // -------------------------------------------------------
        // DOCKER IMAGES (YOUR PROJECT)
        // -------------------------------------------------------
        BACKEND_IMAGE = "crawan/quantum-mind-api"
        FRONTEND_IMAGE = "crawan/quantum-mind-client"

        // -------------------------------------------------------
        // VERSIONING STRATEGY
        // -------------------------------------------------------
        // WHY:
        // - Each build gets a unique tag
        // - Enables rollback to older versions
        // -------------------------------------------------------
        IMAGE_TAG = "${BUILD_NUMBER}"
    }


    // ===========================================================
    // PIPELINE STAGES
    // ===========================================================
    stages {


        // =======================================================
        // 1. GET SOURCE CODE
        // =======================================================
        stage('Checkout Code') {
            steps {
                // Pull latest code from Git repository
                checkout scm
            }
        }


        // =======================================================
        // 2. BUILD BACKEND (FASTAPI DOCKER IMAGE)
        // =======================================================
        stage('Build Backend Image') {
            steps {

                // WHY:
                // We package FastAPI into a Docker image
                // so it runs consistently anywhere
                sh """
                    docker build -t ${BACKEND_IMAGE}:${IMAGE_TAG} ./backend
                    docker tag ${BACKEND_IMAGE}:${IMAGE_TAG} ${BACKEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 3. BUILD FRONTEND (ANGULAR DOCKER IMAGE)
        // =======================================================
        stage('Build Frontend Image') {
            steps {

                // WHY:
                // Angular app is compiled and served via Nginx container
                sh """
                    docker build -t ${FRONTEND_IMAGE}:${IMAGE_TAG} ./frontend/quantum-mind-ui
                    docker tag ${FRONTEND_IMAGE}:${IMAGE_TAG} ${FRONTEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 4. LOGIN TO DOCKER HUB
        // =======================================================
        stage('Login to Docker Hub') {
            steps {

                // WHY:
                // Required before pushing images to Docker Hub registry
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }


        // =======================================================
        // 5. PUSH BACKEND IMAGE
        // =======================================================
        stage('Push Backend Image') {
            steps {

                // WHY:
                // Makes backend available for deployment servers
                sh """
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker push ${BACKEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 6. PUSH FRONTEND IMAGE
        // =======================================================
        stage('Push Frontend Image') {
            steps {

                // WHY:
                // Frontend image is also pushed for deployment
                sh """
                    docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
                    docker push ${FRONTEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 7. OPTIONAL DEPLOY STEP (COMMENTED)
        // =======================================================
        stage("ROLLOUT APP") {
            steps {
                script {
                    // Start new containers in detached mode
                    // sh 'docker-compose up -d'

                    withCredentials([file(credentialsId: 'QUANTUM_API_SECRETS_FILE', variable: 'SECRETS_FILE')]) {
                        sh '''
                            # Copy the secret file into the workspace
                            cat "$SECRETS_FILE" > .env
                            
                            # Instead of rebuilding locally, we PULL from Docker Hub
                            docker-compose pull

                            # Run docker-compose (it will load .env)
                            docker-compose up -d
                        '''
                    }
                }
            }
        }
    }


    // ===========================================================
    // POST EXECUTION ACTIONS
    // ===========================================================
    post {

        // -------------------------------------------------------
        // SUCCESS
        // -------------------------------------------------------
        success {
            echo "🚀 Quantum Mind pipeline completed successfully"
        }

        // -------------------------------------------------------
        // FAILURE
        // -------------------------------------------------------
        failure {
            echo "❌ Pipeline failed — check logs"
        }

        // -------------------------------------------------------
        // ALWAYS RUN
        // -------------------------------------------------------
        always {
            echo "🧹 Cleaning Docker system"

            // WHY:
            // Removes unused images/containers to free disk space
            sh "docker system prune -af || true"
        }
    }
}