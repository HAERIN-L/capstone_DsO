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
             bat ' C:/Users/user/AppData/Local/Microsoft/WindowsApps/python3.exe C:/Users/user/AppData/Local/Microsoft/WindowsApps/Python/Python310/Auth.py'
           }
       }

     
      
   }
}
