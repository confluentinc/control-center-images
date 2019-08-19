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
    properties = [
        parameters([
            string(name: 'TEST_PATH', defaultValue: 'muckrake/tests/ muckrake/connector_tests/', description: 'Use this to specify a test or subset of tests to run.'),
            string(name: 'NUM_WORKERS', defaultValue: '40', description: 'Number of EC2 nodes to use when running the tests.'),
            string(name: 'INSTALL_TYPE', defaultValue: 'source', description: 'Use tarball or source'),
            string(name: 'RESOURCE_URL', defaultValue: '', description: 'If using tarball, specify S3 URL to download artifacts from'),
            string(name: 'PARALLEL', defaultValue:'true', description: 'Whether to execute the tests in parallel. If disabled, you should probably reduce NUM_WORKERS')
        ])
    ]
}
