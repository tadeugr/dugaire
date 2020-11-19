requirements:
	pip install -r requirements.txt

install:
	make requirements
	pip3 install . --force

install-dev:
	make requirements
	pip3 install --editable . --force

build:
	pyinstaller --onefile --name=dugaire dugaire.py