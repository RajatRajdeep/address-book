# Address Book Application

Welcome to the Address Book Application! This application provides an API for managing addresses. Users can create, read, update, and delete addresses in the address book.
It's built using [FastAPI](https://fastapi.tiangolo.com/).

## Project Structure

- **main.py:** This file is the generic entry point and the root of our FastAPI application.
- **cloud_build/:** The cloud build directory contains GCP cloud build configuration files.
- **.dockerignore:**.dockerignore file is used to ignore files and folders when building a Docker Image. It's similar to the .gitignore file.
- **.gitignore:**.gitignore file specifies intentionally untracked files that Git should ignore. Files already tracked by Git are not affected.
- **requirements.txt:** This file stores information about all the libraries, modules, and packages that are used to build the project.

## Project Setup/ Installation Guide

- Clone the repository using the below git clone command.

```
    git clone https://github.com/RajatRajdeep/address-book.git
```

- Install [python 3.10.4](https://www.python.org/downloads/release/python-3104) which comes with pip3.
- Change your current directory to address-book/.
- Install Virtualenv and create a virtual environment using pip3. Follow the below commands for macOS:

```
pip3 install virtualenv
virtualenv <env_name>
```

- Activate the virtual environment and install dependencies. Follow the below commands for macOS:

```
source <env_name>/bin/activate
pip3 install -r requirements.txt
```

- The setup is complete! Run the FastAPI application using the below command.

```
uvicorn main:app
```

## Built With

- [FastAPI 0.95.0](https://fastapi.tiangolo.com)
- [Python 3.10.4](https://www.python.org/downloads/)

## Authors

- [**Rajat Rajdeep**](https://rajatrajdeep.in)
