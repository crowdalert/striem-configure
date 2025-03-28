SOURCES := $(shell find sources | sed  's:\.py::g' | tr '/' '.' | sed 's:^:--hidden-import :g' | grep -v 'sources._' |  xargs)

SYSPYTHON=$(shell which python3)
VENV=venv
PYTHON="$(VENV)/bin/python"
PIP="$(VENV)/bin/pip"

all: venv
	$(VENV)/bin/pyinstaller $(SOURCES) --add-data template:template \
		--add-data static:static \
		--add-data docker-compose.yaml:. \
		striem-configure.py

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(SYSPYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
