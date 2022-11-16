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
            bat '"C:/Program Files/Docker/Docker/resources/bin/docker-compose" up -d'
           }
       }
     

     
      
   }
}
