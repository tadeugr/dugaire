```
cd dugaire
```

Command line tool to quickly build docker images with custom packages.

python3 dugaire/dugaire.py build -apt=curl,vim -kubectl=latest

python3 dugaire/dugaire.py build -i kubectl -i curl

stevedore build --name=my-image --output=image-id --bi=terraform:3 --pm=curl --pi=ansible

docker images -f label='builtwith=dugaire'

pip install --editable .

pip3 install --upgrade setuptools

# Install (on Linux)

Clone this repo.

`cd` to its directory.

```
cd dugaire
```

Install it.

```
make install
```

You should have the command available.

```
dugaire --help
```

# Supported features

## Base images

Dugaire supports `ubuntu:18.04`. More to come soon.

## Package Managers

Dugaire supports `apt-get`. More to come soon.

## Packages

* kubectl