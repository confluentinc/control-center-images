FROM 519856050701.dkr.ecr.us-west-2.amazonaws.com/docker/prod/confluentinc/cp-base-java:master-latest-ubi9 as builder

WORKDIR /app

ENV COMPONENT=control-center
ENV CONTROL_CENTER_DATA_DIR=/var/lib/confluent-${COMPONENT}
ENV CONTROL_CENTER_CONFIG_DIR=/etc/confluent-${COMPONENT}

#ENV CONFLUENT_PACKAGES_REPO=https://packages.confluent.io/archive/7.7
ENV CONFLUENT_PACKAGES_REPO=http://confluent-platform-hotfixes-891377121322-us-west-2.s3-website-us-west-2.amazonaws.com/7.7.1-cp3/rpm/7.7

USER root


RUN echo "===> Installing ${COMPONENT}..."
RUN rpm --import ${CONFLUENT_PACKAGES_REPO}/archive.key

RUN printf "[Confluent.dist] \n\
name=Confluent repository (dist) \n\
baseurl=${CONFLUENT_PACKAGES_REPO}/7 \n\
gpgcheck=1 \n\
gpgkey=${CONFLUENT_PACKAGES_REPO}/archive.key \n\
enabled=1 \n\
\n\
[Confluent] \n\
name=Confluent repository \n\
baseurl=${CONFLUENT_PACKAGES_REPO}/ \n\
gpgcheck=1 \n\
gpgkey=${CONFLUENT_PACKAGES_REPO}/archive.key \n\
enabled=1 " > /etc/yum.repos.d/confluent.repo


ENV CONFLUENT_VERSION=7.7.1

RUN microdnf install -y confluent-${COMPONENT}-${CONFLUENT_VERSION}
RUN echo "===> Cleaning up ..."  \
    && microdnf clean all \
    && echo "===> Setting up ${COMPONENT} dirs" \
    && mkdir -p "${CONTROL_CENTER_DATA_DIR}" \
    && chown appuser:root -R "${CONTROL_CENTER_DATA_DIR}" \
    && chown appuser:root -R "${CONTROL_CENTER_CONFIG_DIR}" \
    && chmod -R ug+w "${CONTROL_CENTER_CONFIG_DIR}" "${CONTROL_CENTER_DATA_DIR}"


FROM registry.access.redhat.com/ubi9/ubi-micro:latest

ARG ARCH

RUN mkdir /etc/prometheus && \
    mkdir /bin/prometheus

COPY --from=builder /usr/libexec/confluent-control-center/linux_$ARCH/prometheus/ /bin/prometheus
COPY --from=builder /etc/confluent-control-center/prometheus-generated.yml /etc/prometheus/prometheus.yml
COPY --from=builder /etc/confluent-control-center/trigger_rules-generated.yml /etc/prometheus/
COPY --from=builder /etc/confluent-control-center/recording_rules-generated.yml /etc/prometheus/
# alertmanager-generated.yml

RUN for file in bin/prometheus/prometheus*; do mv "$file" bin/prometheus/prometheus; done

EXPOSE 9090

RUN chmod +x /bin/prometheus/prometheus
WORKDIR /prometheus


RUN echo "appuser:x:1000:1000::/home/appuser:/bin/sh" >> /etc/passwd && \
    mkdir -p /home/appuser && \
    chown 1000:1000 /home/appuser

RUN chown -R 1000:1000 /etc/prometheus /prometheus
USER appuser
# Make the entrypoint script executable

VOLUME     [ "/prometheus" ]
ENTRYPOINT [ "/bin/prometheus/prometheus" ]
CMD        [ "--config.file=/etc/prometheus/prometheus.yml", \
             "--storage.tsdb.path=/prometheus" ]