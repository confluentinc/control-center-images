#!/usr/bin/env groovy
 
dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
//    dockerUpstreamTag = 'trunk-latest'
    mvnPhase = 'package' // enable later: integration-test
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-compose'
    slackChannel = 'tools' //temporary until done developing this.
    //upstreamProjects = ['confluentinc/common'] // Need to update this at the end
    dockerPullDeps = ['confluentinc/cp-base-new']
}

//dockerPullDeps = ['confluentinc/cp-base-new']