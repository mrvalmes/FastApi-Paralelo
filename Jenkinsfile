pipeline {
    agent any

    environment {
        DO_API_TOKEN = credentials('DO_API_TOKEN') // Token con scopes registry:read,registry:write
        APP_ID = credentials('DO_APP_ID')
        DO_REGISTRY = "registry.digitalocean.com/appparalelo" //registro DOCR
        DOCKER_IMAGE = "mi-repo-docker/mi-app-fastapi"
        NEXUS_REGISTRY = "localhost:8083" // URL de tu registro Nexus
        NEXUS_CREDENTIALS = credentials('NEXUS_CREDENTIALS') // Credenciales para Nexus
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
                bat "docker build -t ${DOCKER_IMAGE}:latest ." // Construye la imagen sin etiqueta de registro
            }
        }

        stage('Subir Imagen a Nexus') {
            when { not { branch 'main' } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'NEXUS_CREDENTIALS', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    bat "docker login ${NEXUS_REGISTRY} -u ${NEXUS_USERNAME} -p ${NEXUS_PASSWORD}"
                    bat "docker tag ${DOCKER_IMAGE}:latest ${NEXUS_REGISTRY}/${DOCKER_IMAGE}:latest" // Etiqueta para Nexus
                    bat "docker push ${NEXUS_REGISTRY}/${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Transferir Imagen a DOCR') {
        when { not { branch 'main' } }
        steps {
            withCredentials([usernamePassword(credentialsId: 'DO_REGISTRY_CREDENTIALS', usernameVariable: 'DO_USERNAME', passwordVariable: 'DO_PASSWORD')]) {
                sh """ // Usamos 'sh' para evitar la interpolación de Groovy
                    docker login registry.digitalocean.com -u "\$DO_USERNAME" -p "\$DO_PASSWORD" // Escapamos las variables
                    docker pull ${NEXUS_REGISTRY}/${DOCKER_IMAGE}:latest
                    docker tag ${NEXUS_REGISTRY}/${DOCKER_IMAGE}:latest ${DO_REGISTRY}/${DOCKER_IMAGE}:latest
                    docker push ${DO_REGISTRY}/${DOCKER_IMAGE}:latest
                """
            }
        }
    }

        stage('Desplegar en Digital Ocean') {
            when {
                expression {
                    return env.GIT_BRANCH == 'main' || env.GIT_BRANCH?.endsWith('/main')
                }
            }
            steps {
                bat "doctl auth init --access-token %DO_API_TOKEN%"
                bat "doctl apps update %APP_ID% --spec app.yaml"
            }
        }
    }
}