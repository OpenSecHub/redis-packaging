# redis-packaging

> build redis rpm package on CentOS 7
>
> Debian https://github.com/redis/redis-debian


```bash
#!/bin/bash


# install rpm tools
yum install -y rpm-build redhat-rpm-config rpmdevtools 

# install build tools
yum install -y make gcc openssl-devel git

# create a new user(rpm) to do rpmbuild
id rpm 2>/dev/null
if [ $? -ne 0 ] ; then
    useradd -r -d /home/rpm -c "rpm maker" -s /bin/bash rpm
    mkdir -p /home/rpm
    chown -R rpm:rpm /home/rpm
fi

# change user to rpm to do rpmbuild
#####################################################################################
su rpm << EOF

cd ~
rm -rf  ~/rpmbuild/
# mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
rpmdev-setuptree

rm -rf redis-packaging
git clone https://github.com/OpenSecHub/redis-packaging.git

cp redis-packaging/rpm/SOURCES/* ~/rpmbuild/SOURCES
cp redis-packaging/rpm/SPECS/*   ~/rpmbuild/SPECS

# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec

# show rpm packages
cd ~/rpmbuild/RPMS/x86_64/
ls -lh $PWD/*

exit
EOF
#####################################################################################
```
