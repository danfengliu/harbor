#!/bin/bash
set -x

set +e
sudo rm -fr /data/*
sudo mkdir -p /data
DIR="$(cd "$(dirname "$0")" && pwd)"

set -e
if [ -z "$1" ]; then echo no ip specified; exit 1;fi
# prepare cert ...
sudo ./tests/generateCerts.sh $1
sudo mkdir -p /etc/docker/certs.d/$1 && sudo cp ./tests/harbor_ca.crt /etc/docker/certs.d/$1/ && rm -rf ~/.docker/ &&  mkdir -p ~/.docker/tls/$1:4443/ && sudo cp ./tests/harbor_ca.crt ~/.docker/tls/$1:4443/

sudo ./tests/hostcfg.sh

if [ "$2" = 'LDAP' ]; then
    cd tests && sudo ./ldapprepare.sh && cd ..
fi

#TODO: Swagger python package used to installed into dist-packages, but it's changed into site-packages all in a sudden, we havn't found the root cause.
#      so current workround is to copy swagger packages from site-packages to dist-packages.
package_dir=/usr/lib/python3.7/site-packages
if [ -d $package_dir ] && [  $(find $package_dir -type f -name "*client*.egg" | wc -l) -gt 0 ];then
    sudo cp -rf ${package_dir}/* /usr/local/lib/python3.7/dist-packages
fi

if [ $GITHUB_TOKEN ];
then
    sed "s/# github_token: xxx/github_token: $GITHUB_TOKEN/" -i make/harbor.yml
fi
