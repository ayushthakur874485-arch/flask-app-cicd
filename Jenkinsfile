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
                    bat '''
                        @echo off
                        setlocal enabledelayedexpansion
                        
                        set "keyPath=%SSH_KEY_FILE%"
                        set "server=%EC2_USER%@%EC2_IP%"
                        set "appDir=%APP_DIR%"
                        
                        icacls "!keyPath!" /inheritance:r /grant:r "SYSTEM:(F)"
                        ssh -i "!keyPath!" -o StrictHostKeyChecking=no "!server!" "mkdir -p !appDir!"
                        scp -i "!keyPath!" -o StrictHostKeyChecking=no -r "." "!server!:!appDir!/"
                    '''
                }
            }
        }
        
        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying on EC2..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-credentials', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    bat '''
                        @echo off
                        setlocal enabledelayedexpansion
                        
                        set "keyPath=%SSH_KEY_FILE%"
                        set "server=%EC2_USER%@%EC2_IP%"
                        set "appDir=%APP_DIR%"
                        
                        icacls "!keyPath!" /inheritance:r /grant:r "SYSTEM:(F)"
                        ssh -i "!keyPath!" -o StrictHostKeyChecking=no "!server!" ^
                            "cd !appDir! && docker compose down || true && sleep 3 && docker compose up -d --build && sleep 10"
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo "✅ Verifying deployment..."
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-credentials', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER')]) {
                    bat '''
                        @echo off
                        setlocal enabledelayedexpansion
                        
                        set "keyPath=%SSH_KEY_FILE%"
                        set "server=%EC2_USER%@%EC2_IP%"
                        set "appDir=%APP_DIR%"
                        
                        icacls "!keyPath!" /inheritance:r /grant:r "SYSTEM:(F)"
                        ssh -i "!keyPath!" -o StrictHostKeyChecking=no "!server!" ^
                            "docker ps && echo. && cd !appDir! && docker compose logs --tail 20"
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