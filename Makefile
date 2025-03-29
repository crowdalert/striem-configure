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

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(SYSPYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-build.txt
	$(PIP) install .

clean:
	rm -rf build dist venv striem-configure.spec src/striem_configure.egg-info
