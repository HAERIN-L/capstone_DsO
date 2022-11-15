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
      stage('Testing') {
           steps {
            echo '> 2. Spider ..'
             bat 'python C:/ProgramData/Jenkins/.jenkins/workspace/local_test/Python/Python310'
           }
       }
      
      
      
   }
}
