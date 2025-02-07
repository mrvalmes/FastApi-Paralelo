pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "localhost:8083" // URL de Nexus
        DOCKER_IMAGE = "mi-repo-docker/mi-app-fastapi"
        NEXUS_CREDENTIALS = credentials('NEXUS_CREDENTIALS')
        DO_API_TOKEN = credentials('DO_API_TOKEN') 
		APP_ID = credentials('DO_APP_ID')		
	
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                git branch: 'feature/nueva-funcionalidad', credentialsId: 'GIT_CREDENTIALS', url: 'git@github.com:mrvalmes/FastApi-Paralelo.git'
            }
        }
        
        stage('Construir Imagen Docker') {
            when { not { branch 'main' } }
            steps {
                bat 'docker build -t %DOCKER_IMAGE%:latest .' 
            }
        }

        stage('Subir Imagen a Nexus') {
            when { not { branch 'main' } }
            steps {
                bat """
                echo %NEXUS_CREDENTIALS_PSW% | docker login -u %NEXUS_CREDENTIALS_USR% --password-stdin %DOCKER_REGISTRY%
                docker tag %DOCKER_IMAGE%:latest %DOCKER_REGISTRY%/%DOCKER_IMAGE%:latest
                docker push %DOCKER_REGISTRY%/%DOCKER_IMAGE%:latest
                """
        }
    }
        stage('Subir Imagen a DOCR') {
            when { branch 'main' }
        steps {
            // Autenticarse en DOCR (si aún no lo has hecho)
            bat 'doctl registry login'
            
            // Retaggear la imagen desde Nexus a DOCR
            bat 'docker tag mi-repo-docker/mi-app-fastapi:latest registry.digitalocean.com/appparalelo/mi-app-fastapi:latest'
            
            // Hacer push a DOCR
            bat 'docker push registry.digitalocean.com/appparalelo/mi-app-fastapi:latest'
        }
    }
        stage('Desplegar en DigitalOcean') {
            steps {
                script {
                    def response = sh(script: 'doctl apps update $APP_ID --spec .do/app.yaml', returnStdout: true).trim()
                    echo "Respuesta de la actualización de la aplicación: ${response}"
                }
            }
        }
    }
}
