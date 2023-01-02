NAME = footbase-trino
REGISTRY = docker-registry.footprint.network
NAMESPACE=mexl
TAG = beta

build:
	echo building ${REGISTRY}/${NAMESPACE}/${NAME}:${TAG}

ifeq ($(TAG), master)
	cd docker/prod && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/prod && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif

ifeq ($(TAG), beta)
	cd docker/beta && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/beta && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif

ifeq ($(TAG), prod-query)
	cd docker/prod-query && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/prod-query && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif

ifeq ($(TAG), event-test)
	cd docker/event-test && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/event-test && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif

ifeq ($(TAG), big-cal)
	cd docker/big-cal && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/big-cal && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif

ifeq ($(TAG), datadog)
	cd docker/event-test && docker build -f datadog-Dockerfile -t docker-registry.footprint.network/mexl/event-test:datadog .
	docker push docker-registry.footprint.network/mexl/event-test:datadog
endif

ifeq ($(TAG), beta-cal-datadog)
	cd docker/beta/datadog && docker build -f Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG}
endif

ifeq ($(TAG), prod-query-datadog)
	cd docker/prod-query/datadog && docker build -f Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG}
endif

ifeq ($(TAG), prod-cal-datadog)
	cd docker/prod/datadog && docker build -f Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-datadog:${TAG}
endif

ifeq ($(TAG), beta-query)
	cd docker/beta-query && docker build -f ./master/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-master:${TAG}

	cd docker/beta-query && docker build -f ./worker/Dockerfile -t ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG} .
	docker push ${REGISTRY}/${NAMESPACE}/${NAME}-worker:${TAG}
endif
