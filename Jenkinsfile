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
    properties = [parameters(defaultParams)]
}
