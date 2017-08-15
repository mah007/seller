#!/bin/bash

echo "Install psycopg2"
pip3 install psycopg2

echo "Install Flask"
pip3 install flask

echo "Install flask cross platform"
pip3 install -U flask-cors

echo "Install requests"
pip3 install requests

echo "Install json"
pip3 install simplejson

echo "Install lxml"
pip3 install lxml

echo "Install jwt"
pip3 install pyjwt

echo "Install bycrypt"
pip3 install bcrypt

echo "Install selenium"
pip3 install selenium

# For bycrypt dependencies
# For Debian and Ubuntu, the following command will ensure that the required dependencies are installed:
# $ sudo apt-get install build-essential libffi-dev python-dev
# For Fedora and RHEL-derivatives, the following command will ensure that the required dependencies are installed:
# $ sudo yum install gcc libffi-devel python-devel

echo "Install mysql"
pip3 install pymysql