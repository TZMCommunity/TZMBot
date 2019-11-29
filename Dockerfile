FROM python:buster

RUN apt-get update
RUN apt-get install libffi-dev libnacl-dev python3-dev -y

COPY Pipfile /
#COPY Pipfile.lock /
#COPY profile /

RUN pip install pipenv
RUN pipenv lock --clear
RUN pipenv install
RUN pipenv update
RUN pipenv install
RUN python3 -m pip install discord.py
RUN python3 -m pip install tortoise

#ENV DISCORD_TOKEN=mytoken
#ENV DISCORD_ERROR_CHANNEL=mychannel
#ENV DISCORD_DEV_ID=myid
ENV PYTHONPATH=/app

COPY TZMBot/ /app/TZMBot
RUN mkdir -p /app/media
WORKDIR /app/TZMBot

CMD ["python", "app.py"]
