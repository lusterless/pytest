pipeline {
    agent {dockerfile true}
    environment {
        // CI set to true to allow it to run in "non-watch" (i.e. non-interactive) mode
        CI = 'true'
//         HOST_IP = "${HOST_IP}".0
//         HOST_PORT = "${HOST_PORT}"
    }
    stages {
        stage('Build') { 
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
                    agent {
                        docker { 
                            image 'theimg:latest' 
                            args '--name apptest --network testing'
                        }
                    }
                    steps {
                        sh 'nohup flask run & sleep 1'
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
                    }
                }
                stage('Headless Browser Test') {
                    agent {
                        docker { 
                            image 'image 'python:3.7.2'
                            args '--name uitest --network testing'
                        }
                    }
                    steps {
                        sh """
                        pip install pytest
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
                        pytest -s -rA --junitxml=test-report.xml
                        """
                    }
                    post {
                        always {
                            junit testResults: 'test-report.xml'
                        }
                    }
                }
            }
        }

        /* Warnings X08 is not well done, pls refer to notes for doc
        it is too dynamic
        */ 
        // stage('warnings') {
            
        //     agent {
        //         docker { image 'theimg:latest' }
        //     }
        //     steps {
        //         sh 'nohup flask run & sleep 1'
        //         sh 'pytest -s -rA --junitxml=warn-report.xml'
        //         echo "hello"

        //     }
        //     post {
        //         always {
                    
        //             // recordIssues enabledForFailure: true, tools: [mavenConsole(), java(), javaDoc()]
                
        //             recordIssues enabledForFailure: true, tool: codeAnalysis()	
        //             recordIssues enabledForFailure: true, tool: codeChecker()
        //             recordIssues enabledForFailure: true, tool: dockerLint()
        //         }
        //     }
        // }

        /* X09 SonarQube */ 
        stage('SonarQube') {
            agent {
                docker { image 'theimg:latest' }
            }
            steps {
                script {
                    def scannerHome = tool 'SonarQube';
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=test -Dsonar.sources=."
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
