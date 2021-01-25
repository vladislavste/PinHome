FROM python:3.8
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['app.py']
