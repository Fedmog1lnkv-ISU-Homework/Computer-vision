PYTHON_FILE = main.py
POETRY_EXECUTABLE = poetry
INSTALL_DEPS = $(POETRY_EXECUTABLE) install

all: run

run: venv
	$(POETRY_EXECUTABLE) run python $(PYTHON_FILE)

venv:
	$(INSTALL_DEPS)

deps: venv

clean:
	rm -rf __pycache__ *.pyc

.PHONY: all run venv deps clean
