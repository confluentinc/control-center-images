#!/usr/bin/env groovy
 
dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
//    dockerUpstreamTag = 'trunk-latest'
    mvnPhase = 'package integration-test' // enable later: 
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8' //change this back to -compose image???
    slackChannel = 'tools' //temporary until done developing this.
    //upstreamProjects = ['confluentinc/common'] // Need to update this at the end
    dockerPullDeps = ['confluentinc/cp-base-new']
}
