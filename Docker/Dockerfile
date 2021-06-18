FROM centos:7


# install rpm tools
RUN yum install -y rpm-build redhat-rpm-config rpmdevtools

# install build tools
RUN yum install -y make gcc openssl-devel

# create new user
RUN adduser redis
RUN mkdir -p /home/redis/rpmbuild
RUN chown redis:redis -R /home/redis/rpmbuild

# add build scripts
RUN mkdir -p /home/redis/buildres/{BUILD,RPMS,SRPMS,SOURCES,SPECS}
COPY rpm/SOURCES    /home/redis/buildres/SOURCES/
COPY rpm/SPECS      /home/redis/buildres/SPECS/
RUN chown redis:redis -R /home/redis/buildres

ADD build.sh /
RUN chmod +x /build.sh

# set entrypoint
ENTRYPOINT ["/build.sh"]