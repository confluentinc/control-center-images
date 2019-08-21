#!/usr/bin/env groovy

dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center-image',]
    mvnPhase = 'package exec:exec@python-docker-tests' //TODO: enable integration-test
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-eli-compose'
    slackChannel = 'tools' //TODO: change to correct team
    upstreamProjects = ['confluentinc/common']
    dockerPullDeps = ['confluentinc/cp-base-new']
    usePackages = true
    //for testing only
    extraBuildArgs = "-DCONFLUENT_MAJOR_VERSION=5 -DCONFLUENT_MINOR_VERSION=3 -DCONFLUENT_PATCH_VERSION=1 -DPACKAGING_BRANCH_NAME=5.3.x -DPACKAGING_BUILD_NUMBER=186 -DCONFLUENT_PACKAGES_REPO=https://jenkins-confluent-packages.s3-us-west-2.amazonaws.com -DCONFLUENT_PLATFORM_LABEL=~SNAPSHOT -DCONFLUENT_DEB_VERSION=1 -DALLOW_UNSIGNED=false"
}
