APP=students
VERSION = $(shell git rev-parse --short HEAD)


.PHONY: build
build:
	pipenv lock -r > requirements.txt
	docker build -t $(APP):$(VERSION) .
