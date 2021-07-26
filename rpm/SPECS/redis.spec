##############################################################################
#                                                                            #
#                               Redis Packaging                              #
# Reference: https://rpm-packaging-guide.github.io/rpm-packaging-guide.pdf   #
#                                                                            #
##############################################################################
Name:           redis
Version:        6.2.5
Release:        1%{?dist}
Summary:        Redis is an in-memory database that persists on disk
Group:          System Environment/Daemons
License:        BSD
URL:            https://redis.io/
Vendor:         redis.io
BuildArch:      x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:       LubinLew

Source0:        https://download.redis.io/releases/redis-%{version}.tar.gz

Source1:        redis.conf
Source2:        redis-server.service
Source3:        sentinel.conf
Source4:        redis-sentinel.service
Source5:        redis_sysctl.conf

### if you want do make test, you need  `yum install tcl tcltls`
BuildRequires:  systemd, gcc, make, openssl-devel
Requires:       openssl-libs
AutoReqProv:    no


%description
Redis is an open source (BSD licensed), in-memory data structure store,
used as a database, cache, and message broker.
Redis provides data structures such as strings, hashes, lists, sets,
sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes,
and streams.
Redis has built-in replication, Lua scripting, LRU eviction, transactions,
and different levels of on-disk persistence,
and provides high availability via Redis Sentinel
and automatic partitioning with Redis Cluster.

##############################################################################
#                                                                            #
#                           Build and Install                                #
#                                                                            #
##############################################################################
%prep
%setup -q -n "redis-%{version}"


### https://github.com/redis/redis/tree/6.2.4#building-redis
%build
%{__make} -j`nproc`  \
     MALLOC=jemalloc \
     BUILD_TLS=yes   \
     USE_SYSTEMD=no  \
     CFLAGS="-DUSE_PROCESSOR_CLOCK" \
     V=1



%install
rm -rf %{buildroot}
%{__make} install PREFIX=%{buildroot}/usr/local

mkdir -p %{buildroot}/etc/redis
mkdir -p %{buildroot}/etc/sysctl.d
mkdir -p %{buildroot}/%{_unitdir}

%{__install} -p -m 0644 %{SOURCE1} %{buildroot}/etc/redis/
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}
%{__install} -p -m 0644 %{SOURCE3} %{buildroot}/etc/redis/
%{__install} -p -m 0644 %{SOURCE4} %{buildroot}/%{_unitdir}
%{__install} -p -m 0644 %{SOURCE5} %{buildroot}/etc/sysctl.d/

%clean
rm -rf %{buildroot}

##############################################################################
#                                                                            #
#                       Scriptlet Directives                                 #
#                                                                            #
##############################################################################

%pre
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just before the package is installed        ##
##--------------------------------------------------------------------------##
# create user redis
useradd -r -c "Redis User" -s /bin/bash redis

# make work dir
mkdir -p /var/log/redis
chown -R redis:redis /var/log/redis
mkdir -p /var/run/redis
chown -R redis:redis /var/run/redis
mkdir -p /var/lib/redis
chown -R redis:redis /var/lib/redis

%post
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is installed         ##
##--------------------------------------------------------------------------##
sysctl -p /etc/sysctl.d/redis_sysctl.conf
systemctl daemon-reload
echo "#######################################################################"
echo "[DB  path]:    /var/lib/redis/                                        #"
echo "[config 1]:    /etc/redis/redis.conf                                  #"
echo "[config 2]:    /etc/redis/sentinel.conf                               #"
echo "[log path]:    /var/log/redis/redis-{server|sentinel}.log             #"
echo "[pid path]:    /var/run/redis/redis-{server|sentinel}.pid             #"
echo "[unix socket]: /var/run/redis/redis-server.sock                       #"
echo "[service 1]:   /usr/lib/systemd/system/redis-server.service           #"
echo "[service 2]:   /usr/lib/systemd/system/redis-sentinel.service         #"
echo "[Listen]:      IPv4-> 127.0.0.1:6379, IPv6 -> [::1]:6379              #"
echo "[password]:    nil                                                    #"
echo "#######################################################################"

%preun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just before the package is uninstalled      ##
##--------------------------------------------------------------------------##
systemctl stop redis-server
systemctl stop redis-sentinel

%postun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is uninstalled       ##
##--------------------------------------------------------------------------##
rm -rf /etc/redis
rm -rf /var/run/redis
rm -rf /var/log/redis
userdel -rf redis
echo "DB data still in /var/lib/redis, you can delete it manually."

%files
##############################################################################
#                                                                            #
#                                   FILES                                    #
#                                                                            #
##############################################################################

%defattr(-,redis,redis,-)
/etc/sysctl.d/redis_sysctl.conf
%{_unitdir}/redis-server.service
%{_unitdir}/redis-sentinel.service
%config /etc/redis/redis.conf
%config /etc/redis/sentinel.conf
/usr/local/bin/*


%changelog
##############################################################################
#                                                                            #
#                              Change Logs                                   #
#                                                                            #
##############################################################################
* Mon Jul 26 2021 - LubinLew lgbxyz@gmail.com
- build redis-%{version}
