FROM python:3.6.2

ENV HTTP_PROXY=http://proxy-rie.http.insee.fr:8080/
ENV HTTPS_PROXY=http://proxy-rie.http.insee.fr:8080/

RUN mkdir -p /home/project/dash_app
WORKDIR /home/project/dash_app
COPY requirements.txt /home/project/dash_app
RUN pip install --proxy=$HTTP_PROXY --no-cache-dir -r requirements.txt

COPY . /home/project/dash_app