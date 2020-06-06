docker build -t tzmbot:0.0.1 .
docker stop tzmbot
docker rm tzmbot
docker run -d --name tzmbot --env-file=/home/juuso/git/TZMBot/env_file -v /home/juuso/git/TZMBot/media:/app/media tzmbot:0.0.1
docker logs -f tzmbot
