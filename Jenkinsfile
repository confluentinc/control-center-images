#!/usr/bin/env groovy
 
dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
//    dockerUpstreamTag = 'trunk-latest'
    mvnPhase = 'package'
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose' //-compose
    slackChannel = 'tools' //temporary until done developing this.
    //upstreamProjects = ['confluentinc/common'] // Need to update this at the end
    dockerPullDeps = ['confluentinc/cp-base-new']
    extraBuildArgs = "-DBRANCH=5.3.x -DCONFLUENT_PACKAGES_REPO=https://jenkins-confluent-packages.s3-us-west-2.amazonaws.com -DUPSTREAM_BUILD_NUMBER=179 -DCONFLUENT_MAJOR_VERSION=5 -DCONFLUENT_MINOR_VERSION=3 -DCONFLUENT_VERSION=5.3.1 -DCONFLUENT_PLATFORM_LABEL=~SNAPSHOT -DCONFLUENT_DEB_VERSION=1 -DALLOW_UNSIGNED"
//    extraBuildArgs = "-DBRANCH=${BRANC} -DCONFLUENT_PACKAGES_REPO=${CONFLUENT_PACKAGES_REPO} -DUPSTREAM_BUILD_NUMBER=${UPSTREAM_BUILD_NUMBER} -DCONFLUENT_MAJOR_VERSION=${CONFLUENT_MAJOR_VERSION} -DCONFLUENT_MINOR_VERSION=${CONFLUENT_MINOR_VERSION} -DCONFLUENT_VERSION=${CONFLUENT_VERSION} -DCONFLUENT_PLATFORM_LABEL=${CONFLUENT_PLATFORM_LABEL} -DCONFLUENT_DEB_VERSION=${CONFLUENT_DEB_VERSION} -DALLOW_UNSIGNED=${ALLOW_UNSIGNED}"    
}
