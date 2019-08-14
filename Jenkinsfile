#!/usr/bin/env groovy
 
dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
    dockerRegistry = '368821881613.dkr.ecr.us-west-2.amazonaws.com/'
//    dockerUpstreamTag = 'trunk-latest'
    mvnPhase = 'package' // enable later: integration-test
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose'
    slackChannel = 'tools' //temporary until done developing this.
    upstreamProjects = ['confluentinc/common'] // Need to update this at the end
}

//dockerPullDeps = ['confluentinc/cp-base-new']