#/usr/bin/env bash
set -e
cd `dirname $0`
##########################################################
REALSE_URL="https://github.com/redis/redis/releases"
LOCATION="Location: ${REALSE_URL}/tag/"
REDIS_VERSION=$(curl -sI ${REALSE_URL}/latest | grep -i "${LOCATION}" | sed "s#${LOCATION}##" | tr -d '\r')

RELEASE_DATE=`date +'%a %b %d %Y'`
AUTHOR="LubinLew lgbxyz@gmail.com"

# build docker
CONTAINER_NAME=redis-builder
CONTAINER_TAG=latest
docker build -t ${CONTAINER_NAME}:${CONTAINER_TAG} docker


# rpmbuild resource
rm   -rf  output
mkdir -p  output/{BUILD,RPMS,SRPMS}
cp   -rf  rpm/SOURCES  output/
cp   -rf  rpm/SPECS    output/
sed   -i "s#REDIS_VERSION#${REDIS_VERSION}#" output/SPECS/redis.spec
sed   -i "s#RELEASE_DATE#${RELEASE_DATE}#"   output/SPECS/redis.spec
sed   -i "s#AUTHOR#${AUTHOR}#"               output/SPECS/redis.spec


# build
docker run -t --rm -h ${CONTAINER_NAME} -v $PWD/output:/root/rpmbuild ${CONTAINER_NAME}:${CONTAINER_TAG}

