def ListHtml() {
    return findFiles(glob: '**/html/*.html')
}

def PublishHtml() {
    for (f in  ListHtml()) {
        if (! f.directory) {
            echo """Publishing ${f.name} ${f.path} ${f.directory} ${f.length} ${f.lastModified}"""
            REPORT_DIR = sh(script: 'dirname ' + f.path, returnStdout: true)
            REPORT_NAME = sh(script: 'basename ' + f.path + ' .html', returnStdout: true)
            publishHTML (target : [allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: REPORT_DIR,
                reportFiles: f.name,
                reportName: REPORT_NAME,
                reportTitles: REPORT_NAME])
        }
    }
}

pipeline {
    agent any

    environment {
        GITHUB_REG_CRED_ID = 'GitHubRegistry'
        GITHUB_REPO = 'https://github.com/houdini91/jenkins_stock.git'
    }
    
    parameters {
        gitParameter name: 'BRANCH_NAME',
           branchFilter: 'origin/(.*)',
           selectedValue: 'NONE',
           defaultValue: 'master',
           type: 'PT_BRANCH'

     }
    
    stages {
        stage('Checkout') {
            steps {
                echo "CHECKOUT BRANCH_TAG: ${BRANCH_NAME}"
                checkout([$class: 'GitSCM',
                          branches: [[name: "${BRANCH_NAME}"]],
                          extensions: [],
                          gitTool: 'Default',
                          submoduleCfg: [],
                          userRemoteConfigs: [[ credentialsId: "${GITHUB_REG_CRED_ID}", url: "${GITHUB_REPO}"]]
                        ])
            }
        }
        stage('Build py_trans_jenkins') {
            steps{
                script {
                     sh 'make build_python'
                }
            }
        }
        stage('Build analysis image') {
            steps{
                script {
                    dockerImage = docker.build "houdini91/jenkins_stock/stock_analyzer"
                }
            }
        }
        stage('Clean') {
            steps {
                script {
                    sh 'make clean'
                }
            }
        }
        stage('Simple') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python -m "trans_jenkins.examples.simple"'
                    }
                }
            }
            post{
                always{
                    script {
                        PublishHtml()
                    }
                }
            }
         }
    }
}