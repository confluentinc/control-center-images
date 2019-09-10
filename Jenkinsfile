#!/usr/bin/env groovy

dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
    mvnPhase = 'package'
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose-swarm'
    slackChannel = 'tools' //TODO: change to correct team
    upstreamProjects = [] //TODO: after roll out, this will be cp-docker-images-overlay
    dockerPullDeps = ['confluentinc/cp-base-new']
    usePackages = true
}
