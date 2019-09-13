import setuptools


setuptools.setup(
    name='control-center-tests',
    version='0.0.1',
    author="Confluent, Inc.",
    author_email="c3@confluent.io",
    description='Control center docker image tests',
    url="https://github.com/confluentinc/control-center-images",
    dependency_links=open("requirements.txt").read().split("\n"),
    packages=['test'],
    include_package_data=True,
    python_requires='>=2.7',
    setup_requires=['setuptools-git'],
)
