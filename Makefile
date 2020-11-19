requirements:
	pip install -r dugaire/requirements.txt

install:
	make requirements
	pip3 install . --force

install-dev:
	make requirements
	pip3 install --editable . --force