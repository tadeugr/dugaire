# stevedore
Command line tool to quickly build docker images with custom packages.

python3 dugaire/dugaire.py build -i kubectl -i curl

stevedore build --name=my-image --output=image-id --bi=terraform:3 --pm=curl --pi=ansible

docker images -f label='builtwith=dugaire'

pip install --editable .

pip3 install --upgrade setuptools