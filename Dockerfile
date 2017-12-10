FROM ubuntu:latest
MAINTAINER Johann Wolf "johann.georg.wolf@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP app.py
ENTRYPOINT ["python"]
CMD [ "-m", "flask", "run", "--host=0.0.0.0" ]
