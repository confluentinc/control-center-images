#!/usr/bin/env groovy

dockerfile {
    dockerPush = false
    dockerRepos = ['confluentinc/cp-enterprise-control-center',]
    mvnPhase = 'package integration-test'
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose-swarm'
    slackChannel = 'tools-notifications' //TODO: change to correct team
    upstreamProjects = [] //TODO: after roll out, this will be cp-docker-images-overlay
    dockerPullDeps = ['confluentinc/cp-base-new']
    usePackages = true
    cron = '' // Disable the cron because this job requires parameters
}
