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

# TODO: remove these. just hard coding now for testing.
ARG CONFLUENT_PACKAGES_REPO="https://jenkins-confluent-packages.s3-us-west-2.amazonaws.com"
ARG BRANCH
ARG UPSTREAM_BUILD_NUMBER="179"
ARG CONFLUENT_MAJOR_VERSION="5"
ARG CONFLUENT_MINOR_VERSION="3"
ARG ALLOW_UNSIGNED
# I thought these should already be available.
ARG CONFLUENT_VERSION="5.3.1"
ARG CONFLUENT_PLATFORM_LABEL="~SNAPSHOT"
ARG CONFLUENT_DEB_VERSION="1"

RUN echo "===> Installing ${COMPONENT}..."

RUN apt-get update

RUN echo "===> Adding confluent repository...${CONFLUENT_PACKAGES_REPO}/${BRANCH}/${UPSTREAM_BUILD_NUMBER}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION}"

#RUN if [ "x$ALLOW_UNSIGNED" = "xtrue" ]; then echo "APT::Get::AllowUnauthenticated \"true\";" > /etc/apt/apt.conf.d/allow_unauthenticated; else

RUN curl -s -L ${CONFLUENT_PACKAGES_REPO}/${BRANCH}/${UPSTREAM_BUILD_NUMBER}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION}/archive.key -o /tmp/archive.key

RUN apt-key add /tmp/archive.key
#; fi

RUN echo "deb [arch=amd64] ${CONFLUENT_PACKAGES_REPO}/${BRANCH}/${UPSTREAM_BUILD_NUMBER}/deb/${CONFLUENT_MAJOR_VERSION}.${CONFLUENT_MINOR_VERSION} stable main" >> /etc/apt/sources.list

RUN cat /etc/apt/sources.list

RUN apt-get install -y apt-transport-https

RUN apt-get update

RUN apt-get install -y confluent-${COMPONENT}=${CONFLUENT_VERSION}${CONFLUENT_PLATFORM_LABEL}-${CONFLUENT_DEB_VERSION}

RUN echo "===> Cleaning up ..."
RUN apt-get clean && rm -rf /tmp/* /var/lib/apt/lists/*

RUN echo "===> Setting up ${COMPONENT} dirs"
RUN mkdir -p "${CONTROL_CENTER_DATA_DIR}"
RUN chmod -R ag+w "${CONTROL_CENTER_CONFIG_DIR}" "${CONTROL_CENTER_DATA_DIR}"

COPY include/etc/confluent/docker /etc/confluent/docker

CMD ["/etc/confluent/docker/run"]
