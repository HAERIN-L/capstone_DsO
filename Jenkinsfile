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
            sh 'docker-compose build'
           }
       }
      stage('Docker Deploy') {
           steps {
            sh 'docker-compose up -d'
           }
       }
      stage('Testing') {
           steps {
            echo '> 2. Spider ..'
             sh 'sudo C:\Users\user\Desktop\owasp\Spider.py'
           }
       }
      
      
      
   }
}
