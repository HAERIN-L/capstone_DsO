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
       stage('OWASP ZAP') {
           steps {
              echo'> 1.Authentication Set..'
              sh 'python /var/lib/jenkins/workspace/capstone/Auth.py'
              
             
           }
       }

   }
}
