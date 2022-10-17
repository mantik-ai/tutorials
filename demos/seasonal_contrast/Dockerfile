FROM python:3.8

RUN apt-get update

##RUN yes | apt install python3-venv
RUN yes | apt install python3-pip

COPY . . 
 
RUN pip install -r ./requirements.txt

RUN pip install mantik==0.1.1
