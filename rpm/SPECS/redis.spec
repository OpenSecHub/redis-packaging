##############################################################################
#                                                                            #
#                               Redis Packaging                              #
# Reference: https://rpm-packaging-guide.github.io/rpm-packaging-guide.pdf   #
#                                                                            #
##############################################################################
Name:           redis
Version:        7.0.0
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

Source1:        redis.service
Source2:        redis-sentinel.service
Source3:        redis_sysctl.conf

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


### https://github.com/redis/redis/tree/7.0.0#building-redis
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

sed -i 's#daemonize no#daemonize yes#' redis.conf
sed -i 's#logfile ""#logfile /var/log/redis/redis_6379.log#' redis.conf
sed -i 's#dir ./#dir /var/lib/redis/#' redis.conf
%{__install} -p -m 0644 redis.conf    %{buildroot}/etc/redis/

sed -i 's#daemonize no#daemonize yes#' sentinel.conf
sed -i 's#logfile ""#logfile /var/log/redis/sentinel.log#' sentinel.conf
%{__install} -p -m 0644 sentinel.conf %{buildroot}/etc/redis/

%{__install} -p -m 0644 %{SOURCE1}    %{buildroot}/%{_unitdir}
%{__install} -p -m 0644 %{SOURCE2}    %{buildroot}/%{_unitdir}

%{__install} -p -m 0644 %{SOURCE3}    %{buildroot}/etc/sysctl.d/




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
useradd -r -c "Redis User" redis

# make work dir
mkdir -p /var/log/redis
chown -R redis:redis /var/log/redis
mkdir -p /var/lib/redis
chown -R redis:redis /var/lib/redis

%post
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is installed         ##
##--------------------------------------------------------------------------##

sysctl -p /etc/sysctl.d/redis_sysctl.conf

echo "#######################################################################"
echo "[DB     ]:    /var/lib/redis/                                         #"
echo "[log    ]:    /var/log/redis/                                         #"
echo "[config ]:    /etc/redis/                                             #"
echo "[service]:    redis.service & redis-sentinel.service                  #"
echo "#######################################################################"
systemctl daemon-reload

%preun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just before the package is uninstalled      ##
##--------------------------------------------------------------------------##
systemctl stop redis-server   >/dev/null 2>&1
systemctl stop redis-sentinel >/dev/null 2>&1

%postun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is uninstalled       ##
##--------------------------------------------------------------------------##
rm -rf /etc/redis      >/dev/null 2>&1
rm -rf /var/log/redis  >/dev/null 2>&1
userdel -rf redis      >/dev/null 2>&1
echo "DB data still in /var/lib/redis, you can delete it manually."

%files
##############################################################################
#                                                                            #
#                                   FILES                                    #
#                                                                            #
##############################################################################

%defattr(-,root,root,-)
/etc/sysctl.d/redis_sysctl.conf
%{_unitdir}/redis.service
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
* Fri Apr 29 2022 - LubinLew lgbxyz@gmail.com
- build redis-%{version}
