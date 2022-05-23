APP=students
VERSION = $(shell git rev-parse --short HEAD)


format:
	black app/*

.PHONY: setup-env
setup-env:

.PHONY: build
build:
	pipenv lock -r > requirements.txt
	docker build -t $(APP):$(VERSION) .

.PHONY: run
run:
	uvicorn app.main:app --reload
