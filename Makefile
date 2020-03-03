
help:
	@echo "clean - remove all build, test and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "format - autoformat Python source"
	@echo "lint - check style"
	@echo "test - run tests quickly with the default Python"

all: default

default: clean dev_deps deps format test lint build

.venv:
	if [ ! -e ".venv/bin/activate_this.py" ] ; then virtualenv -p python3 .venv ; fi

clean: clean-pyc clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -rf build/ dist/

deps: .venv
	. .venv/bin/activate && pip install -U -r requirements.txt

dev_deps: .venv
	. .venv/bin/activate && pip install -U -r dev_requirements.txt

setup: deps dev_deps

format:
	. .venv/bin/activate && autopep8 --in-place -r src/ tests/

lint:
	. .venv/bin/activate && pylint -r n src/main.py src/git src/bitbucket

test:
	. .venv/bin/activate && python -m unittest discover

dist:
	. .venv/bin/activate && python setup.py sdist	

release: dist
	. .venv/bin/activate && python -m twine upload dist/*
