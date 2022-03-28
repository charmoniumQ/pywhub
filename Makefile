SHELL := /bin/bash
DOCKER_ORG ?= crs4
DOCKER_IMG ?= $(DOCKER_ORG)/seek:workflow-pywhub
DOCKER_DATA_IMG ?= $(DOCKER_IMG)-data
WHUB_HOST_PORT ?= 3000

setup:
	docker pull $(DOCKER_IMG)
	docker pull $(DOCKER_DATA_IMG)
	docker run -v /seek/filestore -v /seek/sqlite3-db --name hubdata $(DOCKER_DATA_IMG) bash
	docker run -d -p $(WHUB_HOST_PORT):3000 --volumes-from hubdata --name hub $(DOCKER_IMG)

teardown:
	docker stop hub
	docker inspect -f '{{range .Mounts}}{{println .Name}}{{end}}' hub > .tbr
	docker rm hub hubdata
	docker volume rm $$(cat .tbr)
	rm -f .tbr

.PHONY: setup teardown
