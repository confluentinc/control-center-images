#!/usr/bin/env groovy

dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/cp-enterprise-control-center',]
    mvnPhase = 'package'
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose-swarm'
    slackChannel = 'c3-alert'
    upstreamProjects = []
    dockerPullDeps = ['confluentinc/cp-base']
    usePackages = true
    cron = '' // Disable the cron because this job requires parameters
}
