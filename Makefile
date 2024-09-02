VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

ifeq (run, $(firstword $(MAKECMDGOALS)))
  runargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(runargs):;@true)
endif

setup:
	virtualenv --python python3.10 $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__

#run:
#	$(PYTHON) main.py --input $(input) --output $(output) --schema $(schema)

auth:
	$(PYTHON) auth.py $(filter-out $@, $(MAKECMDGOALS))

help:
	echo "make run --input input.csv --output output.csv --schema mapping.json"