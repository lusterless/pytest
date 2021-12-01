pipeline {
    agent any
    environment {
        // CI set to true to allow it to run in "non-watch" (i.e. non-interactive) mode
        CI = 'true'
//         HOST_IP = "${HOST_IP}".0
//         HOST_PORT = "${HOST_PORT}"
    }
    stages {
        stage('Build') { 
	    agent {
	    	docker {
			image 'python:3.7.2' 
		}
	    }
	    steps {
                script {
                    try { sh 'yes | docker image prune' }
                    catch (Exception e) { echo "no dangling images deleted" }
                    try { sh 'yes | docker image prune -a' }
                    catch (Exception e) { echo "no images w containers deleted" }
                    try { sh 'yes | docker container prune' }
                    catch (Exception e) { echo "no unused containers deleted" }
                }
                // ensure latest image is being build
                sh 'docker build -t theimg:latest .'
            }
        }
        /* Selenium portion */
        stage('unit/sel test') {
            parallel {
                stage('Deploy') {
                    agent any
                    steps {
			sh 'docker run -d -p 5000:5000 --name apptest --network testing theimg:latest'
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
			sh 'docker container stop apptest'
                    }
                }
                stage('Headless Browser Test') {
                    agent {
			docker {
				image 'theimg:latest'
				args '--name uitest --network testing'
			}
		    }
                    steps {
                        sh 'pytest -rA --junitxml=logs/uireport.xml'	
                    }
		    post {
			always {
				junit testResults: 'logs/uireport.xml'
				recordIssues enabledForFailure: true, tools: [mavenConsole(), java(), javaDoc()]
              
                    		recordIssues enabledForFailure: true, tool: codeAnalysis()	
                     		recordIssues enabledForFailure: true, tool: codeChecker()
                     		recordIssues enabledForFailure: true, tool: dockerLint()
			}
		    }
                }
            }
        }
        /* X09 SonarQube */ 
        stage('SonarQube') {
            agent {
                docker { image 'theimg:latest' }
            }
            steps {
                script {
                    def scannerHome = tool 'SonarQube';
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=project:test -Dsonar.sources=."
                    }
                }
            }
            post {
                always {
                    recordIssues enabledForFailure: true, tool: sonarQube()	
                }
            }
        }
    }
}
