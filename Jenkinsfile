pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "localhost:8081/repository/mi-repo-docker/" // URL de Nexus
        DOCKER_IMAGE = "mi-repo-docker/mi-app-fastapi"
        NEXUS_USER = credentials('NEXUS_CREDENTIALS')
        NEXUS_PASS = credentials('NEXUS_CREDENTIALS')
        DO_API_TOKEN = credentials('DO_API_TOKEN')        
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                git branch: 'feature/nueva-funcionalidad', credentialsId: 'GIT_CREDENTIALS', url: 'git@github.com:mrvalmes/FastApi-Paralelo.git'
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
                echo $NEXUS_PASS | docker login $DOCKER_REGISTRY -u $NEXUS_USER --password-stdin
                docker tag $DOCKER_IMAGE:latest $DOCKER_REGISTRY/mi-app-fastapi:latest
                docker push $DOCKER_REGISTRY/mi-app-fastapi:latest
                """
            }
        }

        stage('Desplegar en Digital Ocean') {
            when {
                branch 'main'
            }
            steps {
                sh "/var/jenkins_home/bin/doctl auth init --access-token $DO_API_TOKEN"
                sh "/var/jenkins_home/bin/doctl apps update ${APP_ID} --spec \$(pwd)/app.yaml"
            }
        }
    }
}
