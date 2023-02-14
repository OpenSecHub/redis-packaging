#!/bin/bash

if [ ! -d /root/rpmbuild ] ; then
  echo "Mount Resources on /root/rpmbuild"
  exit 127
fi


# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec 2>&1 | tee ~/rpmbuild/build.log

exit 0
