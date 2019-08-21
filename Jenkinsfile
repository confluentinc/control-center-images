#!/usr/bin/env groovy
//TODO: remove defaults when done testing
def defaultParams = [
    string(name: 'CONFLUENT_MAJOR_VERSION',
      defaultValue: '5',
      description: 'Major version number.'),
    string(name: 'CONFLUENT_MINOR_VERSION',
      defaultValue: '3',
      description: 'Minor version number.'),
    string(name: 'CONFLUENT_PATCH_VERSION',
      defaultValue: '1',
      description: 'Patch version number.'),
    string(name: 'PACKAGING_BRANCH_NAME',
      defaultValue: '5.3.x',
      description: 'Branch of packaging job.'),
    string(name: 'PACKAGING_BUILD_NUMBER',
      defaultValue: '186',
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
      defaultValue: '',
      description: 'Allow unsigned packages.')
]

// This needs to be defined as a variable here otherwise it tries to resolve
// the parameters before they have been set.
def mvnArgs = "-DCONFLUENT_MAJOR_VERSION=${params.CONFLUENT_MAJOR_VERSION} -DCONFLUENT_MINOR_VERSION=${params.CONFLUENT_MINOR_VERSION} -DCONFLUENT_PATCH_VERSION=${params.CONFLUENT_PATCH_VERSION} -DPACKAGING_BRANCH_NAME=${params.PACKAGING_BRANCH_NAME} -DPACKAGING_BUILD_NUMBER=${params.PACKAGING_BUILD_NUMBER} -DCONFLUENT_PACKAGES_REPO=${params.CONFLUENT_PACKAGES_REPO} -DCONFLUENT_PLATFORM_LABEL=${params.CONFLUENT_PLATFORM_LABEL} -DCONFLUENT_DEB_VERSION=${params.CONFLUENT_DEB_VERSION} -DALLOW_UNSIGNED=${params.ALLOW_UNSIGNED}"

dockerfile {
    dockerPush = true
    dockerRepos = ['confluentinc/control-center',]
//    dockerUpstreamTag = 'trunk-latest'
    mvnPhase = 'package'
    mvnSkipDeploy = true
    nodeLabel = 'docker-oraclejdk8-eli-compose' //docker-oraclejdk8-compose
    slackChannel = 'tools' //temporary until done developing this.
    //upstreamProjects = ['confluentinc/common'] // Need to update this at the end
    dockerPullDeps = ['confluentinc/cp-base-new']
    properties = [parameters(defaultParams)]
    extraBuildArgs = mvnArgs
}
