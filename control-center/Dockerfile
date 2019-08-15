ARG DOCKER_UPSTREAM_REGISTRY
ARG DOCKER_UPSTREAM_TAG=latest
 
FROM ${DOCKER_UPSTREAM_REGISTRY}confluentinc/cp-base-new:${DOCKER_UPSTREAM_TAG}

ARG PROJECT_VERSION
ARG ARTIFACT_ID
 
# Make sure you use an appropriate contact address.
MAINTAINER partner-support@confluent.io
LABEL io.confluent.docker=true
ARG COMMIT_ID=unknown
LABEL io.confluent.docker.git.id=$COMMIT_ID
ARG BUILD_NUMBER=-1
LABEL io.confluent.docker.build.number=$BUILD_NUMBER

ENV COMPONENT=control-center 
ENV CONTROL_CENTER_DATA_DIR=/var/lib/confluent-${COMPONENT}
ENV CONTROL_CENTER_CONFIG_DIR=/etc/confluent-${COMPONENT}

# Default listener
EXPOSE 9021 

COPY include/etc/confluent/docker /etc/confluent/docker

RUN bash /etc/confluent/docker/print_env

RUN echo "===> Installing ${COMPONENT}..." \
    && apt-get update \
    && echo "===> Adding confluent repository...${CONFLUENT_PACKAGES_REPO}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION}" \
    && if [ "x$ALLOW_UNSIGNED" = "xtrue" ]; then echo "APT::Get::AllowUnauthenticated \"true\";" > /etc/apt/apt.conf.d/allow_unauthenticated; else curl -L ${CONFLUENT_PACKAGES_REPO}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION}/archive.key | apt-key add - ; fi \
    && echo "deb [arch=amd64] ${CONFLUENT_PACKAGES_REPO}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION} stable main" >> /etc/apt/sources.list \
    && apt-get install -y confluent-${COMPONENT}=${CONFLUENT_VERSION}${CONFLUENT_PLATFORM_LABEL}-${CONFLUENT_DEB_VERSION} \
    \
    && echo "===> Cleaning up ..."  \
    && apt-get clean && rm -rf /tmp/* /var/lib/apt/lists/* \
    \
    && echo "===> Setting up ${COMPONENT} dirs" \
    && mkdir -p "${CONTROL_CENTER_DATA_DIR}" \
    && chmod -R ag+w "${CONTROL_CENTER_CONFIG_DIR}" "${CONTROL_CENTER_DATA_DIR}"



CMD ["/etc/confluent/docker/run"]
