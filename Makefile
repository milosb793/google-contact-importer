VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

setup:
	virtualenv --python python3.10 $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__

run:
	$(PYTHON) main.py

auth:
	$(PYTHON) auth.py