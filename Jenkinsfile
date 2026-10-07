pipeline {

    // ===========================================================
    // JENKINS AGENT
    // ===========================================================
    // Run this pipeline on the available Jenkins executor.
    // ===========================================================
    agent any


    // ===========================================================
    // GLOBAL VARIABLES
    // ===========================================================
    environment {

        // Docker Hub repositories
        BACKEND_IMAGE  = "crawan/quantum-mind-api"
        FRONTEND_IMAGE = "crawan/quantum-mind-client"

        // Every Jenkins build gets a unique version number.
        //
        // Example:
        //   Jenkins build #23
        //
        // produces:
        //   crawan/quantum-mind-api:23
        //   crawan/quantum-mind-client:23
        IMAGE_TAG = "${BUILD_NUMBER}"
    }


    // ===========================================================
    // PIPELINE STAGES
    // ===========================================================
    stages {


        // =======================================================
        // 1. CHECKOUT SOURCE CODE
        // =======================================================
        stage('Checkout Code') {
            steps {

                // Jenkins checks out the Git commit that triggered
                // this build.
                checkout scm
            }
        }


        // =======================================================
        // 2. BUILD BACKEND IMAGE
        // =======================================================
        stage('Build Backend Image') {
            steps {

                // Build the FastAPI backend image.
                //
                // We first create the immutable versioned tag.
                //
                // Example:
                //   crawan/quantum-mind-api:23
                sh """
                    docker build \
                        -t ${BACKEND_IMAGE}:${IMAGE_TAG} \
                        ./backend
                """
            }
        }


        // =======================================================
        // 3. BUILD FRONTEND IMAGE
        // =======================================================
        stage('Build Frontend Image') {
            steps {

                // Build the Angular production image.
                //
                // Example:
                //   crawan/quantum-mind-client:23
                sh """
                    docker build \
                        -t ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                        ./frontend/quantum-mind-ui
                """
            }
        }


        // =======================================================
        // 4. LOGIN TO DOCKER HUB
        // =======================================================
        stage('Login to Docker Hub') {
            steps {

                // Docker Hub credentials are stored in Jenkins
                // Credentials using the ID:
                //
                //   dockerhub-creds
                //
                // The password is never written directly into
                // this Jenkinsfile.
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASS" | \
                        docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin
                    '''
                }
            }
        }


        // =======================================================
        // 5. CREATE LATEST TAGS
        // =======================================================
        stage('Tag Images as Latest') {
            steps {

                // The versioned image already exists locally.
                //
                // Now create the "latest" tag pointing to the
                // exact same image.
                //
                // Example:
                //
                //   quantum-mind-api:23
                //             ↓
                //          latest
                //
                // Both tags point to the same image.
                sh """
                    docker tag \
                        ${BACKEND_IMAGE}:${IMAGE_TAG} \
                        ${BACKEND_IMAGE}:latest

                    docker tag \
                        ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                        ${FRONTEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 6. PUSH BACKEND IMAGE
        // =======================================================
        stage('Push Backend Image') {
            steps {

                // Push BOTH backend tags:
                //
                //   crawan/quantum-mind-api:23
                //   crawan/quantum-mind-api:latest
                sh """
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker push ${BACKEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 7. PUSH FRONTEND IMAGE
        // =======================================================
        stage('Push Frontend Image') {
            steps {

                // Push BOTH frontend tags:
                //
                //   crawan/quantum-mind-client:23
                //   crawan/quantum-mind-client:latest
                sh """
                    docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
                    docker push ${FRONTEND_IMAGE}:latest
                """
            }
        }
    }


    // ===========================================================
    // POST BUILD ACTIONS
    // ===========================================================
    post {

        success {
            echo """
🚀 Quantum Mind images built and pushed successfully.

Backend:
  ${BACKEND_IMAGE}:${IMAGE_TAG}
  ${BACKEND_IMAGE}:latest

Frontend:
  ${FRONTEND_IMAGE}:${IMAGE_TAG}
  ${FRONTEND_IMAGE}:latest

Kubernetes rollout is currently MANUAL.
"""
        }

        failure {
            echo "❌ Quantum Mind image pipeline failed. Check the Jenkins logs."
        }

        always {

            // Remove unused Docker resources from the Jenkins host
            // after the build to prevent the VPS disk from filling up.
            //
            // This does not remove images currently used by containers.
            sh 'docker system prune -af || true'
        }
    }
}