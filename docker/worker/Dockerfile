FROM trinodb/trino:403
USER root:root
RUN apt-get update && apt-get install -y unzip

USER trino:trino
RUN rm -fr /etc/trino/catalog/*

COPY catalog /etc/trino/catalog
COPY ./worker/config.properties /etc/trino/config.properties
COPY ./worker/jvm.config /etc/trino/jvm.config
COPY ./worker/node.properties /etc/trino/node.properties
COPY config /etc/trino/config
COPY user/password.db /etc/trino/password.db
COPY user/password-authenticator.properties /etc/trino/password-authenticator.properties
COPY user/user-mapping.json /etc/trino/user-mapping.json