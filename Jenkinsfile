pipeline {
   agent any
   stages {
       stage('Github SourceCode Pull') {
           steps {
            
              checkout scm 
           }
       }
      stage('Docker Build') {
           steps {
            bat 'docker-compose build'
           }
       }
      stage('Docker Deploy') {
           steps {
            bat 'docker-compose up -d'
           }
       }
       stage('OWASP ZAP') {
           steps {
            bat './python C:/Users/user/AppData/Local/Programs/Python/Python310/Auth.py'
           }
       }
     
   }
}
