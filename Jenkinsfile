pipeline {

    // ===========================================================
    // JENKINS AGENT
    // ===========================================================
    agent any


    // ===========================================================
    // GLOBAL VARIABLES
    // ===========================================================
    environment {

        // Docker Hub repositories
        BACKEND_IMAGE  = "crawan/quantum-mind-api"
        FRONTEND_IMAGE = "crawan/quantum-mind-client"

        // Unique image version for this Jenkins build
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
                checkout scm
            }
        }


        // =======================================================
        // 2. BUILD BACKEND IMAGE
        // =======================================================
        stage('Build Backend Image') {

            // Only run this stage when backend files changed.
            when {
                changeset "backend/**"
            }

            steps {
                echo "Backend changes detected. Building backend image..."

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

            // Only run this stage when frontend files changed.
            when {
                changeset "frontend/quantum-mind-ui/**"
            }

            steps {
                echo "Frontend changes detected. Building frontend image..."

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

            // Login only when at least one application changed.
            when {
                anyOf {
                    changeset "backend/**"
                    changeset "frontend/quantum-mind-ui/**"
                }
            }

            steps {
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
        // 5. TAG BACKEND AS LATEST
        // =======================================================
        stage('Tag Backend Latest') {

            when {
                changeset "backend/**"
            }

            steps {
                sh """
                    docker tag \
                        ${BACKEND_IMAGE}:${IMAGE_TAG} \
                        ${BACKEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 6. TAG FRONTEND AS LATEST
        // =======================================================
        stage('Tag Frontend Latest') {

            when {
                changeset "frontend/quantum-mind-ui/**"
            }

            steps {
                sh """
                    docker tag \
                        ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                        ${FRONTEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 7. PUSH BACKEND
        // =======================================================
        stage('Push Backend Image') {

            when {
                changeset "backend/**"
            }

            steps {
                sh """
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker push ${BACKEND_IMAGE}:latest
                """
            }
        }


        // =======================================================
        // 8. PUSH FRONTEND
        // =======================================================
        stage('Push Frontend Image') {

            when {
                changeset "frontend/quantum-mind-ui/**"
            }

            steps {
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
            🚀 Quantum Mind image pipeline completed successfully.

            Build:
                #${BUILD_NUMBER}

            Only images corresponding to changed application code were built
            and pushed.

            Kubernetes rollout remains MANUAL.
            """
        }

        failure {
            echo "❌ Quantum Mind image pipeline failed. Check the Jenkins logs."
        }

        always {

            // Remove unused Docker resources so the VPS does not
            // continuously accumulate build layers and stopped data.
            sh 'docker system prune -af || true'
        }
    }
}