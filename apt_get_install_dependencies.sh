#!/bin/bash

apt-get install python-setuptools

git submodule init
git submodule update --recursive

cd mechanize
python setup.py install
cd ../

cd beautifulsoup
python setup.py install
cd ../

cd Yahoo-ticker-symbol-downloader
python setup.py install
cd ../

easy_install jsonrpc2

apt-get install redis-server python-redis 