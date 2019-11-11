FROM python:3.6-stretch

RUN apt-get update
RUN apt-get install libffi-dev libnacl-dev python3-dev -y

COPY Pipfile /
COPY Pipfile.lock /
#COPY profile /

RUN pip install pipenv
RUN pipenv install --system

#ENV DISCORD_TOKEN=mytoken
#ENV DISCORD_ERROR_CHANNEL=mychannel
#ENV DISCORD_DEV_ID=myid
ENV PYTHONPATH=/app

COPY TZMBot/ /app/TZMBot
RUN mkdir -p /app/media
WORKDIR /app/TZMBot

CMD ["python", "app.py"]
