FROM centos:7

# change repo
#RUN rm -f /etc/yum.repos.d/*

# add epel repo
RUN yum install epel-release

# install rpm tools
RUN yum install -y rpm-build redhat-rpm-config rpmdevtools

# install build tools
RUN yum install -y make gcc openssl-devel systemd-devel jemalloc

# redis makefile need these
RUN yum install -y which python3 tcl tcltls

# entrypoint
ADD entrypoint.sh  /
ENTRYPOINT ["/entrypoint.sh"]
