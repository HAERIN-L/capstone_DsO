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
              sh 'python C:/Users/user/Desktop/zap_test/Auth.py'
              
              echo'> 2.Spider ..'
              sh 'python C:/Users/user/Desktop/zap_test/Spider.py'
              
              echo'> 3.VulnerabilityScan ..'
              sh 'python C:/Users/user/Desktop/zap_test/VulnerabilityScan.py'
              
              echo'> 4.Result ..'
              sh 'python C:/Users/user/Desktop/zap_test/Result.py'
              
              echo'> 5.Result Vuln..'
              sh 'python C:/Users/user/Desktop/zap_test/ResultVuln.py'
              
            
           }
       }
     
   }
}
