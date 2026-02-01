# SecureProxyLite Telegram Bot

This is a simple Telegram bot that answers user questions based on a predefined JSON file.

## Build Docker Image

```bash
docker build -t teamkempa/secureproxybot:1.0 .
```
---> input after -t is TAG

## Verify the Docker Images created
```bash
docker images
```

## Login to Docker Hub
```bash
docker login
```
username : teamkempa 
password : Cupidlove4 

## Push Docker Image
```bash
docker push teamkempa/secureproxybot:1.0
```
---> use tag to identify the docker image

## SSH into host/server
```bash
ssh root@192.34.61.160
```
list the Docker process, stop the running Docker if you want, if any.

## Run/Deploy docker

```bash
docker run --env-file .env teamkempa/secureproxybot:1.0 &
```

### Optional: Enable Live Updates
If you want to edit `qna.json` or `flow.json` without rebuilding the image, use volume mapping:
```bash
docker run --env-file .env -v $(pwd)/qna.json:/app/qna.json -v $(pwd)/flow.json:/app/flow.json teamkempa/secureproxybot:1.0 &
```

### parameters

--env-file : loads variables from .env file
-v : volume mapping (optional: needed only if you want to edit json files on the server)
&  : at the end is to run the docker in the background

## Managing Content

Edit `qna.json` or `flow.json` to change the behavior.
Since they are mapped as volumes, changes usually require just a restart or sometimes take effect immediately depending on implementation.
