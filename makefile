.PHONY: lint tests pytests prod github

export LINTER = flake8
export PYLINT_FLAGS = --exclude=__main__.py

PYTHON_FILES = $(wildcard *.py)
PYTEST_FLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning
PKG = api_temperature_logger
REQ_DIR = .

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests: tests

tests: lint pytests

lint: $(patsubst %.py,%.pylint,$(PYTHON_FILES))

pytests: FORCE
	export TEST_DB=1; pytest $(PYTEST_FLAGS) --cov=$(PKG)

%.pylint:
	$(LINTER) $(PYLINT_FLAGS) $*.py

# test a single Python file, invoke with "make file_name.test"
%.test: FORCE
	export TEST_DB=1; pytest $(PYTEST_FLAGS) tests/test_$*.py

dev_env: FORCE
	pip install --upgrade pip
	pip install -r $(REQ_DIR)/requirements-dev.txt