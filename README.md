# control-center-images
Docker images for control center
This will build the control center docker image with debian packages and rpm's.
It will use the packages from the packaging build.

## Properties

Properties are inherited from a top-level POM. Properties may be overridden on the command line (`-DCONFLUENT_MAJOR_VERSION=5`), or in a subproject's POM.

- *CONFLUENT_MAJOR_VERSION*: Major version number.
- *CONFLUENT_MINOR_VERSION*: Minor version number.
- *CONFLUENT_PATCH_VERSION*: Patch version number.
- *PACKAGING_BRANCH_NAME*: Branch of packaging job.
- *PACKAGING_BUILD_NUMBER*: Build number of packaging job.
- *CONFLUENT_PACKAGES_REPO*: (Optional) Url of packages repo.
- *CONFLUENT_PLATFORM_LABEL*: (Optional) Platform label.
- *CONFLUENT_DEB_VERSION*: (Optional) Debian package version.
- *ALLOW_UNSIGNED*: (Optional) Allow unsigned packages.

## Building

This project uses `dockerfile-maven-plugin` to build Docker images via Maven.
The Dockerfile will register the apt/yum repo where the packages were uploaded by the 
packaging job.
