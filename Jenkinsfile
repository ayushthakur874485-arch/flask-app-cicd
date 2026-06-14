pipeline {
    agent any
    
    environment {
        EC2_IP = 'ec2-65-0-71-207.ap-south-1.compute.amazonaws.com'
        EC2_USER = 'ubuntu'
        APP_DIR = '/home/ubuntu/flask-app'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo "🔄 Cloning repository..."
                deleteDir()
                git branch: 'main', url: 'https://github.com/ayushthakur874485-arch/flask-app-cicd.git'
            }
        }
        
        stage('Copy Files to EC2') {
            steps {
                echo "📤 Copying files to EC2..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-credentials', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    powershell '''
                        $keyPath = $env:SSH_KEY_FILE
                        $server = "${env:EC2_USER}@${env:EC2_IP}"
                        $appDir = $env:APP_DIR
                        
                        # Fix key permissions
                        icacls "$keyPath" /inheritance:r /grant:r "$($env:USERNAME):(F)" | Out-Null
                        
                        # Create directory on EC2
                        ssh -i "$keyPath" -o StrictHostKeyChecking=no "$server" "mkdir -p $appDir"
                        
                        # Copy files to EC2
                        scp -i "$keyPath" -o StrictHostKeyChecking=no -r "." "${server}:${appDir}/"
                    '''
                }
            }
        }
        
        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying on EC2..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-credentials', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    powershell '''
                        $keyPath = $env:SSH_KEY_FILE
                        $server = "${env:EC2_USER}@${env:EC2_IP}"
                        $appDir = $env:APP_DIR
                        
                        # Deploy
                        ssh -i "$keyPath" -o StrictHostKeyChecking=no "$server" @"
                        cd $appDir
                        docker compose down || true
                        sleep 3
                        docker compose up -d --build
                        sleep 10
"@
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo "✅ Verifying deployment..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-credentials', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    powershell '''
                        $keyPath = $env:SSH_KEY_FILE
                        $server = "${env:EC2_USER}@${env:EC2_IP}"
                        $appDir = $env:APP_DIR
                        
                        ssh -i "$keyPath" -o StrictHostKeyChecking=no "$server" @"
                        echo "--- Running Containers ---"
                        docker ps
                        echo ""
                        echo "--- Docker Compose Logs ---"
                        cd $appDir
                        docker compose logs --tail 20
"@
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