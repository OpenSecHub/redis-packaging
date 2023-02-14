##############################################################################
#                                                                            #
#                               Redis Packaging                              #
# Reference: https://rpm-packaging-guide.github.io/rpm-packaging-guide.pdf   #
# https://gitlab.com/redhat/centos-stream/rpms/redis/-/blob/c9s/redis.spec   #
##############################################################################
Name:           redis
Version:        REDIS_VERSION
Release:        1%{?dist}
Summary:        A persistent key-value database
Group:          System Environment/Daemons
License:        BSD and MIT
URL:            https://redis.io/
Vendor:         redis.io
BuildArch:      x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:       LubinLew

Source0:        https://download.redis.io/releases/%{name}-%{version}.tar.gz

Source1:        redis-server.service
Source2:        redis-sentinel.service

Source3:        https://raw.githubusercontent.com/redis/redis/%{version}/redis.conf
Source4:        https://raw.githubusercontent.com/redis/redis/%{version}/sentinel.conf
Source5:        redis-sysctl.conf



BuildRequires:  systemd, systemd-devel
BuildRequires:  gcc, make
BuildRequires:  tcl, tcltls
BuildRequires:  openssl-devel

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


### https://github.com/redis/redis/tree/7.0.8#building-redis
%build
%{__make} -j`nproc`   \
     MALLOC=jemalloc  \
     BUILD_TLS=yes    \
     USE_SYSTEMD=yes  \
     CFLAGS="-DUSE_PROCESSOR_CLOCK" \
     V=1

#make test
#./utils/gen-test-certs.sh
#./runtest --tls

%install
rm -rf %{buildroot}
%{__make} install PREFIX=%{buildroot}/usr/local

mkdir -p %{buildroot}/etc/redis
mkdir -p %{buildroot}/etc/sysctl.d
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/var/lib/redis
mkdir -p %{buildroot}/var/lib/redis-sentinel
mkdir -p %{buildroot}/var/log/redis
mkdir -p %{buildroot}/var/log/redis-sentinel

%{__install} -p -m 0644 %{SOURCE1}    %{buildroot}/%{_unitdir}
%{__install} -p -m 0644 %{SOURCE2}    %{buildroot}/%{_unitdir}
%{__install} -p -m 0644 redis.conf    %{buildroot}/etc/redis/
%{__install} -p -m 0644 sentinel.conf %{buildroot}/etc/redis/
%{__install} -p -m 0644 %{SOURCE5}    %{buildroot}/etc/sysctl.d/

# set daemonize
sed -i 's#daemonize no#daemonize yes#'  %{buildroot}/etc/redis/redis.conf
sed -i 's#daemonize no#daemonize yes#'  %{buildroot}/etc/redis/sentinel.conf

# set logfile path
sed -i 's#^logfile ""#logfile /var/log/redis/redis.log#'             %{buildroot}/etc/redis/redis.conf
sed -i 's#^logfile ""#logfile /var/log/redis-sentinel/sentinel.log#' %{buildroot}/etc/redis/sentinel.conf

# set dir path
sed -i 's#^dir ./#dir /var/lib/redis/#'            %{buildroot}/etc/redis/redis.conf
sed -i 's#^dir /tmp#dir /var/lib/redis-sentinel/#' %{buildroot}/etc/redis/sentinel.conf



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
# create group
if ! getent group %{name} &> /dev/null ; then
  groupadd -r %{name} > /dev/null
fi

# create user
if ! getent passwd %{name} &> /dev/null; then
  useradd -g %{name} \
    -G %{name}       \
    -r               \
    -s /sbin/nologin \
    -c 'Redis Database Server' \
    %{name} > /dev/null
fi

exit 0



%post
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is installed         ##
##--------------------------------------------------------------------------##

sysctl -p /etc/sysctl.d/redis-sysctl.conf &> /dev/null

cat << EOF
+----------+------------------------------+--------------------------------+
| Setting  | $(tput setaf 2)redis-server$(tput sgr0)                 | $(tput setaf 1)redis-sentinel$(tput sgr0)                 |
+----------+------------------------------+--------------------------------+
| conf     | $(tput setaf 2)/etc/redis/redis-server.conf$(tput sgr0) | $(tput setaf 1)/etc/redis/redis-sentinel.conf$(tput sgr0) |
| db  path | $(tput setaf 2)/var/lib/redis/$(tput sgr0)              | $(tput setaf 1)/var/lib/redis-sentinel/$(tput sgr0)       |
| log path | $(tput setaf 2)/var/log/redis/$(tput sgr0)              | $(tput setaf 1)/var/log/redis-sentinel/$(tput sgr0)       |
| service  | $(tput setaf 2)redis-server.service$(tput sgr0)         | $(tput setaf 1)redis-sentinel.service$(tput sgr0)         |
+----------+------------------------------+--------------------------------+
EOF

systemctl daemon-reload &> /dev/null




%preun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just before the package is uninstalled      ##
##--------------------------------------------------------------------------##
systemctl stop redis-server   &>/dev/null
systemctl stop redis-sentinel &>/dev/null



%postun
##--------------------------------------------------------------------------##
##   Scriptlet that is executed just after the package is uninstalled       ##
##--------------------------------------------------------------------------##
userdel -rf redis  &>/dev/null


%files
##############################################################################
#                                                                            #
#                                   FILES                                    #
#                                                                            #
##############################################################################

## cmds
/usr/local/bin/*

## services
%{_unitdir}/redis-server.service
%{_unitdir}/redis-sentinel.service

## kernel parameters
%attr(0400, root, root) /etc/sysctl.d/redis-sysctl.conf

## config files
%dir %attr(0750, redis, root) /etc/redis
%attr(0640, redis, root) %config(noreplace) /etc/redis/redis.conf
%attr(0640, redis, root) %config(noreplace) /etc/redis/sentinel.conf

## work dir
%dir %attr(0750, redis, redis) /var/lib/redis
%dir %attr(0750, redis, redis) /var/lib/redis-sentinel

## log dir
%dir %attr(0750, redis, redis) /var/log/redis
%dir %attr(0750, redis, redis) /var/log/redis-sentinel


%changelog
##############################################################################
#                                                                            #
#                              Change Logs                                   #
#                                                                            #
##############################################################################
* RELEASE_DATE - AUTHOR
- https://github.com/redis/redis/releases/tag/%{version}
