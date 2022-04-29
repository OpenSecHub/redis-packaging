#!/bin/bash

su redis << EOF
cd ~

cp -r ~/buildres/*  ~/rpmbuild/

# download redis source
spectool -g -R ~/rpmbuild/SPECS/redis.spec

# generate rpm packages
rpmbuild -ba ~/rpmbuild/SPECS/redis.spec 2>&1 | tee ~/rpmbuild/build.log

exit
EOF