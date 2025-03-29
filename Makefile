#SOURCES := $(shell find src/striem_configure/sources | sed  's:\.py::g' | tr '/' '.' | sed 's:^:--hidden-import :g' | grep -v 'sources._' | sed 's:^src\.::g' | xargs)

SYSPYTHON=$(shell which python3)
VENV=venv
PYTHON="$(VENV)/bin/python"
PIP="$(VENV)/bin/pip"

all: venv
	$(VENV)/bin/pyinstaller \
		--onefile \
		--collect-all striem_configure \
		--name striem-configure \
		src/__main__.py
none:
	--add-data src/striem_configure/static:striem_configure/static \
	--add-data src/striem_configure/template:striem_configure/templates \
	--onefile \
	--name striem-configure \
	__main__.py

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(SYSPYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-build.txt
	$(PIP) install .

clean:
	rm -rf build dist venv striem-configure.spec
