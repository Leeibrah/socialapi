### README.md

FAST API Project built by Python FastAPI Framework

Activate env:
source /Users/Lee/code/python/fastapi/social/venv/bin/activate

Load app using uvicorn:
uvicorn app.main:app --reload

# DOCKER

Build app first:
docker build -t socialapi .

Show docker images:
docker image ls

Start docker image:
docker-compose up -d

Show if image is running:
docker ps -a

Show docker logs:
docker logs social-api-1

Stop docker image:
docker-compose down

Create a repository on hub.docker.com. eg: socialapi
So now we have the repository as: leeibrah/socialapi

Login to docker:
docker login
username and password

Show docker images:
docker image ls

REPOSITORY TAG IMAGE ID CREATED SIZE
social-api latest d759f8a7c0c7 41 hours ago 1.14GB

docker image tag social-api leeibrah/socialapi
