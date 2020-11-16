# stevedore
Command line tool to quickly build docker images with custom packages.

stevedore build --name=my-image --output=image-id --bi=terraform:3 --pm=curl --pi=ansible

docker images -f label='stvid=123'