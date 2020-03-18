pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:latest'
                }
            }
            steps {
                sh 'wget -N https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz -P ~/'
                sh 'tar -C ~/ -zxvf ~/geckodriver-v0.25.0-linux64.tar.gz'
                sh 'rm ~/geckodriver-v0.25.0-linux64.tar.gz'
                sh 'sudo mv -f ~/geckodriver /usr/local/share/'
                sh 'sudo chmod +x /usr/local/share/geckodriver'
                sh 'sudo ln -s /usr/local/share/geckodriver /usr/local/bin/geckodriver'
                sh 'python src/process_html.py'
                sh 'python src/web_driver.py'
                sh 'python src/build_test.py'
                sh 'python src/guiUtils.py'
            }
        }
    }
}
