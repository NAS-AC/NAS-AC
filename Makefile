include .env

all: build run

build:
	@docker build -t courinha/nas-ac:latest .

run:
	@docker run -v ./data:/data courinha/nas-ac:latest

cleani:
	@docker images | awk '$$1 == "courinha/nas-ac" {print $$3}' | xargs docker rmi -f

garbagecollector:
	@docker images | awk '$$1 == "<none>" {print $$3}' | xargs docker rmi -f

ls:
	@docker image ls | grep "courinha/nas-ac"

publish:
	@docker build -t courinha/nas-ac:latest .
	@docker build -t ghcr.io/courinha768/nas-ac/nas-ac:latest .
	@docker push courinha/nas-ac:latest
	@docker push ghcr.io/courinha768/nas-ac/nas-ac:latest

