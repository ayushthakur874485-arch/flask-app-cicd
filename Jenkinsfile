pipeline {
    agent any
    
    environment {
        GITHUB_REPO = 'ayushthakur874485-arch/flask-app-cicd'
        EC2_IP = 'ec2-65-0-71-207.ap-south-1.compute.amazonaws.com'
        EC2_USER = 'ubuntu'
        APP_DIR = '/home/ubuntu/flask-app'
        SSH_KEY = 'ec2-ssh-credentials'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo "🔄 Cloning repository..."
                deleteDir()
                git branch: 'main', url: 'https://github.com/${GITHUB_REPO}.git'
            }
        }
        
        stage('Copy Files to EC2') {
            steps {
                echo "📤 Copying files to EC2..."
                withCredentials([sshUserPrivateKey(credentialsId: "${SSH_KEY}", keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    sh '''
                        ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no ${SSH_USER}@${EC2_IP} "mkdir -p ${APP_DIR}"
                        scp -i $SSH_KEY_FILE -o StrictHostKeyChecking=no -r . ${SSH_USER}@${EC2_IP}:${APP_DIR}/
                    '''
                }
            }
        }
        
        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying on EC2..."
                withCredentials([sshUserPrivateKey(credentialsId: "${SSH_KEY}", keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    sh '''
                        ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no ${SSH_USER}@${EC2_IP} "
                            cd ${APP_DIR}
                            docker compose down || true
                            sleep 3
                            docker compose up -d --build
                            sleep 10
                        "
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo "✅ Verifying deployment..."
                withCredentials([sshUserPrivateKey(credentialsId: "${SSH_KEY}", keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    sh '''
                        ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no ${SSH_USER}@${EC2_IP} "
                            echo '--- Running Containers ---'
                            docker ps
                            echo ''
                            echo '--- Docker Compose Logs ---'
                            cd ${APP_DIR}
                            docker compose logs --tail 20
                        "
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Deployment successful!"
            echo "Access your app at: http://${EC2_IP}:5000"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
