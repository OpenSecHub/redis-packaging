#/usr/bin/env bash

CONTAINER_NAME=redis_builder
CONTAINER_TAG=6.2.6

# copy rpm sources
rm -rf rpm
cp -r ../rpm .

# build docker
docker build -t ${CONTAINER_NAME}:${CONTAINER_TAG} .
rm -rf rpm

# build source with docker
rm -rf    output
mkdir -p  output
chmod 777 output
docker run -t --rm -v $PWD/output:/home/redis/rpmbuild ${CONTAINER_NAME}:${CONTAINER_TAG}

