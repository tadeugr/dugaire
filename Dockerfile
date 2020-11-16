FROM ubuntu:18.04
LABEL stvid="123"

RUN apt-get update -qq
RUN apt-get install -qqy --no-install-recommends curl ca-certificates

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
#RUN curl -k -LO https://storage.googleapis.com/kubernetes-release/release/latest/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin
#ARG MYAPP_IMAGE=myorg/myapp:latest
#COPY --from=$APP_IMAGE /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl