# redis-packaging

> build redis rpm package on CentOS 7


```bash
#!/bin/bash

REDISVER=6.2.2

# install rpm tools
yum install -y rpm-build redhat-rpm-config rpmdevtools 

# install build tools
yum install -y make gcc openssl-devel git

# create a new user(rpm) to do rpmbuild
id rpm
if [ $? -ne 0 ] ; then
    useradd -r -d /home/rpm -c "rpm maker" -s /bin/bash rpm
    mkdir -p /home/rpm
    chown -R rpm:rpm /home/rpm
fi

# change user to rpm to do rpmbuild
#####################################################################################
su rpm << EOF

cd ~
# mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
rpmdev-setuptree 

git clone https://github.com/OpenSecHub/redis-packaging.git -b ${REDISVER}

cp redis-packaging/rpm/SOURCES/* ~/rpmbuild/SOURCES
cp redis-packaging/rpm/SPECS/*   ~/rpmbuild/SPECS

# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec

# show rpm packages
ls -lh  ~/rpmbuild/RPMS/x86_64/

exit
EOF
#####################################################################################
```
