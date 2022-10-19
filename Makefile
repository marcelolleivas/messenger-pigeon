SHELL := /bin/bash

.pip:
	pip install --upgrade 'pip<22'

.install-dependencies:
	pip install pipenv pre-commit &&\
    pipenv install &&\
    pipenv shell

install-dev: .pip .install-dependencies

code-convention:
	pre-commit run --all-files
