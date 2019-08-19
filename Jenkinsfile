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
    extraBuildArgs = "-DCONFLUENT_MAJOR_VERSION=${params.CONFLUENT_MAJOR_VERSION} -DCONFLUENT_MINOR_VERSION=${params.CONFLUENT_MINOR_VERSION} -DCONFLUENT_PATCH_VERSION=${params.CONFLUENT_PATCH_VERSION} -DPACKAGING_BRANCH_NAME=${params.PACKAGING_BRANCH_NAME} -DPACKAGING_BUILD_NUMBER=${params.PACKAGING_BUILD_NUMBER} -DCONFLUENT_PACKAGES_REPO=${params.CONFLUENT_PACKAGES_REPO} -DCONFLUENT_PLATFORM_LABEL=${params.CONFLUENT_PLATFORM_LABEL} -DCONFLUENT_DEB_VERSION=${params.CONFLUENT_DEB_VERSION} -DALLOW_UNSIGNED=${params.ALLOW_UNSIGNED}"
}
