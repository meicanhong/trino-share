FROM trinodb/trino:403
USER root:root
RUN apt-get update && apt-get install -y unzip

USER trino:trino
RUN rm -fr /etc/trino/catalog/*

COPY catalog /etc/trino/catalog
COPY ./master/config.properties /etc/trino/config.properties
COPY ./master/jvm.config /etc/trino/jvm.config
COPY ./master/node.properties /etc/trino/node.properties
COPY config /etc/trino/config
COPY user/password.db /etc/trino/password.db
COPY user/password-authenticator.properties /etc/trino/password-authenticator.properties
COPY user/user-mapping.json /etc/trino/user-mapping.json
COPY resource/resource-groups.properties /etc/trino/resource-groups.properties
COPY resource/resource-groups.json /etc/trino/resource-groups.json