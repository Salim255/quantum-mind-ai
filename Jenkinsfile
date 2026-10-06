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

        // Every Jenkins build gets a unique image tag.
        // Example:
        //   Build #42
        //   crawan/quantum-mind-api:42
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

                // Build the FastAPI Docker image.
                //
                // The resulting image is tagged with the Jenkins
                // build number so every build is uniquely identifiable.
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
                // Again, use the Jenkins build number rather than
                // relying on the mutable "latest" tag.
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

                // Docker Hub credentials are stored securely
                // inside Jenkins Credentials.
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
        // 5. PUSH BACKEND IMAGE
        // =======================================================
        stage('Push Backend Image') {
            steps {

                // Push only the immutable Jenkins build tag.
                //
                // Example:
                // crawan/quantum-mind-api:42
                sh """
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                """
            }
        }


        // =======================================================
        // 6. PUSH FRONTEND IMAGE
        // =======================================================
        stage('Push Frontend Image') {
            steps {

                // Push only the immutable Jenkins build tag.
                //
                // Example:
                // crawan/quantum-mind-client:42
                sh """
                    docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
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

            Frontend:
              ${FRONTEND_IMAGE}:${IMAGE_TAG}

            Kubernetes rollout is currently MANUAL.
            """
        }

        failure {
            echo "❌ Quantum Mind image pipeline failed. Check the Jenkins logs."
        }

        always {
            // Remove unused Docker resources from the Jenkins host
            // after the build to avoid filling the VPS disk.
            sh 'docker system prune -af || true'
        }
    }
}