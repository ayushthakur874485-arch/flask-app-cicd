pipeline {
    agent any
    
    environment {
        GITHUB_REPO = 'YOUR_USERNAME/YOUR_REPO'  // Change this to your repo
        APP_NAME = 'flask-app'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo "🔄 Cloning repository..."
                deleteDir()
                git branch: 'main', url: 'https://github.com/${GITHUB_REPO}.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "🏗️  Building Docker image..."
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:latest'
                sh 'docker images'
            }
        }
        
        stage('Stop Old Containers') {
            steps {
                echo "🛑 Stopping old containers..."
                sh '''
                    docker compose down || true
                    sleep 5
                '''
            }
        }
        
        stage('Deploy with Docker Compose') {
            steps {
                echo "🚀 Deploying application..."
                sh 'docker compose up -d --build'
                sh 'sleep 10'
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo "✅ Verifying deployment..."
                sh 'docker ps'
                sh 'docker compose logs'
            }
        }
    }
    
    post {
        always {
            echo "Pipeline execution completed"
        }
        success {
            echo "✅ Deployment successful! Access your app at http://<EC2-IP>:5000"
        }
        failure {
            echo "❌ Deployment failed! Check logs above"
            sh 'docker compose logs || true'
        }
    }
}
