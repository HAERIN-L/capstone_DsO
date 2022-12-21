pipeline {
   agent any
   options {
      skipDefaultCheckout(true)
   }
   stages {
      stage('Start') {
            agent any
            steps {
                slackSend (channel: '#capstone_project', color: '#FFFF00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
            }
        }
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
   post {
        success {
            slackSend (channel: '#capstone_project', color: '#00FF00', message: "빌드 성공: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
        failure {
            slackSend (channel: '#capstone_project', color: '#FF0000', message: "빌드 실패: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}
