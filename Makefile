requirements:
	pip install -r requirements.txt

requirements-dev:
	pip install -r requirements-dev.txt

install:
	make requirements
	pip install . --force

install-dev:
	make requirements
	make requirements-dev
	pip install --editable . --force

test:
	pytest --disable-pytest-warnings

dist:
	rm -fr *.egg-info dist || true
	python setup.py sdist bdist_wheel
.PHONY: dist

# binary:
# 	#pyinstaller --onefile --name=dugaire dugaire.py
# 	cd dugaire
# 	pyinstaller --clean -y --name=dugaire --add-data="templates\base.j2;templates" dugaire.py

readme:
	python3 docs/make_readme.py > README.md

readthedocs:
	pandoc README.md --from markdown --to rst -s -o docs/index.rst

docker-rm:
	docker rmi -f $(docker images -aq -f label='builtwith=dugaire')

pre-commit:
	black .
	make readme
	make readthedocs