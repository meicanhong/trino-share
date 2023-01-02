NAME = trino
TAG = beta

build:
	echo building ${NAME}:${TAG}

ifeq ($(TAG), beta)
	docker build -f ./master/Dockerfile -t ${NAME}-master:${TAG} .
	docker build -f ./worker/Dockerfile -t ${NAME}-worker:${TAG} .
endif
