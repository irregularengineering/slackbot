FROM python:3.6
ENV PROJECT_DIR=/opt/slackbot \
    TERM=XTERM
RUN apt-get update && apt-get -y install mysql-client vim
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
ADD ./requirements.txt $PROJECT_DIR/requirements.txt
RUN pip3 install -r $PROJECT_DIR/requirements.txt
ADD . $PROJECT_DIR
