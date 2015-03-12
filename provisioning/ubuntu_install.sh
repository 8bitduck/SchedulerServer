#!/bin/bash
echo "Setting up Development VM"

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

sudo -u postgres /usr/bin/createuser -s ubuntu
sudo -u postgres /usr/bin/createdb -E utf-8 -O ubuntu SMSSchedulerServer_dev

cat >> /home/ubuntu/.bashrc <<EOF
export PATH=/usr/local/bin:$PATH
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export DEBUG=True
export TWILIO_ACCOUNT_SID=AC7089d119fc90cdf546b98867cdb9cbfe
export TWILIO_AUTH_TOKEN=2503730ee7a56c4fcdad3aabf889f9ca
source /usr/local/bin/virtualenvwrapper.sh
workon SMSSchedulerServer

echo "Some helpful commands to get up and running:"
echo "--------------------------------------------"
echo "pip install -r requirements.txt   # Install the python dependencies"
echo "./manage.py runserver [::]:8000   # Run the development server"
echo "./manage.py migrate"              # Apply database changes (to all apps)
echo "./manage.py migrate example 0002" # Roll back migrations on the example app to 0002
echo "./manage.py startapp appname"     # Start a django app called 'appname'
EOF

su ubuntu -c "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --python=/usr/bin/python3 SMSSchedulerServer"

echo ""
echo "Finished setting up the development server."
echo ""
echo "Run the Install Requirements for pip"
echo "Sync the database"
echo "And then run the server"
