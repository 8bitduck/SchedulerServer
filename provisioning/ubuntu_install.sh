#!/bin/bash
echo "Setting up Development VM"

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=ubuntu
APP_DB_PASS=ubuntu

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=SMSSchedulerServer_dev

echo "Fixing tty issue with root"
sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile

echo "Updating package lists..."
apt-get -y update
aptitude -y upgrade --safe 2> /dev/null

apt-get -y install \
  python3-pip \
  python3-dev \
  postgresql \
  postgresql-contrib \
  libpq-dev \
  libxml2-dev \
  libxslt1-dev \
  curl

# Install the python3 versions of virtualenv and wrapper
pip3 install virtualenv
pip3 install virtualenvwrapper

PG_VERSION=9.3
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
service postgresql restart

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
EOF

sudo -u postgres /usr/bin/createdb -E utf-8 -O ubuntu SMSSchedulerServer_dev

cat >> /home/ubuntu/.bashrc <<EOF
export PATH=/usr/local/bin:$PATH
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
workon SMSSchedulerServer

echo "Some helpful commands to get up and running:"
echo "--------------------------------------------"
echo "pip install -r requirements.txt   # Install the python dependencies"
EOF

su ubuntu -c "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --python=/usr/bin/python3 SMSSchedulerServer"

echo ""
echo "Finished setting up the development server."
echo ""
echo "Run the Install Requirements for pip"
echo "And then run the server"
