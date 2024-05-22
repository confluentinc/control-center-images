import setuptools

# Read the requirements from the requirements.txt file
def read_requirements():
    try:
        with open("requirements.txt") as req_file:
            return req_file.read().splitlines()
    except FileNotFoundError:
        return []

setuptools.setup(
    name='control-center-tests',
    version='0.0.1',
    author="Confluent, Inc.",
    author_email="c3@confluent.io",
    description='Control center docker image tests',
    url="https://github.com/confluentinc/control-center-images",
    install_requires=read_requirements(),
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    setup_requires=['setuptools-git'],
)
