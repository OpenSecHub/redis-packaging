# redis-packaging

> build redis rpm package


```bash
# install rpm tools
yum install rpm-build redhat-rpm-config rpmdevtools 

# install build tools
yum install make gcc openssl-devel

# create a new user to do rpmbuild
useradd -r -d /home/rpm -c "rpm maker" -s /bin/bash rpm
mkdir -p /home/rpm
chown -R rpm:rpm /home/rpm
su rpm

# cd ~ && rpmdev-setuptree
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

git clone https://github.com/OpenSecHub/redis-packaging.git

cp redis-packaging/rpm/SOURCES/* ~/rpmbuild/SOURCES
cp redis-packaging/rpm/SPECS/*   ~/rpmbuild/SPECS

# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec

# show rpm packages
ls -lh  ~/rpmbuild/RPMS/x86_64/
```