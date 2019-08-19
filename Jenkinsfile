#!/usr/bin/env groovy

def defaultParams = [
    string(name: 'CONFLUENT_MAJOR_VERSION',
      defaultValue: '',
      description: 'Major version number.'),
    string(name: 'CONFLUENT_MINOR_VERSION',
      defaultValue: '',
      description: 'Minor version number.'),
    string(name: 'CONFLUENT_PATCH_VERSION',
      defaultValue: '',
      description: 'Patch version number.'),
    string(name: 'PACKAGING_BRANCH_NAME',
      defaultValue: '',
      description: 'Branch of packaging job.'),
    string(name: 'PACKAGING_BUILD_NUMBER',
      defaultValue: '',
      description: 'Build number of packaging job.'),
    string(name: 'CONFLUENT_PACKAGES_REPO',
      defaultValue: 'https://jenkins-confluent-packages.s3-us-west-2.amazonaws.com',
      description: 'Url of packages repo.'),
    string(name: 'CONFLUENT_PLATFORM_LABEL',
      defaultValue: '~SNAPSHOT',
      description: 'Platform label.'),
    string(name: 'CONFLUENT_DEB_VERSION',
      defaultValue: '1',
      description: 'Debian package version.'),
    string(name: 'ALLOW_UNSIGNED',
      defaultValue: 'true',
      description: 'Allow unsigned packages.')
]


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
