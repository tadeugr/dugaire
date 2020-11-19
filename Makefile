requirements:
	pip install -r requirements.txt

install:
	make requirements
	pip install . --force

install-dev:
	make requirements
	pip install --editable . --force

build:
	pyinstaller --onefile --name=dugaire dugaire.py

pkg:
	python setup.py sdist bdist_wheel