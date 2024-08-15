def getGitBranchName() { 
                return scm.branches[0].name 
            }
def branchName
def targetBranch

pipeline{
    agent any

    environment {
         DOCKERHUB_USERNAME = "hamdiiala"
       DEV_TAG = "${DOCKERHUB_USERNAME}/courzelo:v1.1.3-dev"
       STAGING_TAG = "${DOCKERHUB_USERNAME}/courzelo:v1.0.0-staging"
       PROD_TAG = "${DOCKERHUB_USERNAME}/courzelo:v1.0.0-prod"

     
  }
     parameters {
       string(name: 'BRANCH_NAME', defaultValue: "${scm.branches[0].name}", description: 'Git branch name')
       string(name: 'CHANGE_ID', defaultValue: '', description: 'Git change ID for merge requests')
       string(name: 'CHANGE_TARGET', defaultValue: '', description: 'Git change ID for the target merge requests')
  }
    stages{

      stage('branch name') {
      steps {
        script {
          branchName = params.BRANCH_NAME
          echo "Current branch name: ${branchName}"
        }
      }
    }

    stage('target branch') {
      steps {
        script {
          targetBranch = branchName
          echo "Target branch name: ${targetBranch}"
        }
      }
    }
        stage('Git Checkout'){
            steps{
                git branch: 'main', credentialsId: 'AlaGitH', url: 'https://github.com/Alaahamdii/Courzelo_MLOps.git'
	    }
        }
        

        stage('Install Dependencies') {
            steps {
                // Install required Python packages
                sh 'pip3 install -r requirements.txt'
            }
        }
           
         stage('Run Script') {
            steps {
                // Run the converted Python script and capture the output
                sh 'python3 train.py > output.log'
            }
        }
        

        
        stage('Publish HTML Report') {
            steps {
                publishHTML([allowMissing: false,
                             alwaysLinkToLastBuild: true,
                             keepAll: true,
                             reportDir: '.',
                             reportFiles: 'output.html',
                             reportName: 'HTML Report',
                             reportTitles: 'Resident Matching Tawasalna'])
            }
        }
    }
}
    