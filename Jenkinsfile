pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "https://bookstore-insured-fashion-can.trycloudflare.com"  // URL del Nexus
        DOCKER_IMAGE = "mi-repo-docker/mi-app-fastapi"
        NEXUS_USER = credentials('NEXUS_CREDENTIALS')
        NEXUS_PASS = credentials('NEXUS_CREDENTIALS')
        DO_API_TOKEN = credentials('DO_API_TOKEN')
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                git branch: 'feature/nueva-funcionalidad', credentialsId: 'GIT_CREDENTIALS', url: 'git@github.com:tu-usuario/tu-repo.git'
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                sh 'pytest tests/'  // Ejecuta pruebas en la app
            }
        }

        stage('Construir Imagen Docker') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t $DOCKER_IMAGE:latest .'
            }
        }

        stage('Subir Imagen a Nexus') {
            when {
                branch 'main'
            }
            steps {
                sh """
                docker login -u $NEXUS_USER -p $NEXUS_PASS $DOCKER_REGISTRY
                docker tag $DOCKER_IMAGE:latest $DOCKER_REGISTRY/$DOCKER_IMAGE:latest
                docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:latest
                """
            }
        }

        stage('Desplegar en Digital Ocean') {
            when {
                branch 'main'
            }
            steps {
                sh "/var/jenkins_home/bin/doctl apps update $APP_ID --spec app.yaml"
            }
        }
    }
}
