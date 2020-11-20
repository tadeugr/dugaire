requirements:
	pip install -r requirements.txt

install:
	make requirements
	pip install . --force

install-dev:
	make requirements
	pip install --editable . --force

test:
	pytest

setup:
	python setup.py sdist bdist_wheel

binary:
	#pyinstaller --onefile --name=dugaire dugaire.py
	cd dugaire
	pyinstaller --clean -y --name=dugaire --add-data="templates\base.j2;templates" dugaire.py

docker-rm:
	docker rmi -f $(docker images -aq -f label='builtwith=dugaire')