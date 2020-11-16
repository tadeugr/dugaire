import docker
client = docker.from_env()

#client.containers.run("ubuntu:18.04", "echo hello world")

image, _ = client.images.build(
    path='.',
    dockerfile='Dockerfile',
    tag='customimage',
    #buildargs='version=1.13.0'
)
print(image)
print(_)