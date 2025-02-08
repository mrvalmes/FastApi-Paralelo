pipeline {
    agent any

    environment {        
        DOCKER_CONFIG = "C:\\Users\\Spectre\\.docker" // Ruta donde se encuentra el archivo config.json
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
            when {
                expression {
                    return env.GIT_BRANCH == 'main' || env.GIT_BRANCH?.endsWith('/main')
                }
            }
            steps {
                // Autenticarse en DOCR con --password-stdin para mayor seguridad
                bat 'echo %DO_API_TOKEN% | docker login registry.digitalocean.com -u doctl --password-stdin'
                
                // Retaggear la imagen desde Nexus a DOCR
                bat 'docker tag mi-repo-docker/mi-app-fastapi:latest registry.digitalocean.com/appparalelo/mi-app-fastapi:latest'
                
                // Hacer push a DOCR
                bat 'docker push registry.digitalocean.com/appparalelo/mi-app-fastapi:latest'
            }
        }    
        
        stage('Desplegar en Digital Ocean') {
            when {
                expression {
                    return env.GIT_BRANCH == 'main' || env.GIT_BRANCH?.endsWith('/main')
                }
            }
            steps {
                bat "doctl apps update %APP_ID% --spec app.yaml"
            }
        }
    }
}
