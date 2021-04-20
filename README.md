# redis-packaging

```bash
# install rpm tools
yum install rpm-build redhat-rpm-config rpmdevtools 

# install build tools
yum install make gcc openssl-devel

# create a new user to do rpmbuild
useradd -r -c "rpm maker" -s /bin/bash rpm
su rpm

# cd ~ && rpmdev-setuptree
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

git clone https://github.com/OpenSecHub/redis-packaging.git

cp redis-packaging/SOURCES/* ~/rpmbuild/SOURCES
cp redis-packaging/SPECS/*   ~/rpmbuild/SPECS

# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec

```

